from src.htmlnode import HTMLNode

class LeafNode(HTMLNode):
	def __init__(
		self, 
		tag: str | None,
		value: str,
		props: dict | None = None
	) -> None:
		super().__init__(tag, value, None, props)

	def to_html(self) -> str:
		if self.value is None:
			raise ValueError("All leaf nodes must have a non-empty value")
		if self.tag is None:
			return self.value
		return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

	def __repr__(self) -> str:
		return (
			f"HTMLNode(tag={self.tag!r}, "
			f"value={self.value!r}, "
			f"props={self.props!r})"
		)