[DEVELOPER]: fix lint issues

[AGENT]: 3 gosec G115 issues (integer overflow conversion `uintptr -> int`) in `status_style.go`. Let me read the relevant lines.

[AGENT]: The fix is to use `#nosec G115` or, better, to use the safe conversion available in Go 1.26. Since `Fd()` returns `uintptr` and `term.IsTerminal`/`term.GetSize` take `int`, and file descriptors are always small non-negative integers, the cleanest fix is to suppress the lint with a comment. However, let me check if there's a preferred pattern in this codebase.

[AGENT]: There's an existing pattern in `explain.go` using `//nolint:gosec` comments. I'll apply the same pattern.

[AGENT]: The second edit only matched one of the two `GetSize` calls (since they have different preceding lines). Let me fix the remaining one on line 89.

[AGENT]: Now let me verify the lint passes.

[AGENT]: All clean. Added `//nolint:gosec // G115: uintptr->int is safe for fd` comments to the 3 `uintptr`-to-`int` conversions in `status_style.go`, matching the existing pattern in `explain.go`.