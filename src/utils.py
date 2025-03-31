#---[ Global Imports ]----------------------------------------------------------
from   textnode import TextNode, TextType
from   htmlnode import HTMLNode
from   leafnode import LeafNode

import re

#---[ Global Imports ]----------------------------------------------------------

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
    assert text_type in type_delimiter_map
    assert type_delimiter_map[text_type] == delimiter

    res = []

    for node in node_list:
        # skip non-text nodes
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue

        string = node.text
        num_delimiters = 0

        # only create nodes if at least 2 delimiters exist
        location = 0
        while string.find(delimiter, location) != -1:
            location = string.find(delimiter, location) + len(delimiter)
            num_delimiters += 1

        split_res = []
        if num_delimiters >= 2:
            split_res = string.split(delimiter, 2)

        if len(split_res) > 2:
            node_left = None
            if split_res[0]:
                node_left = TextNode(split_res[0])
            node_right = None
            if split_res[0]:
                node_right = TextNode(split_res[2])
            node_middle = TextNode(split_res[1], text_type)

            if node_left:
                res.append(node_left)
            res.append(node_middle)
            if node_right:
                res.append(node_right)
        else:
            res.append(node)

    return res

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)

    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)

    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        link_pairs = extract_markdown_images(node.text)

        # no match: extract() returns empty list
        if not link_pairs:
            new_nodes.append(node)
            continue

        # match: create left TextNode, image node, & right TextNode
        text_node_start = 0

        for text, link in link_pairs:
            # get start & end indices of link
            reconstructed_link = f"![{text}]({link})"

            left = node.text.find(reconstructed_link)
            right = left + len(reconstructed_link)

            # create text node before
            if text_node_start != left:
                text_string = node.text[text_node_start:left]
                new_text_node = TextNode(text_string)
                new_nodes.append(new_text_node)

            # create image node
            new_image_node = TextNode(text, TextType.IMAGE, link)
            new_nodes.append(new_image_node)

            # set next text starting index
            text_node_start = right

        # create possible last text node
        if text_node_start < len(node.text):
            new_text_node = TextNode(node.text[text_node_start:])
            new_nodes.append(new_text_node)

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        link_pairs = extract_markdown_links(node.text)

        # no match: extract() returns empty list
        if not link_pairs:
            new_nodes.append(node)
            continue

        # match: create left TextNode, image node, & right TextNode
        text_node_start = 0

        for text, link in link_pairs:
            # get start & end indices of link
            reconstructed_link = f"[{text}]({link})"

            left = node.text.find(reconstructed_link)
            right = left + len(reconstructed_link)

            # create text node before
            if text_node_start != left:
                text_string = node.text[text_node_start:left]
                new_text_node = TextNode(text_string)
                new_nodes.append(new_text_node)

            # create image node
            new_image_node = TextNode(text, TextType.LINK, link)
            new_nodes.append(new_image_node)

            # set next text starting index
            text_node_start = right

        # create possible last text node
        if text_node_start < len(node.text):
            new_text_node = TextNode(node.text[text_node_start:])
            new_nodes.append(new_text_node)

    return new_nodes

def test():
    # test1 = TextNode("image ![middle image](https)middle")
    # test2 = TextNode("![starting image](https) image start")
    # test3 = TextNode("image end ![starting image](https)")
    # test4 = TextNode("here is a kitty: ![kitty placeholder](https://cat-image.com), and another one: ![some cat](https://hotmail.com)b")
    # test5 = TextNode("![raw image](byitself)")
    node = TextNode(
        "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])

    for node in new_nodes:
        print(node)

    return

if __name__ == "__main__":
    test()

