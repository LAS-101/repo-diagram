# Examples

This folder contains example usage and output demonstrations of the Repository Diagram Generator.

## Quick Start Examples

### Generate a Simple Directory Overview

```bash
# Basic command - generates a 2-level directory map
python3 generator.py --link https://github.com/facebook/react
```
Output: `repo_tree.svg` with React's directory structure

### View a Complete Repository Tree

```bash
# Full tree with all files and folders up to depth 3
python3 generator.py --link https://github.com/nodejs/node \
  --include-files --max-depth 3 --output node_structure.svg
```

### Compare Repository Structures

```bash
# Generate multiple repository diagrams for comparison
python3 generator.py --link https://github.com/vuejs/vue --output vue_structure.svg
python3 generator.py --link https://github.com/angular/angular --output angular_structure.svg
```

## Real-World Use Cases

### 1. **Onboarding New Developers**
Help new team members understand the project structure:
```bash
python3 generator.py --link https://github.com/your-org/your-project \
  --output project_structure.svg
# Share the SVG with new developers
```

### 2. **Architecture Documentation**
Create visual diagrams for project documentation:
```bash
python3 generator.py --link https://github.com/kubernetes/kubernetes \
  --include-files --max-depth 2 --output k8s_architecture.svg
```

### 3. **Repository Analysis**
Analyze complex project structures:
```bash
# Deep dive into a monorepo
python3 generator.py --link https://github.com/facebook/react-native \
  --include-files --max-depth 4 --output monorepo_analysis.svg
```

### 4. **Quick Repository Comparison**
```bash
# Compare two similar projects
python3 generator.py --link https://github.com/twbs/bootstrap --output bootstrap.svg
python3 generator.py --link https://github.com/tailwindlabs/tailwindcss --output tailwind.svg
```

## Popular Repositories to Explore

| Repository | Command | Output |
|------------|---------|--------|
| **React** | `python3 generator.py --link https://github.com/facebook/react` | `react.svg` |
| **Vue** | `python3 generator.py --link https://github.com/vuejs/vue` | `vue.svg` |
| **Node.js** | `python3 generator.py --link https://github.com/nodejs/node --max-depth 1` | `node.svg` |
| **Python** | `python3 generator.py --link https://github.com/python/cpython --max-depth 2` | `cpython.svg` |
| **Linux Kernel** | `python3 generator.py --link https://github.com/torvalds/linux --max-depth 1` | `linux.svg` |

## Advanced Examples

### Pipe Output Directly

```bash
# Chain getTree and generator for custom processing
python3 getTree.py --link https://github.com/owner/repo | \
  python3 generator.py --repo-name "My Project" --output custom.svg
```

### Generate Multiple Formats

```bash
# Create both SVG and PNG versions
python3 generator.py --link https://github.com/owner/repo --output repo.svg
python3 generator.py --link https://github.com/owner/repo --output repo.png --include-files
```

### Directory-Only Comparison

```bash
# Generate compact directory maps for multiple repos
python3 generator.py --link https://github.com/torvalds/linux --output linux.svg
python3 generator.py --link https://github.com/git/git --output git.svg
# Both outputs show only top-level directories (compact and readable)
```

## Tips for Best Results

1. **For large repositories:** Start with default settings (directories only, 2-level depth)
2. **For understanding structure:** Use `--include-files` with `--max-depth 2-3`
3. **For complete analysis:** Use `--max-depth 0` with `--include-files`
4. **For presentations:** SVG format works best, can be embedded in slides
5. **For reports:** PNG format is better for Word/PDF documents

## Expected Output Examples

### Directory-Only (Default)
- Compact and clean
- Shows folder hierarchy
- Easy to read at a glance
- Best for quick understanding

### With Files (--include-files)
- More detailed
- Shows all file names
- Larger canvas
- Better for complete documentation

### Full Tree (--max-depth 0 --include-files)
- Complete repository view
- May be very wide for large repos
- Useful for detailed analysis
- Best viewed in a browser with zoom
