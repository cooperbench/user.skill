"use client";

import { useEffect } from "react";

/** Former standalone results page — content lives on the dataset home. */
export default function ResultsRedirect() {
  useEffect(() => {
    window.location.replace("/#leaderboard");
  }, []);

  return (
    <main className="mx-auto max-w-4xl px-6 py-14">
      <p className="text-sm text-zinc-500">
        Results moved to the{" "}
        <a href="/#leaderboard" className="text-indigo-600 hover:underline">
          dataset page
        </a>
        …
      </p>
    </main>
  );
}
