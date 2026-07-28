"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import type { PublicUser } from "@/lib/users";
import { LoginForm } from "./LoginForm";

function safeNextPath(raw: string | null): string | null {
  if (!raw || !raw.startsWith("/") || raw.startsWith("//")) return null;
  if (raw.includes("://")) return null;
  return raw;
}

export function AuthShell({
  children,
}: {
  children: (user: PublicUser, logout: () => Promise<void>) => React.ReactNode;
}) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [user, setUser] = useState<PublicUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await fetch("/api/auth/me", { credentials: "same-origin" });
        if (!res.ok) {
          if (!cancelled) setUser(null);
          return;
        }
        const data = (await res.json()) as { user: PublicUser | null };
        if (!cancelled) setUser(data.user ?? null);
      } catch {
        if (!cancelled) setUser(null);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const logout = useCallback(async () => {
    await fetch("/api/auth/logout", {
      method: "POST",
      credentials: "same-origin",
    });
    setUser(null);
    router.replace("/annotator");
  }, [router]);

  const handleLogin = useCallback(
    (nextUser: PublicUser) => {
      setUser(nextUser);
      const next = safeNextPath(searchParams.get("next"));
      if (next) {
        router.replace(next);
      }
    },
    [router, searchParams],
  );

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-sm text-stone-600">
        Loading…
      </div>
    );
  }

  if (!user) {
    return <LoginForm onLogin={handleLogin} />;
  }

  return <>{children(user, logout)}</>;
}
