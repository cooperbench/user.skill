"use client";

import { Suspense } from "react";
import { AuthShell } from "../components/AuthShell";
import { DashboardView } from "../components/Dashboard";

function DashboardAuthed() {
  return (
    <AuthShell>
      {(user, logout) => <DashboardView user={user} logout={logout} />}
    </AuthShell>
  );
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
      <DashboardAuthed />
    </Suspense>
  );
}
