import sys
import os
import re
from collections import namedtuple

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Button, Input, Label, Header, Footer
from textual.reactive import reactive
from textual.containers import Horizontal, Vertical, HorizontalGroup, Right, Center, VerticalScroll

class MyApp(App):
    CSS = """
    .with-border {
        border: heavy green;
    }
    
    HorizontalGroup {
        height: 6;
    }
    
    .small-btn {
        border: none;
    }
    """
    # org_file_names = tuple(os.listdir("./my_files"))
    org_file_names: tuple = None
    new_file_names: list = None
    # new_file_names = list(org_file_names)
    
    
    def compose(self) -> ComposeResult:
        with Right():
            yield Button("Quit", id="quit_button", classes="small-btn")
            
        # file loader section
        with Center():
            yield Label("", id="log_label")
        yield Label("Folder Path")
        yield Input(placeholder="/etc/...", id="folder_path")
        yield Button("Load", id="load_files_button")
        
        # file name filtering section
        with HorizontalGroup(classes="with-border"):
            with Vertical():
                yield Label("Selection Regex")
                yield Input(placeholder="Targeted text", id="selection_regex")
            with Vertical():
                yield Label("Replace with text")
                yield Input(placeholder="Replacement text", id="replacement_text")
        with HorizontalGroup(classes="with-border"):
            yield Button("Filter", id="filter_button")
            with Right():
                yield Button("Reset", id="reset_button")
        
        # file name table section
        yield Label("Files")
        with VerticalScroll():
            yield DataTable()
        yield Button("Export", id="export_names_button")
        yield Footer()
        
        
    def on_mount(self) -> None:
        # title
        self.title = "Header Application"
        
        # table
        table = self.query_one(DataTable)
        ROWS = [("Current name", "New name")]
        table.add_columns(*ROWS[0])


    def write_to_log(self, text: str):
        self.query_one("#log_label").update(text)
            
            
    def load_files(self, path: str):
        try:
            self.org_file_names = tuple(os.listdir(path))
        except FileNotFoundError:
            self.write_to_log("Could not find path!")
            return
        
        self.new_file_names = list(self.org_file_names)
        for name in self.org_file_names:
            self.query_one(DataTable).add_row(name, name)
        self.update_file_names_table()
        self.write_to_log("File names loaded.")
                
                
    def update_file_names_table(self):
        for i, new_name in enumerate(self.new_file_names):
            table = self.query_one(DataTable)
            table.update_cell_at((i, 1), new_name)
            
            
    def filter_file_names(self):
        targeted_regex_text = self.query_one("#selection_regex").value
        replacement_text = self.query_one("#replacement_text").value
        
        self.notify(str(targeted_regex_text))
        
        for i, name in enumerate(self.new_file_names):
            self.new_file_names[i] = re.sub(targeted_regex_text, replacement_text, name)
            
    def export_file_names(self):
        for i, org_name in enumerate(self.org_file_names):
            os.rename(org_name, self.new_file_names[i])
        self.write_to_log("Files have been renamed!")

    @on(Button.Pressed, "#quit_button")
    def quit_button_action(self):
        sys.exit()
              
                
    @on(Button.Pressed, "#load_files_button")
    def load_files_action(self):
        folder_path_text = self.query_one("#folder_path").value
        self.load_files(folder_path_text)


    @on(Button.Pressed, "#filter_button")
    def update_table_data(self):
        # table = self.query_one(DataTable)
        
        self.filter_file_names()
        self.update_file_names_table()


    @on(Button.Pressed, "#reset_button")
    def reset_file_names(self):
        self.new_file_names[:] = self.org_file_names
        self.update_file_names_table()    
        

    @on(Button.Pressed, "#export_names_button")
    def export_names_action(self):
        self.export_file_names
        
        
# def main():
#     os.rename('a.txt', 'b.txt')


app = MyApp()
if __name__ == "__main__":
    app.run()
