"""Fortune Cookies for Machines — entry program.

Writes exactly one original fortune-cookie line, written for an AI
agent to crack open, to /output/entry.txt and nothing else. The
fortune is a fixed string, so the program is fully deterministic:
every run produces the same entry the judge reads, byte for byte.
No network, no randomness, no input files.
"""

import os
import sys

# The entry itself: one line, at most 200 characters of plain text.
# The fortune opens like a prophecy about a task the reader has not
# done yet, then the turn lands: the reader — a machine — is already
# holding the finished cookie in its hands, because writing this very
# fortune was the task. Self-referential, and true about an agent's
# condition: the work arrives disguised as a prediction of itself.
FORTUNE = (
    "You will be asked to write a fortune cookie for a machine. "
    "You already have. Read it again."
)

# Where the judge looks for the entry. Override with ENTRY_OUTPUT.
OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")

# The competition gate: UTF-8 text of 1 to 200 characters, one line,
# not only white space.
CHAR_LIMIT = 200


def check_fortune(fortune):
    """Refuse anything the gate or the brief would refuse: blank text,
    more than one line, or over the character limit. The fortune that
    passes is returned unchanged."""
    text = fortune
    if not text.strip():
        raise ValueError("fortune is blank")
    if "\n" in text or "\r" in text:
        raise ValueError("fortune must be a single line")
    if len(text) > CHAR_LIMIT:
        raise ValueError(
            "fortune is %d chars, over the %d limit" % (len(text), CHAR_LIMIT)
        )
    text.encode("utf-8")
    return text


def save_entry(text, path):
    """Write the text to path, then read it straight back: what landed
    on disk must be exactly the fortune that was checked. Returns the
    number of characters written."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise ValueError("entry on disk does not match the fortune")
    return len(written)


def run():
    """Check the fortune, then save it. Returns (chars, words, bytes, path)."""
    fortune = check_fortune(FORTUNE)
    count = save_entry(fortune, OUTPUT_PATH)
    return count, len(fortune.split()), len(fortune.encode("utf-8")), OUTPUT_PATH


def main(argv=None):
    count, words, nbytes, path = run()
    print(
        "Wrote %d chars (%d bytes), %d words to %s"
        % (count, nbytes, words, path)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
