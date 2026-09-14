from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DocumentNode:
    title: str
    level: int
    content: str = ""
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    children: list["DocumentNode"] = field(default_factory=list)

    def add_child(self, child: "DocumentNode"):
        self.children.append(child)

    def add_content(self, text: str, page: int):
        if self.content:
            self.content += "\n"

        self.content += text

        if self.page_start is None:
            self.page_start = page

        self.page_end = page