import os
import re
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env in root folder
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO")
VAULT_PATH = os.getenv("VAULT_PATH")

def check_env_variables():
    print("[TEST] Checking .env variables...")

    missing = False

    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN is missing.")
        print("   👉 Add your GitHub personal access token in .env like this:")
        print("      GITHUB_TOKEN=ghp_your_token_here\n")
        missing = True

    if not REPO:
        print("❌ REPO is missing.")
        print("   👉 Add the target repo in format username/repository in .env:")
        print("      REPO=yourusername/yourrepo\n")
        missing = True

    if not VAULT_PATH:
        print("❌ VAULT_PATH is missing.")
        print("   👉 Add the full path to your Obsidian vault folder in .env:")
        print("      VAULT_PATH=D:/Path/To/Obsidian/Vault\n")
        missing = True

    if not missing:
        print("✅ .env variables are present and loaded.")
    return not missing

def check_repo_format():
    print("[TEST] Validating REPO format...")

    if re.match(r"^[a-zA-Z0-9_-]+\/[a-zA-Z0-9_.-]+$", REPO):
        print("✅ REPO format is valid.")
        return True
    else:
        print("❌ Invalid REPO format:", REPO)
        print("   👉 Expected format is username/repository (not a URL). Example:")
        print("      REPO=octocat/Hello-World\n")
        return False

def check_vault_path():
    print("[TEST] Validating VAULT_PATH...")

    if not os.path.exists(VAULT_PATH):
        print(f"❌ VAULT_PATH does not exist: {VAULT_PATH}")
        print("   👉 Make sure the path is correct and the folder exists.")
        print("   Example: VAULT_PATH=D:/Notes/ObsidianVault\n")
        return False
    if not os.path.isdir(VAULT_PATH):
        print(f"❌ VAULT_PATH is not a directory: {VAULT_PATH}")
        print("   👉 Make sure VAULT_PATH points to a folder, not a file.\n")
        return False

    print("✅ VAULT_PATH exists and is a directory.")
    return True

def check_github_repo_access():
    print("[TEST] Verifying GitHub repository access...")

    url = f"https://api.github.com/repos/{REPO}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("✅ GitHub repository is accessible.")
        return True
    elif response.status_code == 404:
        print("❌ GitHub repository not found (404).")
        print(f"   👉 Check if the REPO name is correct: {REPO}")
        print("   👉 If it's a private repo, make sure your token has repo scope.\n")
        return False
    else:
        print(f"❌ GitHub API error: {response.status_code}")
        print("   👉 Double-check your token and repo name.")
        print(f"   Details: {response.text}\n")
        return False

if __name__ == "__main__":
    all_passed = (
        check_env_variables() and
        check_repo_format() and
        check_vault_path() and
        check_github_repo_access()
    )

    if all_passed:
        print("\n✅ All tests passed. You may now run main.py")
        exit(0)
    else:
        print("\n❌ One or more tests failed.")
        print("🔧 Please fix the issues above, mostly by updating your .env file.")
        exit(1)
