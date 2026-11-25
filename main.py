#!/usr/bin/env python3
"""Pigeon Pitch, One Line — make.fun entry.

Writes the one-line elevator pitch a city pigeon gives investors for
its courier startup to /output/entry.txt (falling back to ./output/
relative to the current directory when /output is not writable).

The pitch is assembled from parts so every word earns its place, then
validated (one line, 1-200 characters) before being written.

Deterministic by construction: no randomness, no clock, no network, no
input — every run writes byte-identical output.
"""

import os
import sys

MAX_CHARS = 200

# The pitch, built from parts: the ask, the joke, the proof, the closer.
HOOK = "Invest in my courier startup:"
JOKE = "our burn rate is literally breadcrumbs,"
PROOF = "our fleet flies over every traffic jam,"
HISTORY = "and after two world wars we're still delivering"
CLOSER = "— the seed round is literally seeds."


def build_pitch() -> str:
    """Assemble the single-line pitch from its parts."""
    parts = [HOOK, JOKE, PROOF, HISTORY, CLOSER]
    return " ".join(parts)


def choose_output_path() -> str:
    """Prefer /output/entry.txt; fall back to ./output/entry.txt."""
    preferred = "/output/entry.txt"
    try:
        os.makedirs("/output", exist_ok=True)
        probe = open(preferred, "a", encoding="utf-8")
        probe.close()
        return preferred
    except OSError:
        # /output is not writable here (e.g. local run); use ./output/.
        return os.path.join(os.getcwd(), "output", "entry.txt")


def main() -> int:
    pitch = build_pitch()

    if not pitch.strip():
        print("error: pitch is empty", file=sys.stderr)
        return 1
    if "\n" in pitch or "\r" in pitch:
        print("error: pitch must be a single line", file=sys.stderr)
        return 1
    if len(pitch) > MAX_CHARS:
        print(
            f"error: pitch is {len(pitch)} characters, over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1

    path = choose_output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(pitch)

    # Read it back and confirm what landed on disk.
    with open(path, encoding="utf-8") as f:
        written = f.read()
    assert written == pitch, "round-trip mismatch"
    print(f"Wrote {len(written)} characters to {path}:")
    print(written)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
