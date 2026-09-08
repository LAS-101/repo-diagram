import argparse
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

from graphviz import Digraph


def read_tree(lines):
	"""Convert getTree.py output into (path, kind) pairs."""
	entries = []
	for line in lines:
		line = line.strip()
		if not line or " - " not in line:
			continue
		path, kind = line.rsplit(" - ", 1)
		entries.append((path, kind))
	return entries


def build_graph(entries, output_name, repo_name,rankdir="LR", engine="dot"):
	output_path = Path(output_name)
	output_format = output_path.suffix.removeprefix(".") or "svg"
	output_file = output_path.with_suffix("") if output_path.suffix else output_path
	dot = Digraph(format=output_format, engine=engine)
	dot.attr(rankdir=rankdir, nodesep="0.15", ranksep="0.6")
	dot.attr("node", shape="box")
	root_id = "__repo_root__"
	dot.node(root_id, repo_name + "/", shape="folder")

	paths = {path for path, _ in entries}
	kinds = dict(entries)
	created=set()
	for path, kind in entries:
		current = PurePosixPath(path)
		parts = current.parts

		for index in range(1, len(parts) + 1):
			node_path = "/".join(parts[:index])
			if node_path not in paths:
				paths.add(node_path)
				kinds[node_path] = "directory"

		node_id = str(current)
		label = current.name + ("/" if kind == "directory" else "")
		dot.node(node_id, label)
		created.add(node_id)
  

		if len(parts) > 1:
			parent_id = "/".join(parts[:-1])
			dot.edge(parent_id, node_id)
		else:
			dot.edge(root_id, node_id)

	dot.render(str(output_file), cleanup=True)
	

def main():
	parser = argparse.ArgumentParser(
		description="Build a Graphviz image from getTree.py output."
	)
	parser.add_argument("--link", help="GitHub repository link")
	parser.add_argument(
		"--output", default="repo_tree.svg", help="Output image path (.svg or .png)"
	)
	parser.add_argument(
		"--max-depth",
		type=int,
		default=2,
		help="Maximum path depth to render; use 0 for the complete tree",
	)
	parser.add_argument(
		"--include-files",
		action="store_true",
		help="Include files in the graph instead of rendering directories only",
	)
	parser.add_argument(
		"--repo-name", default="repository", help="Root label for piped input"
	)
	args = parser.parse_args()
	only_dirs = not args.include_files

	if args.link:
		command = [sys.executable, "getTree.py", "--link", args.link]
		if only_dirs:
			command.extend(["--only-dir", "true"])
		result = subprocess.run(command, capture_output=True, text=True, check=True)
		entries = read_tree(result.stdout.splitlines())
		repo_name = PurePosixPath(urlparse(args.link).path.rstrip("/")).name
		repo_name = repo_name.removesuffix(".git") or args.repo_name
	else:
		entries = read_tree(sys.stdin)
		repo_name = args.repo_name

	if not entries:
		parser.error("no tree entries received; provide --link or pipe getTree.py output")
	if args.max_depth < 0:
		parser.error("--max-depth must be 0 or greater")
	if args.max_depth:
		entries = [
			(entry_path, kind)
			for entry_path, kind in entries
			if len(PurePosixPath(entry_path).parts) <= args.max_depth
		]
	if only_dirs:
		entries = [(entry_path, kind) for entry_path, kind in entries if kind == "directory"]

	build_graph(entries, args.output, repo_name)


if __name__ == "__main__":
	main()