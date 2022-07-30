from textual.app import App
from textual.widgets import Header, Footer, FileClick, ScrollView, DirectoryTree
from rich.panel import Panel
from rich.table import Table
from rich.style import StyleType

class CustomHeader(Header):
    def __init__(
        self, *, tall: bool = True, style: StyleType = "white",
        clock: bool = True,) -> None:
        super().__init__()
        self.tall = tall
        self.style = style
    def render(self):
        header_table = Table.grid(padding=(0, 1), expand=True)
        header_table.style = self.style
        header_table.add_column("title", justify="center", ratio=1)
        header_table.add_row(
            self.full_title
        )
        header: RenderableType
        header = Panel(header_table, style=self.style) if self.tall else header_table
        return header

class MyApp(App):
    async def on_load(self) -> None:
        await self.bind("q", "quit", "Quit")

    async def on_mount(self) -> None:
        await self.view.dock(CustomHeader(), edge="top")

MyApp.run(title='Chat')
