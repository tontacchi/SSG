import unittest

from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()

