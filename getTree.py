import argparse
import requests
from config import githubToken

parser = argparse.ArgumentParser(description="Print a GitHub repo's file tree.")
parser.add_argument("--link", type=str, default=None, help="GitHub repo link")
parser.add_argument("--only-dir", type=lambda v: v.lower() == "true",
                     default=False, help="Show only directories (True/False)")
args = parser.parse_args()

repo_url = args.link or input("Paste github repo link: ")
repo_url = repo_url.strip()

# Strip trailing slash and .git if present, then split into parts
parts = repo_url.rstrip("/").removesuffix(".git").split("/")
owner = parts[-2]
repo = parts[-1]

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {githubToken}",
    "X-GitHub-Api-Version": "2022-11-28"
}
params = {"recursive": "1"}

def get_tree(owner, repo, branch):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}"
    return requests.get(url, headers=headers, params=params)

response = get_tree(owner, repo, "main")

if response.status_code == 404:
    response = get_tree(owner, repo, "master")

response.raise_for_status()  # if neither branch worked, this raises now

data = response.json()

type_map = {"blob": "file", "tree": "directory"}

for item in data["tree"]:
    kind = type_map.get(item["type"], item["type"])
    if args.only_dir and kind != "directory":
        continue
    print(item["path"], "-", kind)