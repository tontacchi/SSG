from enum import Enum

class TextType(Enum):
    NORMAL_TEXT = "normal"
    BOLD_TEXT   = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT   = "code"
    LINK_TEXT   = "link"
    IMAGE_TEXT  = "image"

class TextNode:
    def __init__(self,
        text: str="",
        text_type: TextType=TextType.NORMAL_TEXT,
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
        if self.url != self.url:
            return False

        return True
    
    def __repr__(self) -> str:
        repr_str = f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return repr_str

