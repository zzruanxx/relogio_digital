import unittest
from ascii_art import build_ascii, render, colorize
from validation import validate_time, to_12h
from cli import get_display_string

class TestClock(unittest.TestCase):
    def test_validate_time_valid(self):
        self.assertTrue(validate_time("00:00"))
        self.assertTrue(validate_time("23:59"))
        self.assertTrue(validate_time("12:30"))

    def test_validate_time_invalid(self):
        self.assertFalse(validate_time("24:00"))
        self.assertFalse(validate_time("12:60"))
        self.assertFalse(validate_time("12"))
        self.assertFalse(validate_time("12:30:45"))
        self.assertFalse(validate_time("ab:cd"))

    def test_to_12h(self):
        self.assertEqual(to_12h(0, 0), "12:00 AM")
        self.assertEqual(to_12h(12, 0), "12:00 PM")
        self.assertEqual(to_12h(13, 30), "01:30 PM")
        self.assertEqual(to_12h(23, 59), "11:59 PM")

    def test_build_ascii(self):
        result = build_ascii("12:34")
        self.assertIn("__", result)
        self.assertIn("|", result)
        self.assertEqual(len(result.split("\n")), 3)

    def test_build_ascii_scale(self):
        result1 = build_ascii("12", scale=1)
        result2 = build_ascii("12", scale=2)
        self.assertGreater(len(result2), len(result1))

    def test_colorize(self):
        result = colorize("test", "red")
        self.assertIn("\033[31m", result)
        self.assertIn("\033[0m", result)

    def test_render(self):
        result = render("12:34")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result.split("\n")), 3)
        # Verificar se tem representação de : (bullet character)
        self.assertIn(" ● ", result)

    def test_get_display_string_24h(self):
        result = get_display_string("14:30", ampm=False, scale=1, color=None)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result.split("\n")), 3)  # Apenas arte ASCII

    def test_get_display_string_12h(self):
        result = get_display_string("14:30", ampm=True, scale=1, color=None)
        self.assertIsInstance(result, str)
        lines = result.split("\n")
        self.assertEqual(len(lines), 4)  # Arte + PM
        self.assertIn("PM", result)

if __name__ == "__main__":
    unittest.main()