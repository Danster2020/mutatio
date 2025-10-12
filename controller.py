import os, re
from store import Store

class Controller:
    def __init__(self, store: Store):
        self.store = store

    def load_files(self, path: str):
        try:
            names = tuple(os.listdir(path))
            self.store.set_import_folder(path)
            self.store.set_files(names)
            return True
        except FileNotFoundError:
            return False
        
    def filter_text(self, pattern: str, replacement: str, text: str):
        filtered_text = re.sub(pattern, replacement, text)
        return filtered_text

    def apply_filter(self, pattern: str, replacement: str):
        for i, name in enumerate(self.store.new_file_names):
            new_name = self.filter_text(pattern, replacement, name)
            self.store.update_file_name(i, new_name)

    def reset_names(self):
        self.store.reset_file_names()

    def export_file_names(self):
        folder = self.store.folder_path
        for i, org_name in enumerate(self.store.org_file_names):
            org_file_name_full_path = folder + "/" + org_name
            new_file_name_full_path = folder + \
                "/" + self.store.new_file_names[i]
            os.rename(org_file_name_full_path, new_file_name_full_path)
        #self.write_to_log("Files have been renamed!")
