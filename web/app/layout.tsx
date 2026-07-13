import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "SWESimBench v2 — a 100-developer Claude Code / Codex dataset",
  description:
    "SWESimBench measures how faithfully a model can stand in for a software engineer using an AI coding agent. The v2 dataset is 100 real developers with deep training histories and strictly-later held-out sets, harvested as full-fidelity Claude Code and Codex session traces. This site shows the data distribution; the v1 leaderboard (next-action prediction accuracy across simulators) lives at /v1.",
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
