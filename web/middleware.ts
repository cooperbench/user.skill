import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

/** Must match `COOKIE_NAME` in lib/auth.ts */
const COOKIE_NAME = "ssb_session";

/** Lightweight presence check; route handlers still verify the HMAC. */
function hasSessionCookie(req: NextRequest): boolean {
  const token = req.cookies.get(COOKIE_NAME)?.value;
  return Boolean(token && token.includes("."));
}

export function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;

  if (pathname === "/api/dashboard") {
    if (!hasSessionCookie(req)) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }
    return NextResponse.next();
  }

  if (
    pathname === "/annotator/dashboard" ||
    pathname.startsWith("/annotator/dashboard/")
  ) {
    if (!hasSessionCookie(req)) {
      const url = req.nextUrl.clone();
      url.pathname = "/annotator";
      url.searchParams.set("next", "/annotator/dashboard");
      return NextResponse.redirect(url);
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/annotator/dashboard",
    "/annotator/dashboard/:path*",
    "/api/dashboard",
  ],
};
