"use client";

import { Suspense, useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import type { PublicUser } from "@/lib/users";
import { DashboardView } from "../components/Dashboard";

function DashboardPublic() {
  const router = useRouter();
  const [user, setUser] = useState<PublicUser | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await fetch("/api/auth/me", { credentials: "same-origin" });
        if (!res.ok) return;
        const data = (await res.json()) as { user: PublicUser | null };
        if (!cancelled) setUser(data.user ?? null);
      } catch {
        // Public page; ignore auth probe failures.
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
    router.refresh();
  }, [router]);

  return <DashboardView user={user} logout={logout} />;
}

export default function DashboardPage() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen items-center justify-center text-sm text-stone-600">
          Loading…
        </div>
      }
    >
      <DashboardPublic />
    </Suspense>
  );
}
