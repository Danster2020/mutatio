import sys
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Button, Input, Label, Header, Footer, Rule
from textual.containers import Horizontal, Vertical, HorizontalGroup, Right, Center, VerticalScroll
from rich.text import Text

#from version import __version__
from controller import Controller
from store import Store

class MyApp(App):
    CSS = """    
    HorizontalGroup {
        height: 6;
    }
    .small-btn {
        border: none;
    }
    DataTable {
        overflow: scroll;
    }
    """

    def __init__(self):
        super().__init__()
        self.store = Store()
        self.controller = Controller(self.store)
        self.store.subscribe(self.update_file_names_table)

    def compose(self) -> ComposeResult:
        with Right():
            yield Button("Quit", id="quit_button", classes="small-btn")
        with Center():
            yield Label("", id="log_label")
        yield Label("Folder Path")
        yield Input(placeholder="/etc/...", id="folder_path")
        yield Button("Load", id="load_files_button")
        yield Rule(line_style="heavy")

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
        yield Rule(line_style="heavy")

        yield Label("Files")
        with VerticalScroll():
            yield DataTable()
        yield Button("Export", id="export_names_button")
        yield Footer()

    def on_mount(self) -> None:
        # self.title = f"Mutatio v{__version__}"
        table = self.query_one(DataTable)
        table.add_columns("Current name", "New name")

    def write_to_log(self, text: str):
        self.query_one("#log_label").update(text)

    def update_file_names_table(self):
        table = self.query_one(DataTable)
        table.clear()
        for org, new in zip(self.store.org_file_names, self.store.new_file_names):
            new_name = new
            if org != new:
                new_name = Text(new, style="yellow")
            table.add_row(org, new_name)

    @on(Button.Pressed, "#quit_button")
    def quit_button_action(self):
        sys.exit()

    @on(Button.Pressed, "#load_files_button")
    def load_files_action(self):
        path = self.query_one("#folder_path").value
        if self.controller.load_files(path):
            self.write_to_log("File names loaded.")
        else:
            self.write_to_log("Could not find path!")

    @on(Button.Pressed, "#filter_button")
    def update_table_data(self):
        pattern = self.query_one("#selection_regex").value
        replacement = self.query_one("#replacement_text").value
        self.controller.apply_filter(pattern, replacement)

    @on(Button.Pressed, "#reset_button")
    def reset_file_names(self):
        self.controller.reset_names()

    @on(Button.Pressed, "#export_names_button")
    def export_names_action(self):
        self.controller.export_file_names()
        self.write_to_log("Files have been renamed!")
