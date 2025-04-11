class HTMLNode:
    def __init__(self,
        tag: str | None=None,
        value: str | None=None,
        children: list["HTMLNode"] | None=None,
        props: dict[str, str] | None=None
    ) -> None:
        self.tag      = tag
        self.value    = value
        self.children = children
        self.props    = props

        return

    def to_html(self) -> str:
        # child classes must override this method to render as HTML
        raise NotImplementedError

    def props_to_html(self) -> str:
        '''
        this method generates the string for the props inside the opening tag
        - it even does the starting space for you!
        '''
        if not self.props: return ""

        res = ""
        for attr, value in self.props.items():
            res += f" {attr}=\"{value}\""

        return res

    def __repr__(self) -> str:
        res = "HTMLNode(\n"
        res += f"    tag: {self.tag}\n"
        res += f"    value: {self.value}\n"
        res += f"    children: {self.children}\n"
        res += f"    props: {self.props}\n"
        res += ")"

        return res
