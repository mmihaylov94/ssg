from src.files import copy_files_recursive, generate_files_recursive
import sys

def main():
	copy_files_recursive("static", "docs")

	if len(sys.argv) > 0:
		base_path = sys.argv[1]
	else:
		base_path = "/"
	generate_files_recursive("content", "template.html", "docs", base_path)

if __name__ == "__main__":
	main()