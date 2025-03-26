import unittest

from   textnode import TextNode, TextType
from   htmlnode import HTMLNode
from   main     import text_node_to_html_node

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

