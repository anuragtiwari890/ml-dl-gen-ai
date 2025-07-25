import os
import subprocess
import shutil

def clone_repo(repo_url: str, local_dir: str = "cloned_repos") -> str:
    repo_name = repo_url.rstrip("/").split("/")[-1]
    repo_path = os.path.join(local_dir, repo_name)

    # Remove if already cloned to avoid stale state
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    os.makedirs(local_dir, exist_ok=True)

    try:
        subprocess.run(["git", "clone", repo_url, repo_path], check=True)
        return repo_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to clone repo: {e}")


def get_repo_files(repo_path, extensions=(".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs", ".go", ".rb", ".php", ".rs", ".html", ".css", ".json", ".yaml", ".yml")):
    """
    Recursively get all code files in the repo with given extensions.
    """
    repo_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(extensions):
                relative_path = os.path.relpath(os.path.join(root, file), repo_path)
                repo_files.append(relative_path)
    return sorted(repo_files)


def get_all_files(repo_path: str, extensions: tuple = (".py", ".js", ".ts", ".md")) -> list:
    matching_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(extensions):
                full_path = os.path.join(root, file)
                matching_files.append(full_path)
    return matching_files


def read_file_content(repo_path, relative_file_path):
    """
    Read the full content of the file using its path relative to the repo root.
    """
    abs_path = os.path.join(repo_path, relative_file_path)
    with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

