import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        node1 = TextNode("normal text node", TextType.NORMAL_TEXT)
        node2 = TextNode("normal text node", TextType.NORMAL_TEXT)

        node3 = TextNode("italic text node", TextType.ITALIC_TEXT)

        node4 = TextNode("link", TextType.LINK_TEXT, "https://example.com")
        node5 = TextNode("link", TextType.LINK_TEXT)

        self.assertEqual(node1, node2)

        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node2, node3)

        self.assertNotEqual(node4, node5)

        return

if __name__ == "__main__":
    unittest.main()

