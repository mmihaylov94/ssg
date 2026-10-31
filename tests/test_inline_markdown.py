import unittest
from src.inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from src.markdown_blocks import markdown_to_blocks
from src.textnode import TextNode, TextType

class TestCode(unittest.TestCase):	
	def test_node_split_one_element(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		actualOutput = split_nodes_delimiter([node], "`", TextType.CODE)
		expectedOutput = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" word", TextType.TEXT)
		]

		self.assertEqual(actualOutput, expectedOutput)

	def test_node_split_two_elements(self):
		node = TextNode("This is text with a `code block``second code block` word", TextType.TEXT)
		actualOutput = split_nodes_delimiter([node], "`", TextType.CODE)
		expectedOutput = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode("second code block", TextType.CODE),
			TextNode(" word", TextType.TEXT)
		]

		self.assertEqual(actualOutput, expectedOutput)

	def test_node_split_mixed_elements(self):
		node = TextNode("This is text with a `code block` word and some **bold** text", TextType.TEXT)
		actualOutput = split_nodes_delimiter([node], "**", TextType.BOLD)
		expectedOutput = [
			TextNode("This is text with a `code block` word and some ", TextType.TEXT),
			TextNode("bold", TextType.BOLD),
			TextNode(" text", TextType.TEXT)
		]

		self.assertEqual(actualOutput, expectedOutput)

	def test_node_split_unclosed_delimiter(self):
		node = TextNode("This is text with a `code block` word and some **bold text", TextType.TEXT)
		with self.assertRaises(ValueError) as context:
			split_nodes_delimiter([node], "**", TextType.BOLD)

		self.assertEqual(
			str(context.exception),
			"No closing delimiter found!"
		)

	def test_node_split_no_element(self):
		node = TextNode("This is text with a `code block` word and some **bold** text", TextType.TEXT)
		actualOutput = split_nodes_delimiter([node], "_", TextType.ITALIC)
		expectedOutput = [
			TextNode("This is text with a `code block` word and some **bold** text", TextType.TEXT)
		]

		self.assertEqual(actualOutput, expectedOutput)

	def test_node_split_multiple_text_nodes(self):
		node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
		node2 = TextNode("This is text with a `code block``second code block` word", TextType.TEXT)
		actualOutput = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
		expectedOutput = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" word", TextType.TEXT),
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode("second code block", TextType.CODE),
			TextNode(" word", TextType.TEXT)
		]

		self.assertEqual(actualOutput, expectedOutput)

	def test_node_split_multiple_mix_nodes(self):
		node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
		node2 = TextNode("Image", TextType.IMAGE, "https://mihaylov.io")
		node3 = TextNode("This is text with a `code block``second code block` word", TextType.TEXT)
		actualOutput = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
		expectedOutput = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" word", TextType.TEXT),
			TextNode("Image", TextType.IMAGE, "https://mihaylov.io"),
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode("second code block", TextType.CODE),
			TextNode(" word", TextType.TEXT)
		]

		self.assertEqual(actualOutput, expectedOutput)

	def test_node_split_no_text_node(self):
		node1 = TextNode("This is some bold text", TextType.BOLD)
		node2 = TextNode("Image", TextType.IMAGE, "https://mihaylov.io")
		node3 = TextNode("This is some italic text", TextType.ITALIC)
		actualOutput = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
		expectedOutput = [
			TextNode("This is some bold text", TextType.BOLD),
			TextNode("Image", TextType.IMAGE, "https://mihaylov.io"),
			TextNode("This is some italic text", TextType.ITALIC)
		]

		self.assertEqual(actualOutput, expectedOutput)

	def test_delim_bold(self):
		node = TextNode("This is text with a **bolded** word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("bolded", TextType.BOLD),
				TextNode(" word", TextType.TEXT),
			],
			new_nodes,
		)

	def test_delim_bold_double(self):
		node = TextNode(
			"This is text with a **bolded** word and **another**", TextType.TEXT
		)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("bolded", TextType.BOLD),
				TextNode(" word and ", TextType.TEXT),
				TextNode("another", TextType.BOLD),
			],
			new_nodes,
		)

	def test_delim_bold_multiword(self):
		node = TextNode(
			"This is text with a **bolded word** and **another**", TextType.TEXT
		)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("bolded word", TextType.BOLD),
				TextNode(" and ", TextType.TEXT),
				TextNode("another", TextType.BOLD),
			],
			new_nodes,
		)

	def test_delim_italic(self):
		node = TextNode("This is text with an _italic_ word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("italic", TextType.ITALIC),
				TextNode(" word", TextType.TEXT),
			],
			new_nodes,
		)

	def test_delim_bold_and_italic(self):
		node = TextNode("**bold** and _italic_", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
		self.assertListEqual(
			[
				TextNode("bold", TextType.BOLD),
				TextNode(" and ", TextType.TEXT),
				TextNode("italic", TextType.ITALIC),
			],
			new_nodes,
		)

	def test_delim_code(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("code block", TextType.CODE),
				TextNode(" word", TextType.TEXT),
			],
			new_nodes,
		)

	def test_extract_markdown_images(self):
		matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

	def test_extract_markdown_links(self):
		matches = extract_markdown_links("This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org)")
		self.assertListEqual(
				[
						("link", "https://boot.dev"),
						("another link", "https://wikipedia.org"),
				],
				matches,
		)

	def test_split_image(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
			],
			new_nodes,
		)

	def test_split_image_single(self):
		node = TextNode(
			"![image](https://www.example.COM/IMAGE.PNG)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
			],
			new_nodes,
		)

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
			"This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows",
			TextType.TEXT,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("link", TextType.LINK, "https://boot.dev"),
				TextNode(" and ", TextType.TEXT),
				TextNode("another link", TextType.LINK, "https://wikipedia.org"),
				TextNode(" with text that follows", TextType.TEXT),
			],
			new_nodes,
		)

	def test_text_to_textnodes(self):
		text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		expected_result = [
			TextNode("This is ", TextType.TEXT),
			TextNode("text", TextType.BOLD),
			TextNode(" with an ", TextType.TEXT),
			TextNode("italic", TextType.ITALIC),
			TextNode(" word and a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" and an ", TextType.TEXT),
			TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
			TextNode(" and a ", TextType.TEXT),
			TextNode("link", TextType.LINK, "https://boot.dev"),
		]

		actual_result = text_to_textnodes(text)
		self.assertEqual(actual_result, expected_result)

if __name__ == "__main__":
	unittest.main()