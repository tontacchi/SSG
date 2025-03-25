import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()

