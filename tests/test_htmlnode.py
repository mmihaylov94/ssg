import unittest
from src.htmlnode import HTMLNode
from src.leafnode import LeafNode
from src.parentnode import ParentNode

class TestHTMLNode(unittest.TestCase):
	def test_three_props_to_html(self):
		props = {
			"style": "bold",
			"target": "_blank",
			"href": "https://www.google.com"
		}
		node = HTMLNode("a", "I have some text", None, props)
		actual_output = node.props_to_html()
		expected_output = " style=\"bold\" target=\"_blank\" href=\"https://www.google.com\""
		self.assertEqual(expected_output, actual_output)

	def test_one_prop_to_html(self):
		props = {
			"style": "bold"
		}
		node = HTMLNode("a", "I have some text", None, props)
		actual_output = node.props_to_html()
		expected_output = " style=\"bold\""
		self.assertEqual(expected_output, actual_output)

	def test_no_prop_to_html(self):
		node = HTMLNode("a", "I have some text")
		actual_output = node.props_to_html()
		self.assertEqual("", actual_output)

	def test_values(self):
		node = HTMLNode("div", "I wish I could read")
		self.assertEqual(node.tag, "div")
		self.assertEqual(node.value, "I wish I could read")
		self.assertEqual(node.children, None)
		self.assertEqual(node.props, None)

	def test_repr(self):
		node = HTMLNode("p", "What a strange world", None, {"class": "primary"})
		expected_output = "HTMLNode(tag='p', value='What a strange world', children=None, props={'class': 'primary'})"
		self.assertEqual(node.__repr__(), expected_output)

	def test_values_leaf(self):
		node = LeafNode("div", "I wish I could read")
		self.assertEqual(node.tag, "div")
		self.assertEqual(node.value, "I wish I could read")
		self.assertEqual(node.props, None)

	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_repr_leaf(self):
		node = LeafNode("p", "What a strange world", {"class": "primary"})
		expected_output = "HTMLNode(tag='p', value='What a strange world', props={'class': 'primary'})"
		self.assertEqual(node.__repr__(), expected_output)

	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(
			parent_node.to_html(),
			"<div><span><b>grandchild</b></span></div>",
		)

	def test_to_html_many_children(self):
		node = ParentNode(
			"p",
			[
				LeafNode("b", "Bold text"),
				LeafNode(None, "Normal text"),
				LeafNode("i", "italic text"),
				LeafNode(None, "Normal text"),
			],
		)
		self.assertEqual(
			node.to_html(),
			"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
		)

	def test_headings(self):
		node = ParentNode(
			"h2",
			[
				LeafNode("b", "Bold text"),
				LeafNode(None, "Normal text"),
				LeafNode("i", "italic text"),
				LeafNode(None, "Normal text"),
				],
		)
		self.assertEqual(
				node.to_html(),
				"<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
		)

if __name__ == "__main__":
	unittest.main()