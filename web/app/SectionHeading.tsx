import type { ReactNode } from "react";

export function SectionHeading({
  id,
  label,
  children,
  className,
}: {
  id: string;
  label: string;
  children: ReactNode;
  className: string;
}) {
  return (
    <h2 id={`${id}-title`} className={`group ${className}`}>
      <a
        href={`#${id}`}
        aria-label={`Link to ${label} section`}
        className="rounded-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-indigo-600"
      >
        {children}
        <span
          aria-hidden="true"
          className="ml-2 hidden text-zinc-300 opacity-0 transition-opacity group-hover:opacity-100 group-focus-within:opacity-100 sm:inline"
        >
          #
        </span>
      </a>
    </h2>
  );
}
