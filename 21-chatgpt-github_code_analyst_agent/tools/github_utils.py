'''
✅ Purpose:
Handles Git operations: clone, replace existing folder.

🧠 Concepts:
This will become a tool used by agents in future versions.

You’re abstracting GitHub repo handling for reuse.
'''

'''
code walk through - 

| Line                                    | Purpose                                                         |
| --------------------------------------- | --------------------------------------------------------------- |
| `import os`                             | To check if the directory already exists                        |
| `import shutil`                         | Used to delete the old directory (if any)                       |
| `from git import Repo`                  | Comes from the `GitPython` library – provides Git API in Python |
| `def clone_repo(...)`                   | Defines a function to clone a repo from GitHub                  |
| `if os.path.exists(target_dir):`        | Checks if previous clone exists                                 |
| `shutil.rmtree(target_dir)`             | Deletes old clone to ensure clean clone each time               |
| `Repo.clone_from(repo_url, target_dir)` | Clones the remote Git repo                                      |
| `return target_dir`                     | Returns the local path of the cloned repo (default: `"repo/"`)  |

'''

# utils/github_utils.py

from github import Github

def fetch_repo_files(repo_url, token=None):
    try:
        if token:
            g = Github(token)
        else:
            g = Github()  # Public access for unauthenticated requests

        repo_name = repo_url.strip("/").split("/")[-2:]
        repo_full_name = "/".join(repo_name)
        repo = g.get_repo(repo_full_name)
        contents = repo.get_contents("")

        files = []
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                files.append({
                    "path": file_content.path,
                    "url": file_content.download_url
                })
        return files
    except Exception as e:
        print("Error fetching repo:", e)
        return []

def fetch_file_content(repo_url, file_path, github_token=None):
    """Fetch the content of a file from a GitHub repo."""
    if github_token:
        g = Github(github_token)
    else:
        g = Github()  # Public access for unauthenticated requests
    
    repo_name = repo_url.split("github.com/")[1].rstrip("/")
    repo = g.get_repo(repo_name)
    file_content = repo.get_contents(file_path)
    return file_content.decoded_content.decode()



'''
possible improvements - 

    * Add support for private repos (using a GitHub token)
    * Clone into a custom folder based on repo name
    * Add error handling (e.g., invalid URL, network issues)
    * Add a CLI wrapper for clone_repo()
'''
