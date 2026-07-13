import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "SWESimBench: benchmarking simulators of software engineers using coding agents",
  description:
    "SWESimBench measures how faithfully a model can stand in for a software engineer using an AI coding agent, grounded in real SWE-chat sessions. One metric, next-action prediction accuracy (did the simulator make the same move the real developer made?), across 7 simulators, on a user- and repo-disjoint test split. Full trial data downloadable.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-zinc-50 text-zinc-900 antialiased">{children}</body>
    </html>
  );
}
