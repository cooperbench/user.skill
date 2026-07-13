import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "SWESimBench v2 — message samples",
  description:
    "Browse 10 randomly sampled user messages with surrounding context from each of the 57 developers in the SWESimBench v2 harbor cohort.",
};

export default function SamplesLayout({ children }: { children: React.ReactNode }) {
  return children;
}
