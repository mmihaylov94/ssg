import shutil, os
from src.markdown_blocks import markdown_to_html_node, extract_title

def copy_files_recursive(source: str, destination: str) -> None:
	wd_path = os.path.abspath(".")
	abs_path_source = os.path.join(wd_path, source)
	abs_path_destination = os.path.join(wd_path, destination)
	if not os.path.exists(source):
		raise Exception("Source path is missing")
	
	if os.path.exists(destination):
		shutil.rmtree(destination)
	os.mkdir(abs_path_destination)
	
	for path in os.listdir(abs_path_source):
		abs_path = os.path.join(abs_path_source, path)
		if os.path.isfile(abs_path):
			shutil.copy(abs_path, abs_path_destination)
		else:
			copy_files_recursive(abs_path, os.path.join(abs_path_destination, path))

def generate_files_recursive(source: str, template: str, destination: str, basepath: str) -> None:
	wd_path = os.path.abspath(".")
	abs_path_source = os.path.join(wd_path, source)
	abs_path_destination = os.path.join(wd_path, destination)
	if not os.path.exists(source):
		raise Exception("Source path is missing")
	
	if not os.path.exists(destination):
		os.mkdir(abs_path_destination)
	
	for path in os.listdir(abs_path_source):
		abs_path = os.path.join(abs_path_source, path)
		if os.path.isfile(abs_path):
			generate_page(abs_path, template, abs_path_destination, basepath)
		else:
			generate_files_recursive(abs_path, template, os.path.join(abs_path_destination, path), basepath)

def generate_page(from_path, template_path, dest_path, basepath):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")
	with open(from_path, "r", encoding="utf-8") as file:
		markdown = file.read()

	content = markdown_to_html_node(markdown).to_html()
	title = extract_title(markdown)

	with open(template_path, "r", encoding="utf-8") as file:
		template = file.read()

	template = template.replace("{{ Title }}", title)
	template = template.replace("{{ Content }}", content)
	template = template.replace("href=\"/", f"href=\"{basepath}")
	template = template.replace("src=\"/", f"src=\"{basepath}")

	html_file_name = os.path.basename(from_path).rstrip(".md") + ".html"
	with open(os.path.join(dest_path, html_file_name), "w") as file:
		file.write(template)
