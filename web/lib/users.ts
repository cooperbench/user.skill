import type { PublicUser } from "./types";

export type { PublicUser };

export type RaterUser = {
  id: string;
  displayName: string;
};

function parseUsers(): RaterUser[] {
  const raw = process.env.RATER_USERS;
  if (!raw) {
    throw new Error("RATER_USERS env var is not set");
  }
  const parsed = JSON.parse(raw) as RaterUser[];
  if (!Array.isArray(parsed) || parsed.length === 0) {
    throw new Error("RATER_USERS must be a non-empty JSON array");
  }
  for (const u of parsed) {
    if (!u?.id || !u?.displayName) {
      throw new Error("Each RATER_USERS entry needs id and displayName");
    }
  }
  return parsed;
}

export function listUsers(): PublicUser[] {
  return parseUsers().map(({ id, displayName }) => ({ id, displayName }));
}

/** Whitelist lookup for passwordless login. */
export function findUserById(userId: string): PublicUser | null {
  const id = userId.trim().toLowerCase();
  if (!id) return null;
  const user = parseUsers().find((u) => u.id.toLowerCase() === id);
  if (!user) return null;
  return { id: user.id, displayName: user.displayName };
}

export function getUserById(userId: string): PublicUser | null {
  const user = parseUsers().find((u) => u.id === userId);
  if (!user) return null;
  return { id: user.id, displayName: user.displayName };
}
