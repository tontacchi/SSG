from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self,
        tag: str,
        children: list["HTMLNode"],
        props: dict[str, str] | None=None
    ) -> None:
        super().__init__(tag=tag, children=children, props=props)

        return

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Error: Parent node must have a tag")

        if not self.children:
            raise ValueError("Error: Parent Node must have children nodes")

        res = f"<{self.tag}{self.props_to_html()}>"
        
        for child in self.children:
            res += f"{child.to_html()}"
        
        res += f"</{self.tag}>"

        return res
