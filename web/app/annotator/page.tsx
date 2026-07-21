"use client";

import { Suspense } from "react";
import { Annotator } from "./components/Annotator";
import { AuthShell } from "./components/AuthShell";
import type { Item, Meta } from "@/lib/types";
import items from "@/public/data/items.json";
import meta from "@/public/data/meta.json";

function HomeAuthed() {
  return (
    <AuthShell>
      {(user, logout) => (
        <Annotator
          items={items as Item[]}
          meta={meta as Meta}
          user={user}
          logout={logout}
        />
      )}
    </AuthShell>
  );
}

export default function Page() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen items-center justify-center text-sm text-stone-600">
          Loading…
        </div>
      }
    >
      <HomeAuthed />
    </Suspense>
  );
}
