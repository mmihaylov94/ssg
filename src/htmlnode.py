
class HTMLNode():
	def __init__(
			self, 
			tag: str | None = None, 
			value: str | None = None, 
			children: list[HTMLNode] | None = None, 
			props: dict | None = None
		) -> None:
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self) -> str:
		raise NotImplementedError("Not implemented yet.")

	def props_to_html(self) -> str:
		if not self.props:
			return ""

		html = ""
		for key, value in self.props.items():
			html += f" {key}=\"{value}\""
		return html

	def __repr__(self) -> str:
		return (
			f"HTMLNode(tag={self.tag!r}, "
			f"value={self.value!r}, "
			f"children={self.children!r}, "
			f"props={self.props!r})"
		)