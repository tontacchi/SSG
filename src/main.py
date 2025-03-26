#---[ Global Imports ]----------------------------------------------------------
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode

#---[ Global Imports ]----------------------------------------------------------


#---[ Main Function ]-----------------------------------------------------------
def main():
    test = TextNode("hi **bold****two** words")

    res = split_nodes_delimiter([ test ], "**", TextType.BOLD)

    return

#---[ Main Function ]-----------------------------------------------------------

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("TextNode to HTMLNode Error: invalid TextType given")

def split_nodes_delimiter(
    node_list: list[TextNode],
    delimiter: str,
    text_type: TextType
) -> list[TextNode]:
    # valid delimiters & text types only
    type_delimiter_map = {
        TextType.BOLD: "**",
        TextType.ITALIC: "_",
        TextType.CODE: "`"
    }

    # guard against faulty input
    if text_type not in type_delimiter_map:
        raise Exception("Split Nodes: invalid text type")
    elif type_delimiter_map[text_type] != delimiter:
        raise Exception(f"Split Nodes: invalid delimiter paired with {text_type}")

    for node in node_list:
        delim_indexes = []
        walk = 0

        location = node.text.find(delimiter, walk)

        while location != -1:
            delim_indexes.append(location)
            walk = location + len(delimiter)

            location = node.text.find(delimiter, walk)

        print(delim_indexes)


    return []

#---[ Entry ]-------------------------------------------------------------------
if __name__ == "__main__":
    main()

#---[ Entry ]-------------------------------------------------------------------
