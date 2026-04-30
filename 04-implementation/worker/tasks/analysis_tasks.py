import json
import logging
from datetime import datetime

from celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=1)
def run_gap_analysis(self, analysis_id: int):
    """
    Compute gap analysis for a GapAnalysis record.
    Handles both programme-to-market and programme-to-programme modes.
    """
    from sqlalchemy.orm import Session
    from app.database import SessionLocal
    from app.models.analysis import GapAnalysis, GapResult
    from app.models.programme import Programme, Course, CourseSkill
    from app.models.vocab import SkillCluster
    from pipeline.vocab_builder import VocabularyBuilder, build_skill_distribution
    from pipeline.skill_extractor import CourseSkillSet
    from pipeline.gap_engine import (
        kl_divergence_market_programme, cosine_similarity,
        rank_gaps, decompose_skills, build_heatmap_data,
        build_market_distribution, compute_rca,
    )

    db: Session = SessionLocal()
    try:
        analysis = db.query(GapAnalysis).filter(GapAnalysis.id == analysis_id).first()
        if not analysis:
            logger.error("Analysis %d not found", analysis_id)
            return

        analysis.status = "running"
        db.commit()

        # Load vocabulary
        clusters = db.query(SkillCluster).all()
        canonical = {c.id: c.label for c in clusters}

        # Rebuild VocabularyBuilder from DB state for assignment
        from pipeline.vocab_builder import VocabularyBuilder
        vocab = _load_vocab_from_db(db)

        # Build programme distribution
        course_skill_sets = _load_course_skill_sets(db, analysis.programme_id)
        prog_dist = build_skill_distribution(course_skill_sets, vocab, scenario=analysis.scenario)

        if analysis.career_path:
            # Programme-to-market mode
            market_dist = build_market_distribution(db, analysis.career_path)
            kl = kl_divergence_market_programme(market_dist, prog_dist)
            cos_sim = cosine_similarity(market_dist, prog_dist)
            ranked = rank_gaps(market_dist, prog_dist, canonical=canonical)
            decomp = decompose_skills(market_dist, prog_dist, canonical=canonical)
            heatmap = build_heatmap_data(course_skill_sets, vocab)

        else:
            # Programme-to-programme mode
            other_sets = _load_course_skill_sets(db, analysis.compare_programme_id)
            other_dist = build_skill_distribution(other_sets, vocab, scenario=analysis.scenario)
            kl = kl_divergence_market_programme(other_dist, prog_dist)
            cos_sim = cosine_similarity(prog_dist, other_dist)
            ranked = rank_gaps(other_dist, prog_dist, canonical=canonical)
            decomp = decompose_skills(prog_dist, other_dist, canonical=canonical)
            heatmap = build_heatmap_data(course_skill_sets, vocab)

        result = GapResult(
            analysis_id=analysis_id,
            kl_divergence=kl,
            cosine_similarity=cos_sim,
            ranked_gaps=ranked,
            skill_decomposition=decomp,
            heatmap_data=heatmap,
        )
        db.add(result)
        analysis.status = "completed"
        analysis.completed_at = datetime.utcnow()
        db.commit()
        logger.info("Gap analysis %d completed — KL=%.4f, cosine=%.4f", analysis_id, kl, cos_sim)

    except Exception as exc:
        db.rollback()
        analysis = db.query(GapAnalysis).filter(GapAnalysis.id == analysis_id).first()
        if analysis:
            analysis.status = "failed"
            db.commit()
        logger.exception("Gap analysis %d failed", analysis_id)
        raise self.retry(exc=exc, countdown=10)
    finally:
        db.close()


def _load_course_skill_sets(db, programme_id: int):
    from app.models.programme import Course, CourseSkill
    from pipeline.skill_extractor import CourseSkillSet

    courses = db.query(Course).filter(Course.programme_id == programme_id).all()
    result = []
    for course in courses:
        skills = [cs.raw_skill for cs in course.skills]
        result.append(CourseSkillSet(
            course_code=course.code or "",
            course_name_th=course.name_th or "",
            course_name_en=course.name_en or "",
            category=course.category.value,
            credits=course.credits,
            skills=skills,
        ))
    return result


def _load_vocab_from_db(db):
    """Reconstruct a minimal VocabularyBuilder with canonical labels for assignment."""
    from app.models.vocab import SkillCluster, SkillToken
    from pipeline.vocab_builder import VocabularyBuilder
    import json
    import numpy as np

    clusters = db.query(SkillCluster).all()
    tokens = db.query(SkillToken).all()

    vb = VocabularyBuilder()
    vb.canonical = {c.id: c.label for c in clusters}
    vb.skill_terms = [t.raw_text for t in tokens]

    labels = []
    embeddings = []
    for t in tokens:
        labels.append(t.cluster_id if t.cluster_id is not None else -1)
        if t.embedding_json:
            embeddings.append(json.loads(t.embedding_json))

    if labels:
        vb.cluster_labels = np.array(labels)
    if embeddings:
        vb.embeddings = np.array(embeddings, dtype=np.float32)

    return vb
