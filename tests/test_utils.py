# test_utils.py
import unittest
from unittest.mock import MagicMock
from utils.utils import mark_item, display_marked_items, bookmark_item, display_bookmarked_items, marked_items, bookmarked_items

class TestUtilsModule(unittest.TestCase):

    def test_mark_item(self):
        path = "src"
        mark_item(path)
        self.assertTrue(marked_items[path])
        mark_item(path)
        self.assertFalse(marked_items[path])

    def test_bookmark_item(self):
        path = "src"
        bookmark_item(path)
        self.assertIn(path, bookmarked_items)
        bookmark_item(path)
        self.assertEqual(bookmarked_items.count(path), 1)

if __name__ == "__main__":
    unittest.main()
