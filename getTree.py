import requests
from config import githubToken

repo_url = input("Paste github repo link: ").strip()

# Strip trailing slash and .git if present, then split into parts
parts = repo_url.rstrip("/").removesuffix(".git").split("/")
owner = parts[-2]
repo = parts[-1]

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {githubToken}",
    "X-GitHub-Api-Version": "2026-03-10"
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
    print(item["path"], "-", kind)