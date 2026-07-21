"use client";

import { useMemo } from "react";
import ReactMarkdown, { type Components } from "react-markdown";
import remarkBreaks from "remark-breaks";
import remarkGfm from "remark-gfm";

type Block = { role: string; body: string };

const ROLE_STYLE: Record<string, string> = {
  DEVELOPER: "border-teal-700/30 bg-teal-50/70 text-teal-950",
  AGENT: "border-stone-300 bg-white text-stone-900",
  TOOL: "border-amber-700/20 bg-amber-50/50 text-stone-800",
  SYSTEM: "border-violet-300/40 bg-violet-50/50 text-stone-800",
  METADATA: "border-stone-200 bg-stone-50 text-stone-700",
};

const ROLE_LABEL: Record<string, string> = {
  DEVELOPER: "DEVELOPER",
  AGENT: "AGENT",
  TOOL: "TOOL",
  SYSTEM: "SYSTEM",
  METADATA: "METADATA",
};

/** Leading `…` from context trim is not real METADATA — skip it. */
function isTruncationPlaceholder(body: string): boolean {
  const t = body.trim();
  return !t || t === "…" || t === "..." || t === "…\n" || /^(\.|…)+$/.test(t);
}

function parseHistory(md: string): Block[] {
  if (!md?.trim()) return [];
  const parts = ("\n" + md.trim()).split(
    /\n(?=> (?:DEVELOPER|AGENT|TOOL|SYSTEM|METADATA)\n)/,
  );
  const out: Block[] = [];
  for (const part of parts) {
    const t = part.trim();
    if (!t) continue;
    const m = t.match(/^> (DEVELOPER|AGENT|TOOL|SYSTEM|METADATA)\n\n?([\s\S]*)$/);
    if (!m) {
      // Unparsed lead-in is almost always the trim marker `…`
      if (isTruncationPlaceholder(t)) continue;
      out.push({ role: "METADATA", body: t });
      continue;
    }
    const body = m[2].replace(/\n$/, "");
    if (m[1] === "METADATA" && isTruncationPlaceholder(body)) continue;
    out.push({ role: m[1], body });
  }
  return out;
}

