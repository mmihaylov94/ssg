from src.textnode import TextNode, TextType
import re

def text_to_textnodes(text: str) -> list[TextNode]:
	nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]
	nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	nodes=  split_nodes_image(nodes)
	nodes = split_nodes_link(nodes)

	return nodes

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
	new_nodes: list[TextNode] = []
	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue
		split_nodes = []
		sections = old_node.text.split(delimiter)
		if len(sections) % 2 == 0:
			raise ValueError("No closing delimiter found!")
		for i in range(len(sections)):
			if sections[i] == "":
				continue
			if i % 2 == 0:
				split_nodes.append(TextNode(sections[i], TextType.TEXT))
			else:
				split_nodes.append(TextNode(sections[i], text_type))
		new_nodes.extend(split_nodes)
	return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
	new_nodes: list[TextNode] = []

	for old_node in old_nodes:
		images = extract_markdown_images(old_node.text)
		if len(images) == 0:
			new_nodes.append(old_node)
			continue

		node_text = old_node.text
		for image in images:
			alt_text = image[0]
			url = image[1]
			node_split = node_text.split(f"![{alt_text}]({url})", 1)
			pre_image_text = node_split[0]
			if pre_image_text != "":
				new_nodes.append(TextNode(pre_image_text, TextType.TEXT))
			new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
			node_text = node_split[1]

		if node_text != "":
			new_nodes.append(TextNode(node_text, TextType.TEXT))

	return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
	new_nodes: list[TextNode] = []

	for old_node in old_nodes:
		links = extract_markdown_links(old_node.text)
		if len(links) == 0:
			new_nodes.append(old_node)
			continue

		node_text = old_node.text
		for link in links:
			link_text = link[0]
			url = link[1]
			node_split = node_text.split(f"[{link_text}]({url})", 1)
			pre_image_text = node_split[0]
			if pre_image_text != "":
				new_nodes.append(TextNode(pre_image_text, TextType.TEXT))
			new_nodes.append(TextNode(link_text, TextType.LINK, url))
			node_text = node_split[1]

		if node_text != "":
			new_nodes.append(TextNode(node_text, TextType.TEXT))

	return new_nodes

def extract_markdown_images(text: str) -> list[tuple]:
	img_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
	matches = re.findall(img_regex, text)

	return matches

def extract_markdown_links(text: str) -> list[tuple]:
	url_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
	matches = re.findall(url_regex, text)

	return matches