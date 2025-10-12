import unittest
import tempfile
import os
from controller import Controller
from store import Store


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.store = Store()
        self.controller = Controller(self.store)

    # helper function
    def make_temp_dir_with_files(self, file_names: list[str]):
        """Helper: creates directory with files to test"""
        tmp_dir = tempfile.TemporaryDirectory()
        for f in file_names:
            open(os.path.join(tmp_dir.name, f), "w").close()
        return tmp_dir, tmp_dir.name

    def test_files_should_load(self) -> None:
        """checks that files can be loaded from disk"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            # creates two test files in a temp directory
            file_names = ["b.txt", "a.txt"]
            for f in file_names:
                open(os.path.join(tmp_dir, f), "w").close()

            could_files_load = self.controller.load_files(tmp_dir)

            self.assertTrue(could_files_load)
            self.assertEqual(self.store.org_file_names, tuple(file_names))
            self.assertEqual(tuple(self.store.new_file_names), tuple(file_names))

    def test_files_should_not_load(self) -> None:
        """checks that non existing directory doesn't load"""
        non_existent_dir = "this/path/does/not/exist"
        could_files_load = self.controller.load_files(non_existent_dir)

        self.assertFalse(could_files_load)

    def test_text_should_be_filtered(self):
        """checks that text gets filtered correctly"""
        unfiltered_file_names = ["My other test_file 1234.JPG", "My test_file 1234.txt"]
        filtered_file_names = []

        filter_pattern = ".txt"
        filter_replacement = ".MP4"
        for name in unfiltered_file_names:
            filtered_file_names.append(
                self.controller.filter_text(filter_pattern, filter_replacement, name)
            )

        self.assertEqual(unfiltered_file_names[0], filtered_file_names[0])
        self.assertEqual("My test_file 1234.MP4", filtered_file_names[1])

    def test_should_export_new_file_names(self):
        """checks that renamed files are exported correctly"""
        tmp_dir, tmp_dir_name = self.make_temp_dir_with_files(
            ["abc 123 456.txt", "123 test.pdf"]
        )
        self.controller.load_files(tmp_dir_name)
        self.controller.apply_filter(" ", "_")
        self.controller.export_file_names()

        exported_names = os.listdir(tmp_dir_name)
        self.assertEqual("abc_123_456.txt", exported_names[0])
        self.assertEqual("123_test.pdf", exported_names[1])

        tmp_dir.cleanup()
