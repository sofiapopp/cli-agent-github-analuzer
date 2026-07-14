import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from github_client import GitHubClient


def print_tree(items):
    files = [i for i in items if i['type'] == 'blob']
    dirs = [i for i in items if i['type'] == 'tree']

    print(f"📁 Папок: {len(dirs)}")
    print(f"📄 Файлів: {len(files)}\n")

    for item in sorted(items, key=lambda x: x['path']):
        icon = "📁" if item['type'] == 'tree' else "📄"
        print(f"{icon} {item['path']}")


def main():
    parser = argparse.ArgumentParser(description="Отримати структуру GitHub-репозиторію.")
    parser.add_argument("--repo", required=True, help="Назва репозиторію у форматі owner/repo")
    parser.add_argument("--branch", default=None, help="Гілка (за замовчуванням — основна гілка репо)")
    args = parser.parse_args()

    env_path = Path(__file__).resolve().parents[4] / ".env"  
    load_dotenv(env_path)

    token = os.getenv("GITHUB_TOKEN")

    try:
        client = GitHubClient(token)
        tree_data = client.get_repository_tree(args.repo, branch=args.branch)

        if tree_data.get('truncated'):
            print("⚠️  Увага: репозиторій завеликий, показано не повний список файлів.")

        print_tree(tree_data['tree'])

    except ValueError as e:
        print(f"❌ Помилка: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Непередбачена помилка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()