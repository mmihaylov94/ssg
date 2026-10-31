from enum import Enum
from src.htmlnode import HTMLNode
from src.leafnode import LeafNode
from src.parentnode import ParentNode
from src.inline_markdown import text_to_textnodes
from src.textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	ULIST = "unordered_list"
	OLIST = "ordered_list"

def extract_title(markdown: str) -> str:
	blocks = markdown_to_blocks(markdown)
	for block in blocks:
		block_type = block_to_block_type(block)
		if block_type != BlockType.HEADING:
			continue
		heading_node = heading_to_html_node(block)
		if heading_node.tag == "h1":
			return heading_node.to_html().lstrip("<h1>").rstrip("</h1>")
	return ""

def markdown_to_html_node(markdown: str) -> HTMLNode:
	children: list[HTMLNode] = []
	blocks = markdown_to_blocks(markdown)
	for block in blocks:
		html_node = block_to_html_node(block)
		children.append(html_node)

	return ParentNode("div", children)

def block_to_html_node(block: str) -> ParentNode:
	block_type = block_to_block_type(block)
	match block_type:
		case BlockType.PARAGRAPH:
			block_children = text_to_children(block)
			return ParentNode("p", block_children)
		case BlockType.HEADING:
			return heading_to_html_node(block)
		case BlockType.CODE:
			return ParentNode("pre", [text_node_to_html_node(TextNode(block[3:-3].lstrip(), TextType.CODE))])
		case BlockType.QUOTE:
			return quote_to_html_node(block)
		case BlockType.ULIST:
			return list_to_html_node(block, BlockType.ULIST)
		case BlockType.OLIST:
			return list_to_html_node(block, BlockType.OLIST)

def heading_to_html_node(text: str) -> ParentNode:
	level = 0
	for char in text:
		if char == "#":
			level+=1
		else:
			break
	text = text[level:].strip()
	children = text_to_children(text)
	return ParentNode(f"h{level}", children)

def quote_to_html_node(text: str) -> ParentNode:
	lines: list[str] = []
	for line in text.split("\n"):
		lines.append(line.lstrip(">").strip())
	children = text_to_children(" ".join(lines))
	return ParentNode("blockquote", children)

def list_to_html_node(text: str, block_type: BlockType) -> ParentNode:
	if block_type == BlockType.ULIST:
		strip_func = lambda x: x[1:].strip()
		tag = "ul"
	else:
		strip_func = lambda x: x.split(". ", 1)[1].strip()
		tag = "ol"

	list_items: list[HTMLNode] = []
	lines = map(strip_func ,text.split("\n"))
	for line in lines:
		children = text_to_children(line)
		list_items.append(ParentNode("li", children))
	return ParentNode(tag, list_items)

def text_to_children(text: str) -> list[HTMLNode]:
	text = " ".join(text.split("\n"))
	children: list[HTMLNode] = []
	nodes = text_to_textnodes(text)
	for node in nodes:
		children.append(text_node_to_html_node(node))
	return children

def block_to_block_type(block: str) -> BlockType:
	lines = block.split("\n")

	if block.startswith(("#", "##", "##", "###", "####", "#####", "######")):
		return BlockType.HEADING
	if block.startswith("```\n") and block.endswith("```"):
		return BlockType.CODE
	if block.startswith(">"):
		for line in lines:
			if not line.startswith(">"):
				return BlockType.PARAGRAPH
		return BlockType.QUOTE
	if block.startswith("- "):
		for line in lines:
			if not line.startswith("- "):
				return BlockType.PARAGRAPH
		return BlockType.ULIST
	if block.startswith("1. "):
		i=1
		for line in lines:
			if not line.startswith(f"{i}. "):
				return BlockType.PARAGRAPH
			i+=1
		return BlockType.OLIST
	return BlockType.PARAGRAPH

def markdown_to_blocks(markdown: str) -> list[str]:
	blocks = list(filter(lambda x: x != "",(map(lambda x: x.strip(), markdown.split('\n\n')))))

	return blocks