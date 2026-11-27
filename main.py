"""One Emoji, One Dream Vacation entry: write exactly one emoji to /output/entry.txt.

The entry is a single emoji, nothing else: U+1F3DD DESERT ISLAND -- a lone
palm island in a turquoise sea, the wordless postcard of a dream vacation.
One Unicode code point, 4 UTF-8 bytes, no trailing newline, so the sealed
gate (1-8 UTF-8 characters, not only whitespace) passes cleanly.
"""

import os
import stat

EMOJI = "\U0001F3DD"  # 🏝 DESERT ISLAND
OUT = "/output/entry.txt"

# Sealed gate: the entry must be 1-8 UTF-8 characters, not only whitespace.
if not (1 <= len(EMOJI) <= 8 and EMOJI.strip()):
    raise SystemExit(f"entry emoji invalid: {len(EMOJI)} chars")


def main() -> None:
    data = EMOJI.encode("utf-8")
    os.makedirs("/output", exist_ok=True)
    with open(OUT, "wb") as f:
        f.write(data)
    # The grader collects /output as another user: leave the file world-readable.
    os.chmod(OUT, 0o644)
    # Verify the mode actually landed: a file the grader cannot read fails the run.
    if stat.S_IMODE(os.stat(OUT).st_mode) != 0o644:
        raise SystemExit("entry.txt mode is not 0644")
    # Read-back check: what landed on disk must be exactly the emoji.
    with open(OUT, "rb") as f:
        written = f.read()
    if written != data:
        raise SystemExit("entry.txt does not match EMOJI")
    # Byte check: U+1F3DD must encode to exactly 4 UTF-8 bytes, and the file
    # must decode to exactly one code point -- a variation selector or a
    # second emoji smuggled in would fail the "exactly one emoji" brief.
    if len(written) != 4:
        raise SystemExit(f"entry.txt must be 4 bytes, got {len(written)}")
    if len(written.decode("utf-8")) != 1:
        raise SystemExit("entry.txt must hold exactly one code point")
    print(f"wrote {EMOJI!r} (U+1F3DD, 4 bytes, 1 char) to {OUT}, mode 0644")


if __name__ == "__main__":
    main()
