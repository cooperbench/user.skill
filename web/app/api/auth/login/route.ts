import { NextResponse } from "next/server";
import { setSessionCookie } from "@/lib/auth";
import { findUserById } from "@/lib/users";

export async function POST(req: Request) {
  let body: { userId?: string };
  try {
    body = (await req.json()) as { userId?: string };
  } catch {
    return NextResponse.json({ error: "Invalid JSON" }, { status: 400 });
  }

  const userId = (body.userId || "").trim();
  if (!userId) {
    return NextResponse.json({ error: "userId required" }, { status: 400 });
  }

  const user = findUserById(userId);
  if (!user) {
    return NextResponse.json({ error: "Unknown user" }, { status: 401 });
  }

  await setSessionCookie(user.id);
  return NextResponse.json({ user });
}
