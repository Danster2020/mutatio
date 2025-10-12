# import unittest
# import tempfile
# import os
# from main import MyApp

# class TestFileOperations(unittest.TestCase):
    # TODO
    # def test_load_files(self):
    #     async def run_test(app):
    #         with tempfile.TemporaryDirectory() as tmpdir:
    #             original_files = ["a.txt", "b.txt"]
    #             app.load_files(tmpdir)
                
    #             app.load_files("/non/existing/folder")
    #     MyApp.run_test(run_test)

    # def test_export_file_names(self):
    #     async def run_test(app):
    #         with tempfile.TemporaryDirectory() as tmpdir:
    #             original_files = ["a.txt", "b.txt"]
    #             for f in original_files:
    #                 open(os.path.join(tmpdir, f), "w").close()

    #             app.load_files(tmpdir)
    #             app.new_file_names = ["x.txt", "y.txt"]
    #             app.export_file_names()

    #             # assert changes happened
    #             final_files = set(os.listdir(tmpdir))
    #             assert final_files == {"x.txt", "y.txt"}

    #             # assert log was updated
    #             log_label = app.query_one("#log_label")
    #             assert log_label.renderable == "Files have been renamed!"

    #     MyApp.run_test(run_test)


