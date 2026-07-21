import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "UserBench — How well can agents simulate users?",
  description:
    "UserBench asks how well agents can simulate real software developers on coding-agent sessions. Harbor eval: 62 developers × 10 held-out tasks (620), scored by multilabel mean Jaccard. Leaderboard and analysis live on the dataset home.",
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
