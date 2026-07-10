import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from github_client import GitHubClient


def main():
    parser = argparse.ArgumentParser(description="Підключення до GitHub-репозиторію.")
    parser.add_argument("--repo", required=True, help="Назва репозиторію у форматі owner/repo")
    args = parser.parse_args()

    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(env_path)

    token = os.getenv("GITHUB_TOKEN")

    try:
        client = GitHubClient(token)
        auth_info = client.check_connection()
        repo_info = client.connect_to_repo(args.repo)

        print(f"✅ Автентифіковано як: {auth_info['authenticated_as']}")
        print(f"✅ Підключено до репозиторію: {repo_info['repo']}")
        print(f"   Приватний: {repo_info['private']}")
        print(f"   Гілка за замовчуванням: {repo_info['default_branch']}")

    except ValueError as e:
        print(f"❌ Помилка підключення: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Непередбачена помилка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()