function makeMarkdownComponents(compact: boolean): Components {
  const pMb = compact ? "mb-1" : "mb-2";
  const listMb = compact ? "mb-1" : "mb-2";
  const prePad = compact ? "px-2 py-1.5" : "px-2.5 py-2";
  const textSize = compact ? "text-[12.5px]" : "text-[12.5px]";
  return {
    p: ({ children }) => (
      <p className={`${pMb} last:mb-0 break-words`}>{children}</p>
    ),
    h1: ({ children }) => (
      <h1
        className={`${compact ? "mb-1 mt-2 text-[13px]" : "mb-2 mt-3 text-base"} font-semibold first:mt-0`}
      >
        {children}
      </h1>
    ),
    h2: ({ children }) => (
      <h2
        className={`${compact ? "mb-1 mt-2 text-[13px]" : "mb-2 mt-3 text-[15px]"} font-semibold first:mt-0`}
      >
        {children}
      </h2>
    ),
    h3: ({ children }) => (
      <h3
        className={`${compact ? "mb-0.5 mt-1.5 text-[12.5px]" : "mb-1.5 mt-2.5 text-[14px]"} font-semibold first:mt-0`}
      >
        {children}
      </h3>
    ),
    ul: ({ children }) => (
      <ul
        className={`${listMb} list-disc ${compact ? "space-y-0.5" : "space-y-1"} pl-5 last:mb-0`}
      >
        {children}
      </ul>
    ),
    ol: ({ children }) => (
      <ol
        className={`${listMb} list-decimal ${compact ? "space-y-0.5" : "space-y-1"} pl-5 last:mb-0`}
      >
        {children}
      </ol>
    ),
    li: ({ children }) => <li className="break-words">{children}</li>,
    a: ({ href, children }) => (
      <a
        href={href}
        className="underline underline-offset-2 decoration-stone-400 hover:decoration-stone-700"
        target="_blank"
        rel="noreferrer"
      >
        {children}
      </a>
    ),
    blockquote: ({ children }) => (
      <blockquote
        className={`${listMb} border-l-2 border-stone-400/50 pl-3 italic opacity-90 last:mb-0`}
      >
        {children}
      </blockquote>
    ),
    hr: () => (
      <hr className={`${compact ? "my-2" : "my-3"} border-stone-300/60`} />
    ),
    table: ({ children }) => (
      <div className={`${listMb} overflow-x-auto last:mb-0`}>
        <table className={`min-w-full border-collapse ${textSize}`}>
          {children}
        </table>
      </div>
    ),
    thead: ({ children }) => (
      <thead className="border-b border-stone-300/70">{children}</thead>
    ),
    th: ({ children }) => (
      <th
        className={`${compact ? "px-1.5 py-0.5" : "px-2 py-1"} text-left font-semibold`}
      >
        {children}
      </th>
    ),
    td: ({ children }) => (
      <td
        className={`border-t border-stone-200/80 ${compact ? "px-1.5 py-0.5" : "px-2 py-1"} align-top`}
      >
        {children}
      </td>
    ),
    code: ({ className, children }) => {
      const text = String(children);
      const isBlock =
        Boolean(className?.includes("language-")) || text.includes("\n");
      if (isBlock) {
        return (
          <code className="font-mono text-[12px] leading-snug text-inherit">
            {children}
          </code>
        );
      }
      return (
        <code className="rounded bg-black/[0.06] px-1 py-0.5 font-mono text-[12px]">
          {children}
        </code>
      );
    },
    pre: ({ children }) => (
      <pre
        className={`${listMb} overflow-x-auto rounded-md border border-black/5 bg-black/[0.04] ${prePad} font-mono text-[12px] leading-snug last:mb-0`}
      >
        {children}
      </pre>
    ),
  };
}

/** Shared markdown renderer (GFM + italics/bold). Used by history turns and Taxonomy tip. */
export function MarkdownProse({
  body,
  compact,
  className,
}: {
  body: string;
  compact?: boolean;
  className?: string;
}) {
  const components = useMemo(
    () => makeMarkdownComponents(Boolean(compact)),
    [compact],
  );
  return (
    <div
      className={[
        "font-body [overflow-wrap:anywhere]",
        compact
          ? "text-[12.5px] leading-snug"
          : "text-[13.5px] leading-relaxed",
        className ?? "",
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkBreaks]}
        components={components}
      >
        {body}
      </ReactMarkdown>
    </div>
  );
}

function TurnMarkdown({
  body,
  compact,
}: {
  body: string;
  compact?: boolean;
}) {
  return <MarkdownProse body={body} compact={compact} />;
}

export function HistoryBlocks({
  markdown,
  compact,
  emptyLabel = "No prior context.",
}: {
  markdown: string;
  /** @deprecated no longer applies a ring; kept optional for call-site compat */
  emphasize?: boolean;
  compact?: boolean;
  emptyLabel?: string;
}) {
  const blocks = useMemo(() => parseHistory(markdown), [markdown]);
  if (!blocks.length) {
    return <p className="text-sm text-stone-500 italic">{emptyLabel}</p>;
  }
  return (
    <div className={compact ? "space-y-1.5" : "space-y-3"}>
      {blocks.map((b, i) => (
        <article
          key={i}
          className={[
            "rounded-md border",
            compact ? "px-2.5 py-1.5" : "px-3 py-2.5",
            ROLE_STYLE[b.role] || ROLE_STYLE.METADATA,
          ].join(" ")}
        >
          <div
            className={[
              "font-mono font-medium tracking-[0.08em] uppercase opacity-70",
              compact ? "mb-0.5 text-[10px]" : "mb-1.5 text-[11px]",
            ].join(" ")}
          >
            {ROLE_LABEL[b.role] || b.role}
          </div>
          <TurnMarkdown body={b.body} compact={compact} />
        </article>
      ))}
    </div>
  );
}
