import type { Metadata } from "next";
import "./annotator.css";

export const metadata: Metadata = {
  title: "UserBench Annotator",
  description:
    "Review Composer 2.5 gold_acts labels against history.md-style conversation context.",
};

export default function AnnotatorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <div className="annotator-shell">{children}</div>;
}
