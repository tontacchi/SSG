#---[ Global Imports ]----------------------------------------------------------
import re

# nodes
from   textnode import TextNode
from   htmlnode import HTMLNode
from   leafnode import LeafNode
from   parentnode import ParentNode

# node types
from   textnode import TextType
from   block    import BlockType

#---[ Global Imports ]----------------------------------------------------------

def extract_title(markdown: str) -> str:
    if not markdown: raise ValueError("empty markdown")

    title = ""

    first_line = markdown.split('\n')[0]
    if first_line[0] != "#":
        raise ValueError("markdown does not begin with a heading #")
    
    index = 0
    while first_line[index] == "#":
        index += 1

    if first_line[index + 1:] == title:
        raise ValueError("empty heading")

    return first_line[index + 1:]

#---[ str, TextNode, HTMLNode Conversion ]--------------------------------------
def text_to_text_nodes(text: str) -> list[TextNode]:
    '''
    Splits inline markdown into text, bold, italic, and code TextNodes
    '''
    type_delimiter_map = {
        TextType.BOLD: "**",
        TextType.ITALIC: "_",
        TextType.CODE: "`"
    }

    node = TextNode(text)
    node_list = [node]

    prev_list = []

    while prev_list != node_list:
        if prev_list == node_list: break
        prev_list = node_list.copy()

        for text_type, delimiter in type_delimiter_map.items():
            node_list = split_nodes_delimiter(node_list, delimiter, text_type)

        node_list = split_nodes_image(node_list)
        node_list = split_nodes_link(node_list)

    return node_list

def text_to_children(text: str) -> list[LeafNode]:
    textnode_list = text_to_text_nodes(text)
    child_node_list = []

    for text_node in textnode_list:
        temp = text_node_to_html_node(text_node)
        child_node_list.append(temp)

    return child_node_list

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    '''
    Converts inline HTML to a LeafNode
    '''
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

def markdown_to_html_node(markdown: str) -> HTMLNode:
    block_list = markdown_to_blocks(markdown)

    children_list = []
    for block in block_list:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                node = block_to_paragraph_html_node(block)
                children_list.append(node)
            case BlockType.HEADING:
                node = block_to_heading_html_node(block)
                children_list.append(node)
            case BlockType.CODE:
                node = block_to_code_html_node(block)
                children_list.append(node)
            case BlockType.QUOTE:
                node = block_to_quote_html_node(block)
                children_list.append(node)
            case BlockType.ORDERED_LIST:
                node = block_to_list_html_node(block, "ol")
                children_list.append(node)
            case BlockType.UNORDERED_LIST:
                node = block_to_list_html_node(block, "ul")
                children_list.append(node)

    root_node = ParentNode("div", children_list)
    return root_node

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    
    # remove surrounding whitespace & filter empty lines
    blocks = [block_str.strip() for block_str in blocks if block_str.strip() != ""]

    return blocks

#---[ str, TextNode, HTMLNode Conversion ]--------------------------------------


#---[ Block str -> HTMLNode Conversion ]----------------------------------------
def block_to_paragraph_html_node(block: str) -> ParentNode | LeafNode:
    block = " ".join(block.split("\n"))

    children_list = text_to_children(block)
    res_node = None

    if not children_list:
        res_node = LeafNode("p", block)
    else:
        res_node = ParentNode("p", children_list)

    return res_node

def block_to_heading_html_node(block: str) -> HTMLNode:
    pound_count = 0

    for i in range(6):
        if block[i] != "#":
            break
        pound_count += 1

    heading_tag_str = f"h{pound_count}"
    heading_text = block[pound_count + 1:]
    # children_list = text_to_text_nodes(heading_text)

    children_list = text_to_children(heading_text)

    heading_node = LeafNode(heading_tag_str, heading_text)
    if len(children_list) > 1:
        heading_node = ParentNode(heading_tag_str, children_list)

    return heading_node

def block_to_code_html_node(block: str) -> ParentNode:
    '''
    Converts a markdown code block to an HTML <pre><code>...</code></pre> node.

    Preconditions:
        - `block` starts and ends with exactly three backticks (```). They are two
          separate groupings.

    Args:
        - `block` (str): markdown code block string. content is wrapped in triple
          backticks

    Postconditions:
        - `ParentNode` returned is always <pre> wrapping `LeafNode` <code>

    Returns:
        - `pre_node` (`ParentNode`): html node <pre> wrapping `LeafNode` <code>
    '''
    res = block[3:-3]

    first_newline = res.find("\n")
    res = res[first_newline+1:]

    node = TextNode(res, TextType.CODE)
    node = text_node_to_html_node(node)

    pre_node = ParentNode("pre", [node])
    return pre_node

