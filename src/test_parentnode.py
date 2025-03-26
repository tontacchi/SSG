import unittest

from leafnode   import LeafNode
from parentnode import ParentNode

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

if __name__ == "__main__":
    unittest.main()

