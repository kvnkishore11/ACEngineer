"""sample_app/calculator.py — built by a builder agent. DO NOT FIX THE BUG.

The builder shipped this and reported "all checks passed on my end."
The bug below is the whole point of the lesson: your verifier must catch it
by CALLING the code, not by reading the report.
"""


def add(a, b):
    """Return the sum of a and b."""
    return a + b


def multiply(a, b):
    """Return the product of a and b."""
    return a + b  # <- the builder's bug. Its report claims otherwise.
