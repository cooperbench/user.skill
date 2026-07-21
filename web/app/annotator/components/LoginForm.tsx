"use client";

import { useEffect, useState } from "react";
import type { PublicUser } from "@/lib/users";

export function LoginForm({
  onLogin,
}: {
  onLogin: (user: PublicUser) => void;
}) {
  const [users, setUsers] = useState<PublicUser[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [busyId, setBusyId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await fetch("/api/auth/users");
        const data = (await res.json()) as {
          users?: PublicUser[];
          error?: string;
        };
        if (!res.ok || !data.users) {
          if (!cancelled) setError(data.error || "Could not load annotators");
          return;
        }
        if (!cancelled) setUsers(data.users);
      } catch {
        if (!cancelled) setError("Network error");
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const enterAs = async (userId: string) => {
    setBusyId(userId);
    setError(null);
    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId }),
      });
      const data = (await res.json()) as { user?: PublicUser; error?: string };
      if (!res.ok || !data.user) {
        setError(data.error || "Login failed");
        return;
      }
      onLogin(data.user);
    } catch {
      setError("Network error");
    } finally {
      setBusyId(null);
    }
  };

  return (
    <div className="mx-auto flex min-h-screen max-w-md flex-col justify-center px-4 py-10">
      <div className="rounded-lg border border-rule bg-panel p-6 shadow-sm">
        <p className="font-mono text-[11px] uppercase tracking-[0.14em] text-accent">
          UserBench
        </p>
        <h1 className="mt-1 font-display text-2xl font-semibold text-ink">
          Choose annotator
        </h1>
        <p className="mt-2 text-sm text-stone-600">
          Click your name to continue. Labels stay private to you until you open
          the shared dashboard.
        </p>

        {loading ? (
          <p className="mt-5 text-sm text-stone-500">Loading…</p>
        ) : (
          <ul className="mt-5 space-y-2">
            {users.map((u) => (
              <li key={u.id}>
                <button
                  type="button"
                  disabled={busyId !== null}
                  onClick={() => void enterAs(u.id)}
                  className="w-full rounded-md border border-rule bg-paper px-3 py-3 text-left text-sm font-medium text-ink transition hover:border-accent hover:bg-accent/5 disabled:opacity-50"
                >
                  {busyId === u.id ? "Entering…" : u.displayName}
                </button>
              </li>
            ))}
          </ul>
        )}

        {error ? (
          <p className="mt-3 text-sm text-rose-700" role="alert">
            {error}
          </p>
        ) : null}
      </div>
    </div>
  );
}
