import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "UserBench — 62-developer coding-agent eval",
  description:
    "UserBench measures how faithfully a model can stand in for a software engineer using an AI coding agent. The public Harbor eval is 62 developers × 10 held-out tasks (620 total), from full-fidelity Claude Code and Codex session traces (Entire, GitHub crawl, DataClaw; Opus 4.6 era ≥2026-02-05). This site shows the data distribution; an older next-action leaderboard lives at /v1.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        {/* Vercel Web Analytics */}
        <script defer src="/_vercel/insights/script.js"></script>
      </head>
      <body className="bg-zinc-50 text-zinc-900 antialiased">{children}</body>
    </html>
  );
}
