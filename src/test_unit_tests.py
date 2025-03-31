#---[ Imports ]-----------------------------------------------------------------
import unittest

from   textnode   import TextNode, TextType
from   htmlnode   import HTMLNode
from   leafnode   import LeafNode
from   parentnode import ParentNode

from   utils import (
    text_node_to_html_node,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link
)

#---[ Imports ]-----------------------------------------------------------------


class TestHTMLNode(unittest.TestCase):
    def test_prop_to_html(self):
        print("[ test ] HTMLNode prop_to_html()")

        test_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=test_props)
        expected_result = ' href="https://www.google.com" target="_blank"'

        self.assertEqual(node.props_to_html(), expected_result)

        return

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self) -> None:
        print("[ test ] LeafNode to_html() normal flow")

        node0 = LeafNode("p", "Hello, world!")
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node0.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node1.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')

        return

    def test_leaf_img(self) -> None:
        print("[ test ] LeafNode <img> to_html() normal flow")

        sample_props = {
            "src": "https://img-loc.com",
            "alt": "alt text"
        }
        node = LeafNode("img", "unused", sample_props)

        expected_value = '<img src="https://img-loc.com" alt="alt text" />'

        self.assertEqual(node.to_html(), expected_value)

        return

    def test_leaf_raises_value_error(self) -> None:
        print("[ test ] LeafNode to_html() ValueError flow: missing value")

        with self.assertRaises(ValueError) as a:
            node = LeafNode("p", "")
            node.to_html()

            node2 = LeafNode("b", None)
            node2.to_html()

        return

