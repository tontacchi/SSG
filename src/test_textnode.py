import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq_match(self) -> None:
        print("[ test ] TextNode overloaded = catches matches")

        node1 = TextNode("normal text node", TextType.NORMAL_TEXT)
        node2 = TextNode("normal text node", TextType.NORMAL_TEXT)

        self.assertEqual(node1, node2)

        return

    def test_eq_not_match(self) -> None:
        print("[ test ] TextNode overloaded = skips mismatches")

        node1 = TextNode("normal text node", TextType.NORMAL_TEXT)
        node2 = TextNode("italic text node", TextType.ITALIC_TEXT)
        node3 = TextNode("link", TextType.LINK_TEXT, "https://example.com")

        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node2, node3)

        return

    def test_eq_handles_missing_url(self) -> None:
        print("[ test ] TextNode overloaded = skips missing url")

        node4 = TextNode("link", TextType.LINK_TEXT, "https://example.com")
        node5 = TextNode("link", TextType.LINK_TEXT)

        self.assertNotEqual(node4, node5)

        return

if __name__ == "__main__":
    unittest.main()

