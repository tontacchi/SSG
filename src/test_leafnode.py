import unittest

from leafnode import LeafNode

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

if __name__ == "__main__":
    unittest.main()

