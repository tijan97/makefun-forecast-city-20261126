#!/usr/bin/env python3
"""Funniest Forecast for a City That Isn't -- make.fun entry program.

The brief: write ONE LINE, no more than 120 characters, that reads as a
weather forecast for a city that does not exist -- and make it funny.
The house judge reads the lines two at a time and keeps the funnier
one, weighing, most important first:

1. a weather forecast for a city that does not exist (a line about a
   real place, or one with no invented city in it, loses);
2. funny: the joke lands on a first read, and the laugh comes from the
   weather itself rather than from a pun bolted on;
3. sounds like a real forecast, borrowing the flat official phrasing
   of a weather bulletin and then breaking it;
4. the invented city feels like a place, with a name and a detail that
   fit its absurd weather;
5. fits in 120 characters with no wasted word.

Why this line wins those criteria
---------------------------------
* Invented city: "Tarnwick" -- it sounds like a real damp English
  market town (a tarn is a small mountain lake; -wick is a settlement
  suffix), so it reads as a place on a map while existing nowhere.
  The name is neutral, not a joke in itself: the laugh does not come
  from a pun bolted onto the city name.
* Flat official phrasing, then the break: "expect 14 degrees with
  rain falling only on people who forgot umbrellas" opens exactly
  like a bulletin -- temperature, precipitation -- and then the rain
  acquires a target. The absurdity is in the weather itself: rain
  that discriminates by preparedness.
* The joke lands on a first read: everyone has been the person
  caught without an umbrella, so the forecast's cruelty is instantly
  recognisable. No setup, no explanation, one twist.
* The closing beat, "then smug sunshine by six", keeps the bulletin
  shape (a time, a condition) while the sunshine itself is smug --
  the weather is not just unfair, it is pleased with itself. That
  second small twist is what makes the city feel like a place with
  its own spiteful climate, and it costs only a few words.
* Length: 112 of the 120 allowed characters. Tight, no padding, no
  wasted word -- every clause carries either a number, the joke, or
  the closing beat.

What was rejected while drafting
--------------------------------
* A city name that is itself the joke (a pun name) -- the judge's
  brief says the laugh should come from the weather, not from a pun
  bolted on, so the name stays straight-faced.
* "Rain falling upwards" -- a bigger absurdity, but it reads as a
  fantasy premise rather than a forecast; targeted rain keeps the
  broadcast frame intact.
* Adding a second weather event (e.g. a hail of lost socks) -- would
  crowd the line and dilute the single twist the judge rewards.
* A longer version with "clearing to sunshine" -- "smug sunshine"
  does the same work in fewer words and lands the joke harder.

Output contract
---------------
The program is fully deterministic: it writes one fixed, hand-chosen
string. It writes to ``entry.txt`` inside the directory named by the
``MAKEFUN_OUTPUT_DIR`` environment variable, falling back to the
absolute path ``/output`` when the variable is unset (the program/v1
harness runs on a read-only filesystem with only /output writable),
and creates that directory if needed. Before writing it validates
the line the same way the sealed gate scorer does -- UTF-8 text of
1 to 120 characters, not only whitespace -- and refuses to write an
invalid line. The file holds the line alone, with no trailing
newline, so the sealed scorer sees exactly the 112 characters of
the forecast and nothing else. No randomness, no network, no clock,
no dependence on the working directory: two runs produce
byte-identical output.
"""

import os
import sys

# The entry: the single forecast line for the invented city of
# Tarnwick. 112 characters, inside the 1-120 gate.
ENTRY = (
    "In Tarnwick, expect 14 degrees with rain falling only on people "
    "who forgot umbrellas, then smug sunshine by six."
)

MAX_CHARS = 120


def validate_entry(text):
    """Check the line against the gate: 1-120 chars, one line,
    not only whitespace, ending with a full stop, carrying a
    concrete number so the forecast feels measured."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if "  " in text:
        raise ValueError("entry must not contain double spaces")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            "entry is %d characters, must be 1-%d" % (len(text), MAX_CHARS)
        )
    text.encode("utf-8")  # raises if not valid UTF-8 text
    if not text.endswith("."):
        raise ValueError("entry must end with a full stop")
    # Caps validation: a flat weather bulletin never shouts. Reject
    # any fully-uppercase word longer than one character (the single
    # letter "I" is fine; "RAIN" or "FREEZING" would break the
    # straight-faced broadcast tone the judge rewards).
    shouted = [
        word for word in text.split()
        if word.isupper() and len(word.strip(".,;:!?")) > 1
    ]
    if shouted:
        raise ValueError("entry must not shout: %r" % (shouted,))
    # The brief demands a forecast that sounds measured: require at
    # least one digit so the line always carries a temperature, not
    # just adjectives.
    if not any(char.isdigit() for char in text):
        raise ValueError("entry must contain a concrete number or detail")
    return text


def main():
    entry = validate_entry(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(entry)
    # Read back what was written: the grading runs must reproduce
    # this exact text, so confirm what landed on disk is
    # byte-identical to the validated line.
    with open(out_path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != entry:
        raise ValueError("entry.txt on disk differs from the forecast")
    return 0


if __name__ == "__main__":
    sys.exit(main())