class TestParentNode(unittest.TestCase):
    def test_parent_missing_tag(self) -> None:
        print("[ test ] ParentNode missing tag -> ValueError raised")

        with self.assertRaises(ValueError):
            node = ParentNode(tag=None, children=[
                LeafNode("p", "something")
            ])

            node.to_html()

        return

    def test_parent_missing_children(self) -> None:
        print("[ test ] ParentNode missing children -> ValueError raised")

        with self.assertRaises(ValueError):
            node = ParentNode("p", children=None)

            node.to_html()

        return

    def test_one_child_leaf(self) -> None:
        print("[ test ] ParentNode has 1 child")

        node = ParentNode("p", [
            LeafNode("b", "bolded text")
        ])
        
        self.assertEqual(node.to_html(), "<p><b>bolded text</b></p>")

        return

    def test_to_html_with_children(self):
        print("[ test ] ParentNode has single child")

        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

        return

    def test_many_children_leaves(self) -> None:
        print("[ test ] ParentNode has many children")

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_result = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        self.assertEqual(node.to_html(), expected_result)

        return

    def test_to_html_with_grandchildren(self):
        print("[ test ] ParentNode parent -> parent -> child")

        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

        return

    def test_parent_and_leaf_children_nodes(self) -> None:
        print("[ test ] ParentNode parent -> [parent, leaf] -> child")

        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])

        leaf_node = LeafNode("b", "sibling")

        parent_node = ParentNode("div", [child_node, leaf_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><b>sibling</b></div>",
        )

        parent_node = ParentNode("div", [leaf_node, child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>sibling</b><span><b>grandchild</b></span></div>",
        )

        return

    def test_parent_props(self) -> None:
        print("[ test ] Parentnode has props")

        child_node  = LeafNode("b", "sample bold")
        parent_node = ParentNode("p", [child_node], {"style": "color: #ffffff"})

        expected_result = '<p style="color: #ffffff"><b>sample bold</b></p>'

        self.assertEqual(parent_node.to_html(), expected_result)

        return

    def test_parent_children_props(self) -> None:
        print("[ test ] ParentNode and LeafNode have props")

        child_node  = LeafNode("b", "sample bold", {"style": "color: #000000"})
        parent_node = ParentNode("p", [child_node], {"style": "color: #ffffff"})

        expected_result = '<p style="color: #ffffff"><b style="color: #000000">sample bold</b></p>'

        self.assertEqual(parent_node.to_html(), expected_result)

        return

    def test_img_child(self) -> None:
        print("[ test ] ParentNode has <img> child")

        sample_props = {
            "src": "https://img-loc.com",
            "alt": "alt text"
        }
        img_node = LeafNode("img", "unused", sample_props)
        parent_node = ParentNode("p", [img_node], {"style": "color: #ffffff"})

        expected_result = '<p style="color: #ffffff"><img src="https://img-loc.com" alt="alt text" /></p>'

        self.assertEqual(parent_node.to_html(), expected_result)

        return

class TestTextNode(unittest.TestCase):
    # Node Creation Tests
    def test_create_text(self) -> None:
        print("[ test ] TextNode creating type text")

        node1 = TextNode("normal text node", TextType.TEXT)
        expected_result = "TextNode(normal text node, text, None)"

        self.assertEqual(str(node1), expected_result)

        return

    def test_create_bold(self) -> None:
        print("[ test ] TextNode creating type bold")

        node1 = TextNode("bold node", TextType.BOLD)
        expected_result = "TextNode(bold node, bold, None)"

        self.assertEqual(str(node1), expected_result)

        return

    def test_create_link_with_url(self) -> None:
        node = TextNode("alt text", TextType.LINK, "https://image-loc.com")

        test_value = str(node)
        expected_value = "TextNode(alt text, link, https://image-loc.com)"

        self.assertEqual(test_value, expected_value)

        return

    def test_create_link_missing_url(self) -> None:
        node1 = TextNode("alt img", TextType.LINK)
        node3 = TextNode("alt img", TextType.LINK, None)

        expected_value = "TextNode(alt img, link, None)"

        test_value_1 = str(node1)
        test_value_3 = str(node3)

        self.assertEqual(test_value_1, expected_value)
        self.assertEqual(test_value_3, expected_value)

        return

    def test_create_link_empty_url(self) -> None:
        node = TextNode("alt img", TextType.LINK, "")

        expected_value = "TextNode(alt img, link, )"
        test_value = str(node)

        self.assertEqual(test_value, expected_value)

        return

    # Overloaded = operator Tests
    def test_eq_match(self) -> None:
        print("[ test ] TextNode overloaded = catches matches")

        node1 = TextNode("normal text node", TextType.TEXT)
        node2 = TextNode("normal text node", TextType.TEXT)

        self.assertEqual(node1, node2)

        return

    def test_eq_not_match(self) -> None:
        print("[ test ] TextNode overloaded = skips mismatches")

        node1 = TextNode("normal text node", TextType.TEXT)
        node2 = TextNode("italic text node", TextType.ITALIC)
        node3 = TextNode("link", TextType.LINK, "https://example.com")

        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node2, node3)

        return

    def test_eq_handles_missing_url(self) -> None:
        print("[ test ] TextNode overloaded = skips missing url")

        node4 = TextNode("link", TextType.LINK, "https://example.com")
        node5 = TextNode("link", TextType.LINK)

        self.assertNotEqual(node4, node5)

        return

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_to_html(self) -> None:
        print("[ test ] TextNode <Text> -> HTMLNode")

        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        return

    # def test_bold_to_html(self) -> None:
    #     ...
    #
    #     return
    #
    # def test_italic_to_html(self) -> None:
    #     ...
    #
    #     return
    #
    # def test_code_to_html(self) -> None:
    #     ...
    #
    #     return
    #
    def test_link_to_html(self) -> None:
        print("[ test ] TextNode <Link> -> HTMLNode")

        node = TextNode(
            "click me!",
            TextType.LINK,
            "https://example.com"
        )
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click me!")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

        return

    def test_image_to_html(self) -> None:
        print("[ test ] TextNode <Image> -> HTMLNode")

        node = TextNode(
            "alt text",
            TextType.IMAGE,
            "https://image-loc.com"
        )
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://image-loc.com", "alt": "alt text"})

        return

    def test_invalid_text_to_html(self) -> None:
        print("[ test ] TextNode <invalid> -> HTMLNode fails")

        node = TextNode("i cannot be converted", "garbage value")
        with self.assertRaises(Exception):
            html_node = text_node_to_html_node(node)

        return

class TestImageLinkExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        print("[ test ] Image Text Extract")

        test_text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        test_res  = ("image", "https://i.imgur.com/zjjcJKZ.png")

        matches = extract_markdown_images(test_text)

        self.assertListEqual(
            [test_res],
            matches
        )

        return

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

#---[ Test Entry ]--------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()

#---[ Test Entry ]--------------------------------------------------------------
