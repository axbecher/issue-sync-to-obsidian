import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("REPO")
VAULT_PATH = os.getenv("VAULT_PATH")

# Validate critical environment values
if not GITHUB_TOKEN or not REPO or not VAULT_PATH:
    raise RuntimeError("❌ One or more environment variables (GITHUB_TOKEN, REPO, VAULT_PATH) are missing.")

def fetch_github_issues():
    url = f"https://api.github.com/repos/{REPO}/issues"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    print(f"[DEBUG] Fetching issues from: {url}")
    response = requests.get(url, headers=headers)

    print(f"[DEBUG] GitHub API Response Code: {response.status_code}")
    if response.status_code == 200:
        issues = response.json()
        print(f"[DEBUG] Retrieved {len(issues)} issue(s).")
        return issues
    else:
        print(f"[ERROR] GitHub API Error: {response.status_code}")
        print(f"[ERROR] Response Body: {response.text}")
        raise Exception(f"GitHub API Error: {response.status_code} - {response.text}")

def write_to_obsidian(issues):
    file_path = os.path.join(VAULT_PATH, "GitHub_Issues.md")

    # Build the new content
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"# GitHub Issues (last updated {today})\n\n"
    for issue in issues:
        if 'pull_request' in issue:
            print(f"[DEBUG] Skipping PR #{issue['number']}")
            continue
        issue_id = issue.get("number")
        title = issue.get("title", "No title")
        summary = issue.get("body", "").strip().split('\n')[0] or "No description."
        url = issue.get("html_url", "")
        content += f"## #{issue_id} - {title}\n"
        content += f"> {summary}\n"
        content += f"[View on GitHub]({url})\n\n"

    # Compare with existing content if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as existing_file:
            existing_content = existing_file.read()
            if existing_content.strip() == content.strip():
                print("[INFO] No changes detected. Skipping update.")
                return

    # Write new content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[INFO] GitHub Issues file updated: {file_path}")

if __name__ == "__main__":
    try:
        issues = fetch_github_issues()
        write_to_obsidian(issues)
    except Exception as e:
        print(f"[FATAL] {e}")
