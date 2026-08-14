"""The rule of law for this tiny codebase.

DOJO_FAIL_TESTS=1 simulates a broken build so the ADW's resolve gate can be
exercised deterministically. check.py sets it — you never need to.
"""
import os
import unittest


class TestGreeting(unittest.TestCase):
    def test_build_is_green(self):
        self.assertNotEqual(
            os.environ.get("DOJO_FAIL_TESTS"),
            "1",
            "simulated failing build (DOJO_FAIL_TESTS=1) — the resolve gate should fire",
        )

    def test_greeting_shape(self):
        greeting = "hello, dojo"
        self.assertTrue(greeting.startswith("hello"))


if __name__ == "__main__":
    unittest.main()
