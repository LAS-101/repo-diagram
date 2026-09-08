# Repository Diagram Generator

A Python tool that generates visual diagram representations of GitHub repository structures.

## Overview

This project creates directed graph visualizations of repository file trees, allowing you to quickly understand the folder hierarchy and structure of any public GitHub repository. The tool fetches repository metadata via the GitHub API and renders it as an interactive SVG or PNG diagram.

## How It Works

The project consists of three main components:

### 1. **config.py** — Configuration Management
Loads the GitHub authentication token from environment variables using `python-dotenv`:
```python
githubToken = os.getenv("githubToken")
```
- Reads the `.env` file to find `githubToken`
- Used by `getTree.py` to authenticate API requests
- Required for accessing private repositories and increasing rate limits

### 2. **getTree.py** — GitHub API Integration
Fetches the complete file tree from a GitHub repository:
```bash
python3 getTree.py --link https://github.com/owner/repo
```

**How it works:**
- Parses the GitHub repository URL to extract owner and repository name
- Calls the GitHub API endpoint: `/repos/{owner}/{repo}/git/trees/{branch}?recursive=1`
- Attempts `main` branch first, falls back to `master` if not found
- Outputs each file/directory as: `path - type` (e.g., `src/main.py - file`)
- Supports the `--only-dir` flag to filter directories only

**Output format:**
```
src - directory
src/main.py - file
README.md - file
config.yaml - file
```

### 3. **generator.py** — Diagram Renderer
Transforms tree data into visual graphs using Graphviz:
```bash
python3 generator.py --link https://github.com/owner/repo
```

**How it works:**
- Reads tree data from `getTree.py` (or stdin)
- Parses path strings and builds a hierarchical structure
- Creates a Graphviz directed graph with:
  - Repository name as the root node (labeled with `/`)
  - Directories and files as child nodes
  - Edges connecting parents to children
- Renders to SVG by default (scalable, zoom-friendly)
- Can output PNG format when specified

**Default behavior:**
- Limits depth to 2 levels (practical for large repos)
- Directories only (excludes files for compactness)
- Output: `repo_tree.svg`

## Setup

### Prerequisites
- Python 3.8+
- `requests` library (API calls)
- `graphviz` library (diagram rendering)
- GitHub Personal Access Token (for authentication)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <this-repo>
   cd repo-diagram
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file with your GitHub token:**
   ```bash
   echo "githubToken=ghp_YOUR_TOKEN_HERE" > .env
   ```

   **To get a GitHub token:**
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token"
   - Select `repo` scope (for public repositories)
   - Copy and save the token in `.env`

## Usage

### Basic Usage — Generate Directory Overview

```bash
python3 generator.py --link https://github.com/owner/repo
```
Creates `repo_tree.svg` showing the 2-level directory structure.

### Include Files — Detailed View

```bash
python3 generator.py --link https://github.com/owner/repo --include-files
```
Shows both directories and files in the visualization.

### Complete Repository Tree

```bash
python3 generator.py --link https://github.com/owner/repo \
  --include-files --max-depth 0 --output full_tree.svg
```
Renders every file and folder in the repository (may be wide for large repos).

### Directory-Only with Shallow Depth

```bash
python3 generator.py --link https://github.com/owner/repo --max-depth 1
```
Shows only the top-level directory structure.

### PNG Output

```bash
python3 generator.py --link https://github.com/owner/repo --output repo_tree.png
```
Renders as PNG instead of SVG.

### Pipeline Usage

Generate tree data separately and pipe to the renderer:
```bash
python3 getTree.py --link https://github.com/owner/repo | \
  python3 generator.py --repo-name myrepo --output diagram.svg
```

## Command-Line Options

### `generator.py`
- `--link` — GitHub repository URL (e.g., `https://github.com/owner/repo`)
- `--output` — Output file path with extension (default: `repo_tree.svg`)
- `--repo-name` — Custom root label for piped input (default: `repository`)
- `--max-depth` — Maximum path depth to display (default: 2, use 0 for complete tree)
- `--include-files` — Include files in addition to directories (default: off)

### `getTree.py`
- `--link` — GitHub repository URL
- `--only-dir` — Show only directories, filter out files (True/False)

## Examples

See [examples/EXAMPLES.md](examples/EXAMPLES.md) for detailed real-world usage examples, including:

- Quick start examples
- Popular repositories to explore
- Architecture documentation use cases
- Advanced piping and batch operations
- Tips for best results

### Quick Examples

**Visualize a Node.js Project:**
```bash
python3 generator.py --link https://github.com/nodejs/node --max-depth 2
```

**Deep Dive Into a Repository:**
```bash
python3 generator.py --link https://github.com/torvalds/linux \
  --include-files --max-depth 3 --output linux_structure.svg
```

**Compact Directory Map:**
```bash
python3 generator.py --link https://github.com/facebook/react
```

## Output

### SVG Format (Default)
- **Advantages:** Scalable, zoomable, works in browsers, vector-based
- **Size:** Compact SVG files even for large repositories
- **Interactivity:** Can be embedded in websites or presentations

### PNG Format
- **Advantages:** Universal compatibility, easy sharing
- **Size:** Larger files for complex trees
- **Use case:** Embedding in documents or reports

## Troubleshooting

### "401 Client Error: Unauthorized"
- Your GitHub token is invalid, expired, or revoked
- Generate a new token and update `.env`
- Verify the token has `repo` scope

### "404 Not Found"
- Repository doesn't exist or is private (without proper token scope)
- Verify the repository URL is correct
- For private repos, ensure your token has appropriate permissions

### Diagram is Too Wide
- The graph contains many sibling files or folders
- Use `--max-depth` to limit the tree depth
- Omit `--include-files` to show directories only
- SVG format handles wide graphs better than PNG

## Project Structure

```
repo-diagram/
├── README.md          # This file
├── config.py          # GitHub token configuration
├── getTree.py         # Repository tree fetcher
├── generator.py       # Diagram renderer
├── requirements.txt   # Python dependencies
├── .env               # GitHub token (not in repo)
└── examples/
    └── EXAMPLES.md    # Real-world usage examples
```

## Future Enhancements

- Filter specific file types (e.g., show only Python files)
- Customize node colors by file type
- Generate interactive HTML with collapsible nodes
- Support for private repositories with token scopes
- Export to different graph formats (DOT, JSON, etc.)

## License

MIT License — Feel free to use and modify as needed.

## Contributing

Found a bug or have a feature suggestion? Contributions welcome!
