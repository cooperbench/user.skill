import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "SWESimBench v2 — a 57-developer Claude Code / Codex cohort",
  description:
    "SWESimBench measures how faithfully a model can stand in for a software engineer using an AI coding agent. The authoritative v2 harbor cohort is 57 developers / 1216 held-out points with deep training histories and strictly-later held-out sets, harvested as full-fidelity Claude Code and Codex session traces. This site shows the data distribution; the v1 CondAgree leaderboard lives at /v1.",
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
