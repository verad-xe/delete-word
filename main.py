#!/usr/bin/env python3
"""The Word You'd Delete From the Dictionary.

Writes the single word this entry would erase from the dictionary
forever to $MAKEFUN_OUTPUT_DIR/entry.txt, after a gate self-check:
UTF-8 text, 1 to 77 characters, exactly one word, nothing else.
"""

import os
import sys

# The word to delete: it is a double negative that means the opposite
# of what its parts say, and the language loses nothing without it --
# the dictionary would be correcting its own mistake.
WORD = "irregardless"

MIN_CHARS = 1
MAX_CHARS = 77


def gate_check(text: str) -> None:
    """Assert the entry meets the competition's gate before writing."""
    if not isinstance(text, str):
        raise AssertionError("entry must be text")
    if not text.strip():
        raise AssertionError("entry must not be only white space")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise AssertionError(
            f"entry must be {MIN_CHARS} to {MAX_CHARS} characters, "
            f"got {len(text)}"
        )
    if len(text.split()) != 1:
        raise AssertionError("entry must be exactly one word")
    text.encode("utf-8")  # must be valid UTF-8


def main() -> int:
    gate_check(WORD)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(WORD)
    # Read it back and re-check the bytes on disk, so a write failure
    # or an encoding surprise is caught here, not by the grader.
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != WORD:
        raise AssertionError(f"wrote {written!r}, expected {WORD!r}")
    gate_check(written)
    print(f"wrote {out_path}: {WORD!r} ({len(WORD)} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
