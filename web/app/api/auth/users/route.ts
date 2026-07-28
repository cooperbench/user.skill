import { NextResponse } from "next/server";
import { listUsers } from "@/lib/users";

/** Public list of rater names for the passwordless picker. */
export async function GET() {
  try {
    return NextResponse.json({ users: listUsers() });
  } catch (e) {
    return NextResponse.json(
      { error: e instanceof Error ? e.message : "Failed to list users" },
      { status: 500 },
    );
  }
}
