import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Iris — Skill Gap Analysis",
  description: "Thai academic curriculum vs job market skill gap analysis",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="th">
      <body>{children}</body>
    </html>
  );
}
