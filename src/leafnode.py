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
        
        res = self.value

        # 1. value
        # 2. <tag>value</tag>
        # 3. <tag props>value</tag>
        if self.tag:
            res = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

        return res

