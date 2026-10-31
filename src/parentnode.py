from src.htmlnode import HTMLNode

class ParentNode(HTMLNode):
	def __init__(
			self, tag: str,
			children: list[HTMLNode],
			props: dict | None = None) -> None:
		super().__init__(tag, None, children, props)

	def to_html(self) -> str:
		if not self.children:
			raise ValueError("All parent nodes must have at least 1 child")
		if self.tag is None:
			raise ValueError("Tag is a required property of parent node")

		html = f"<{self.tag}{self.props_to_html()}>"
		for child in self.children:
			html += child.to_html()
		html += f"</{self.tag}>"
		return html