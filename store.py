from typing import List, Callable

class Store:
    def __init__(self):
        self.folder_path: str = ""
        self.org_file_names: tuple[str] = ()
        self.new_file_names: list[str] = []
        self._subscribers: list[Callable] = []

    def subscribe(self, callback: Callable):
        self._subscribers.append(callback)

    def _notify(self):
        for subscriber in self._subscribers:
            subscriber()
            
    def set_import_folder(self, folder_path: str):
        self.folder_path = folder_path
        self._notify()

    def set_files(self, file_names: tuple[str]):
        self.org_file_names = file_names
        self.new_file_names = list(file_names)
        self._notify()

    def update_file_name(self, index: int, new_name: str):
        self.new_file_names[index] = new_name
        self._notify()

    def reset_file_names(self):
        self.new_file_names = list(self.org_file_names)
        self._notify()
