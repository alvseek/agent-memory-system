"""Token-counter — estimate token sizes of framework content against the MCP cap.

Standalone: no network, no required dependencies. Counts tokens per file in a
target directory, writes a sorted report, and flags files near Claude Code's MCP
tool-result limits — a **10,000-token warning** threshold and a **25,000-token
hard cap** (the cap is client-configurable via ``MAX_MCP_OUTPUT_TOKENS``; the
warning is fixed). Anything a Munnin face returns — a served Prompt, a Resource,
or an ``awaken`` payload — is subject to that cap, so oversized content is
silently truncated at the client.

Counting method (best available, offline — both are ESTIMATES):
  1. ``tiktoken`` if importable (``cl100k_base``) — close to Claude for English;
  2. else a rough ``len(text) / 4`` heuristic.
Claude's own tokenizer differs from both — keep ~10-20% headroom vs the real cap.

Run (from the control-files root)::

    python procedures/setup-scripts/token-counter.py [--path DIR] [--out FILE] [--strict]

Default target: ``procedures/output/`` (the compiled procedure previews from
``compile-procedures.py``). Point ``--path`` at the memory store to size an
``awaken`` payload. Report → ``procedures/output/token-report.md``.
"""

from __future__ import annotations

import argparse
from pathlib import Path

# control-files/ root (this script lives at procedures/setup-scripts/token-counter.py).
_CF_ROOT = Path(__file__).resolve().parents[2]

WARN = 10_000  # Claude Code MCP warning threshold (fixed)
CAP = 25_000   # Claude Code MCP hard cap (default; MAX_MCP_OUTPUT_TOKENS overrides)
_REPORT_NAME = "token-report.md"


def make_counter() -> tuple:
    """Return (count_fn, method_label) — the best offline token estimator available."""
    try:
        import tiktoken

        enc = tiktoken.get_encoding("cl100k_base")

        def _tik(s: str) -> int:
            return len(enc.encode(s, disallowed_special=()))

        return (_tik, "tiktoken cl100k_base (estimate)")
    except Exception:
        def _approx(s: str) -> int:
            return max(1, round(len(s) / 4))

        return (_approx, "chars/4 heuristic (rough estimate)")


def _status(tokens: int) -> str:
    if tokens >= CAP:
        return "over cap"
    if tokens >= WARN:
        return "warn"
    return "ok"


def _icon(status: str) -> str:
    return {"over cap": "over-cap", "warn": "warn", "ok": "ok"}[status]


def count_dir(path: Path, count_fn, pattern: str) -> list[tuple[Path, int]]:
    """Token count per file matching ``pattern`` under ``path``, sorted largest-first.

    Excludes this tool's own report file so re-runs don't count it.
    """
    rows: list[tuple[Path, int]] = []
    for f in sorted(path.rglob(pattern)):
        if f.name == _REPORT_NAME or not f.is_file():
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        rows.append((f, count_fn(text)))
    rows.sort(key=lambda r: r[1], reverse=True)
    return rows


def build_report(rows: list[tuple[Path, int]], path: Path, method: str) -> str:
    total = sum(t for _, t in rows)
    over = [(f, t) for f, t in rows if t >= CAP]
    warn = [(f, t) for f, t in rows if WARN <= t < CAP]

    lines = [
        "# Token Report",
        "",
        f"- **Method**: {method} — Claude's real tokenizer differs; keep ~10-20% headroom.",
        f"- **Thresholds**: warn {WARN:,} · cap {CAP:,} (Claude Code MCP tool result; "
        "cap overridable client-side via `MAX_MCP_OUTPUT_TOKENS`).",
        f"- **Target**: `{path}` — {len(rows)} file(s), {total:,} tokens total.",
        "",
        "| file | tokens | status |",
        "|------|-------:|:------:|",
    ]
    for f, t in rows:
        try:
            name = f.relative_to(path).as_posix()
        except ValueError:
            name = f.name
        lines.append(f"| {name} | {t:,} | {_icon(_status(t))} |")

    lines += ["", "## Flags", ""]
    if over:
        listing = ", ".join(f"{f.name} ({t:,})" for f, t in over)
        lines.append(f"- 🚫 **over cap ({CAP:,})**: {listing}")
    if warn:
        listing = ", ".join(f"{f.name} ({t:,})" for f, t in warn)
        lines.append(f"- ⚠️ **warn (≥{WARN:,})**: {listing}")
    if not over and not warn:
        lines.append(f"- ✅ all files under the {WARN:,}-token warning threshold.")
    lines.append("")
    return "\n".join(lines)


def _print_summary(rows: list[tuple[Path, int]], method: str, out_path: Path) -> int:
    print(f"\nToken counts ({method}) - warn {WARN:,} / cap {CAP:,}\n")
    print(f"{'file':<40} {'tokens':>8}  status")
    print(f"{'-' * 40} {'-' * 8}  {'-' * 8}")
    over = 0
    for f, t in rows:
        st = _status(t)
        if st == "over cap":
            over += 1
        print(f"{f.name:<40} {t:>8,}  {_icon(st)}")
    total = sum(t for _, t in rows)
    print(f"\n{len(rows)} file(s), {total:,} tokens total -> {out_path}\n")
    return over


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--path", type=Path, default=_CF_ROOT / "procedures" / "output",
        help="directory to scan (default: procedures/output)",
    )
    parser.add_argument(
        "--glob", default="*.md", help="filename pattern to count (default: *.md)"
    )
    parser.add_argument(
        "--out", type=Path, default=None,
        help="report path (default: <path>/token-report.md)",
    )
    parser.add_argument(
        "--strict", action="store_true", help="exit non-zero if any file is over the cap"
    )
    args = parser.parse_args(argv)

    if not args.path.exists():
        parser.error(
            f"target not found: {args.path}"
            + (" — run compile-procedures.py first?" if args.path.name == "output" else "")
        )

    count_fn, method = make_counter()
    rows = count_dir(args.path, count_fn, args.glob)
    if not rows:
        print(f"no files matching '{args.glob}' under {args.path}")
        return 0

    out_path = args.out or (args.path / _REPORT_NAME)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_report(rows, args.path, method), encoding="utf-8")

    over = _print_summary(rows, method, out_path)
    return 1 if args.strict and over else 0


if __name__ == "__main__":
    raise SystemExit(main())
