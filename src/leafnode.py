from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None=None
    ) -> None:
        super().__init__(tag=tag, value=value, props=props)

        return

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("Error: All leaf nodes must have a value")
        
        # case 1: no tag
        # 1. value
        res = self.value

        # case 2: everything besides img
        # 2. <tag>value</tag>
        # 3. <tag props>value</tag>
        if self.tag and self.tag != "img":
            res = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

        # case 3: img is self closing
        # 4. <img props />
        if self.tag and self.tag == "img":
            res = f"<img{self.props_to_html()} />"

        return res

