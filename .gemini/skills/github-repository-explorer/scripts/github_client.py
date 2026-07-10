import requests

class GitHubClient:
    def __init__(self, token):
        if not token:
            raise ValueError("Токен не передано. Перевір GITHUB_TOKEN у .env.")
        self.token = token
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
        }

    def _request(self, method, url, **kwargs):
        response = requests.request(method, url, headers=self.headers, **kwargs)

        if response.status_code == 401:
            raise ValueError("Токен недійсний або протух.")
        if response.status_code == 403:
            raise ValueError("Немає прав доступу (scope) або перевищено ліміт запитів (rate limit).")
        if response.status_code == 404:
            raise ValueError("Репозиторій не знайдено або немає доступу.")

        response.raise_for_status()
        return response.json()

    def check_connection(self):
        url = f'{self.base_url}/user'
        data = self._request('GET', url)
        return {
            "status": "ok",
            "authenticated_as": data.get("login"),
        }

    def connect_to_repo(self, repo_full_name):
        url = f'{self.base_url}/repos/{repo_full_name}'
        data = self._request('GET', url)
        return {
            "status": "ok",
            "repo": data.get("full_name"),
            "private": data.get("private"),
            "default_branch": data.get("default_branch"),
        }

    def get_contents(self, repo_full_name, path=''):
        url = f'{self.base_url}/repos/{repo_full_name}/contents/{path}'
        return self._request('GET', url)

