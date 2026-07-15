> DEVELOPER

Continue building the `signalkit` library (read the existing code first). Add a small feature: a function `fetch_frames(url, **kwargs)` in `signalkit/client.py` that calls the existing `fetch(url, **kwargs)` and then `parse_frame` on the result, returning the parsed dict. Also add a tiny CLI in `signalkit/__main__.py` so `python3 -m signalkit <url>` prints the parsed frame. Add tests for `fetch_frames`. Keep using only the standard library, keep retry behavior unchanged. Run the tests and make sure all pass, then commit it yourself with git and a clear message.

> AGENT

Let me read the existing code first.

> AGENT

I have a clear picture of the code. Now I'll add `fetch_frames`, the CLI, update exports, and add tests — all in parallel.

> AGENT

Now add tests for `fetch_frames` to `tests/test_client.py`.

> AGENT

All 10 tests pass. Now committing.

> AGENT

Done. Here's what was added: - **`signalkit/client.py`** — `fetch_frames(url, **kwargs)` calls `fetch` then `parse_frame` and returns the dict. Retry behavior is unchanged. - **`signalkit/__main__.py`** — `python3 -m signalkit <url>` prints each `key=value` pair from the parsed frame. - **`signalkit/__init__.py`** — `fetch_frames` added to `__all__`. - **`tests/test_client.py`** — 3 new tests: parsed dict result, empty body, and `**kwargs` forwarding to the underlying `fetch`. All 10 tests pass; committed as `2bc197b`.