# TODO: further parse lines using text -> TextNode -> LeafNode
def block_to_quote_html_node(block: str) -> LeafNode:
    lines = block.split('\n')
    res = [line[2:] for line in lines]
    quote = "\n".join(res)
    
    node = LeafNode("blockquote", quote)

    return node

def block_to_list_html_node(block: str, list_type: str="ul") -> ParentNode | LeafNode:
    """
    Converts a markdown unordered list block into an HTML <ul> node 
    containing <li> elements, with support for bold, italic, and code formatting.

    Preconditions:
        - Each line in `block` must start with "- " (dash followed by space).
        - The block represents a valid unordered list in markdown format.

    Args:
        `block` (str): A markdown string representing an unordered list, where each list item starts on a new line with "- ".

    Postconditions:
        - Returns a `ParentNode` with tag 'ul' containing one <li> child node 
          for each item in the markdown list.
        - Supports nested inline formatting using:
            - `**bold**` for bold
            - `_italic_` for italic
            - `` `code` `` for inline code

    Returns:
        `ParentNode`: An HTML <ul> element where each child is an <li> element
        corresponding to a list item in the markdown block.

    Side Effects:
        None.

    Raises:
        None.
    """
    # removes the "- " at the start of each list element
    lines = block.split('\n')
    
    res = []

    if list_type == "ul":
        res = [line[2:] for line in lines]
    elif list_type == "ol":
        res = [line[3:] for line in lines]

    # collect all of the list element nodes
    item_node_list = []
    for line in res:
        # check for inline elements
        text_node_list = text_to_text_nodes(line)
        text_node = TextNode(line)

        # default to child not having nested elements
        child = LeafNode("li", line)
    
        # list has nested elements
        if text_node_list != [text_node]:
            leaf_node_list = []

            for node in text_node_list:
                if node.text:
                    leaf_node = text_node_to_html_node(node)
                    leaf_node_list.append(leaf_node)
 
            child = ParentNode("li", leaf_node_list)

        # list element node added
        item_node_list.append(child)
 
    # create wrapping <ul> element w/ the <li> leaf & parent nodes
    if list_type in ("ul", "ol"):
        list_node = ParentNode(list_type, item_node_list)
        return list_node

    raise ValueError("Error: list_type is invalid type (only ul and ol supported for now)")

#---[ Block str -> HTMLNode Conversion ]----------------------------------------


#---[ Split TextNodes & extract link str ]--------------------------------------
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

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)

    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)

    return matches

#---[ Split TextNodes & extract link str ]--------------------------------------


#---[ Block str Type Checking ]-------------------------------------------------
def block_to_block_type(markdown_block: str) -> BlockType:
    '''
    - precondition: whitespace stripped from markdown_block
    '''
    res = BlockType.PARAGRAPH

    lines = markdown_block.split('\n')
    if check_block_is_heading(lines):
        res = BlockType.HEADING
    elif check_block_is_code(lines):
        res = BlockType.CODE
    elif check_block_is_quote(lines):
        res = BlockType.QUOTE
    elif check_block_is_unordered_list(lines):
        res = BlockType.UNORDERED_LIST
    elif check_block_is_ordered_list(lines):
        res = BlockType.ORDERED_LIST

    return res

def check_block_is_heading(lines: list[str]) -> bool:
    import re
    if len(lines) != 1: return False

    pattern = r"(#{1,6}) ([^\s].*)"
    return re.match(pattern, lines[0]) is not None

def check_block_is_code(lines: list[str]) -> bool:
    # check total length is at least 6
    total_length = 0

    for line in lines:
        total_length += len(line)

    if total_length < 6:
        return False

    # check ends are both triple back ticks
    return lines[0].startswith(r"```") and lines[-1].endswith(r"```") 

def check_block_is_quote(lines: list[str]) -> bool:
    for line in lines:
        if not line.startswith(">"):
            return False

    return True

def check_block_is_unordered_list(lines: list[str]) -> bool:
    for line in lines:
        if not line.startswith("- "):
            return False

    return True

def check_block_is_ordered_list(lines: list[str]) -> bool:
    count = 1

    for line in lines:
        if not line.startswith(f"{count}. "):
            return False
        count += 1

    return True

#---[ Block str Type Checking ]-------------------------------------------------
