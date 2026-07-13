"use client";

import { useMemo, useState } from "react";
import raw from "../v2_samples.json";

type Turn = {
  role: string;
  text: string;
  clipped: boolean;
  focal: boolean;
};

type Sample = {
  session_id: string;
  repo: string;
  source: string;
  start_time: string | null;
  turn_index: number;
  n_turns: number;
  window: Turn[];
};

type Dev = {
  user: string;
  n_available: number;
  samples: Sample[];
};

type Payload = {
  dataset: string;
  policy_version: string;
  n_developers: number;
  n_samples_per_developer: number;
  n_samples_total: number;
  context_before: number;
  context_after: number;
  note: string;
  developers: Dev[];
};

const data = raw as Payload;

function roleStyle(role: string, focal: boolean) {
  if (focal) return "border-emerald-300 bg-emerald-50/80";
  if (role === "user") return "border-zinc-200 bg-white";
  if (role === "assistant") return "border-zinc-100 bg-zinc-50";
  if (role === "tool") return "border-amber-100 bg-amber-50/40";
  return "border-zinc-100 bg-zinc-50";
}

function roleLabel(role: string, focal: boolean) {
  if (focal) return "user · sampled";
  return role;
}

function SampleCard({ sample, index }: { sample: Sample; index: number }) {
  return (
    <article className="overflow-hidden rounded-xl border border-zinc-200 bg-white">
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1 border-b border-zinc-100 bg-zinc-50/80 px-4 py-2.5 text-[11px] text-zinc-500">
        <span className="font-mono font-semibold text-zinc-700">#{index + 1}</span>
        <span className="font-mono">{sample.repo}</span>
        <span>{sample.source}</span>
        {sample.start_time && <span>{sample.start_time}</span>}
        <span className="font-mono text-zinc-400">
          turn {sample.turn_index}/{sample.n_turns - 1}
        </span>
      </div>
      <div className="space-y-2 p-3">
        {sample.window.map((t, i) => (
          <div key={i} className={`rounded-lg border px-3 py-2 ${roleStyle(t.role, t.focal)}`}>
            <div className="mb-1 flex items-center justify-between gap-2">
              <span className={`font-mono text-[10px] uppercase tracking-wider ${t.focal ? "font-semibold text-emerald-700" : "text-zinc-400"}`}>
                {roleLabel(t.role, t.focal)}
              </span>
              {t.clipped && <span className="font-mono text-[10px] text-zinc-400">truncated</span>}
            </div>
            <pre className={`whitespace-pre-wrap break-words font-sans text-[13px] leading-relaxed ${t.focal ? "text-zinc-900" : "text-zinc-600"}`}>
              {t.text}
            </pre>
          </div>
        ))}
      </div>
    </article>
  );
}

export default function SamplesPage() {
  const developers = data.developers;
  const [user, setUser] = useState(developers[0]?.user ?? "");
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return developers;
    return developers.filter((d) => d.user.toLowerCase().includes(q));
  }, [developers, query]);

  const current = developers.find((d) => d.user === user) ?? filtered[0] ?? developers[0];

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-10 border-b border-zinc-200 bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-3">
          <h1 className="text-sm font-semibold tracking-tight">
            <a href="/" className="hover:text-zinc-600">
              SWESimBench
            </a>{" "}
            · <span className="text-zinc-400">message samples</span>
          </h1>
          <div className="flex items-center gap-3 text-xs text-zinc-500">
            <a href="/" className="hover:text-zinc-900">
              v2 cohort
            </a>
            <a href="/v1" className="hover:text-zinc-900">
              v1 leaderboard
            </a>
            <a href="/data" className="hover:text-zinc-900">
              data
            </a>
          </div>
        </div>
      </header>

      <main className="mx-auto grid max-w-5xl gap-8 px-6 py-10 lg:grid-cols-[240px_1fr]">
        <aside className="lg:sticky lg:top-16 lg:self-start">
          <div className="text-xs font-semibold uppercase tracking-wide text-indigo-500">browse</div>
          <h2 className="mt-1 text-lg font-semibold tracking-tight text-zinc-900">
            {data.n_samples_per_developer} messages × {data.n_developers} developers
          </h2>
          <p className="mt-2 text-xs leading-relaxed text-zinc-500">{data.note}</p>

          <label className="mt-4 block">
            <span className="sr-only">Filter developers</span>
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Filter developers…"
              className="w-full rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-800 outline-none ring-emerald-500/30 placeholder:text-zinc-400 focus:ring-2"
            />
          </label>

          <div className="mt-3 max-h-[28rem] overflow-y-auto rounded-xl border border-zinc-200 bg-white">
            {filtered.map((d) => {
              const active = d.user === current?.user;
              return (
                <button
                  key={d.user}
                  type="button"
                  onClick={() => setUser(d.user)}
                  className={`flex w-full items-center justify-between gap-2 border-b border-zinc-100 px-3 py-2 text-left text-sm last:border-b-0 ${
                    active ? "bg-emerald-50 text-emerald-900" : "text-zinc-700 hover:bg-zinc-50"
                  }`}
                >
                  <span className="truncate font-mono text-xs">{d.user}</span>
                  <span className="shrink-0 font-mono text-[10px] text-zinc-400">{d.samples.length}</span>
                </button>
              );
            })}
            {filtered.length === 0 && (
              <div className="px-3 py-4 text-xs text-zinc-400">No developers match.</div>
            )}
          </div>
        </aside>

        <section>
          {current ? (
            <>
              <div className="mb-5">
                <div className="font-mono text-[11px] uppercase tracking-wider text-zinc-400">developer</div>
                <h3 className="mt-1 font-mono text-xl font-semibold text-zinc-900">{current.user}</h3>
                <p className="mt-1 text-sm text-zinc-500">
                  Showing {current.samples.length} sampled user messages
                  {current.n_available > current.samples.length && (
                    <> (from {current.n_available.toLocaleString()} eligible user turns)</>
                  )}
                  . Each card highlights the sampled user turn with ±{data.context_before}/+{data.context_after} surrounding turns.
                </p>
              </div>
              <div className="space-y-4">
                {current.samples.map((s, i) => (
                  <SampleCard key={`${s.session_id}-${s.turn_index}`} sample={s} index={i} />
                ))}
              </div>
            </>
          ) : (
            <p className="text-sm text-zinc-500">Select a developer.</p>
          )}
        </section>
      </main>
    </div>
  );
}
