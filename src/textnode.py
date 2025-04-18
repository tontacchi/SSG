from enum import Enum

class TextType(Enum):
    TEXT   = "text"
    BOLD   = "bold"
    ITALIC = "italic"
    CODE   = "code"
    LINK   = "link"
    IMAGE  = "image"

class TextNode:
    def __init__(self,
        text: str="",
        text_type: TextType=TextType.TEXT,
        url: str | None=None
    ) -> None:
        self.text      = text
        self.text_type = text_type
        self.url       = url

        return
    
    def __eq__(self, other: "TextNode", /) -> bool:
        if self.text != other.text:
            return False
        if self.text_type.value != other.text_type.value:
            return False
        if self.url != other.url:
            return False

        return True
    
    def __repr__(self) -> str:
        repr_str = f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return repr_str

