""" API impl for github
    flaniganswake@protonmail.com """
from app_impl.api import HostData, RepoAPIData


# curl https://api.github.com/users/<user>/repos
GIT_BASE_URL = "https://github.com"
GIT_API_URL = "https://api.github.com"
GIT_API_HDR = {
    "Accept": "application/vnd.github.mercy-preview+json",
    # "Authorization": "token %s" % "<token>",
}


class GithubRepoAPIData(RepoAPIData):

    def __init__(self):
        params = HostData(GIT_BASE_URL, GIT_API_URL, GIT_API_HDR)
        super().__init__(params)

    def parse_data(self, _repos: 'json', user: str)-> 'json':
        ''' get the github repo names '''
        data = {
            "followers": 0,
            "watchers": 0,
            "originals": [],
            "forks": [],
            "languages": [],
            "topics": []
        }

        # parse github repositories
        for repo in _repos:

            # repo names
            name = repo.get("full_name", "")
            if name:
                link = self.host_data.base + f"/{name}"
                if repo.get("fork", False):
                    data["forks"].append(link)
                else:
                    data["originals"].append(link)

            # watchers/followers
            watchers_count = repo.get("watchers", 0)
            if watchers_count:
                data["watchers"] = watchers_count
            owner = repo.get("owner", "")
            if owner:
                followers_url = owner.get("followers_url", "")
                if followers_url:
                    data["followers"] = len(self.api_call(followers_url))

            # languages
            language = repo.get("language", "")
            if language:
                data["languages"].append(language)

            # topics
            tops = repo.get("topics", [])
            if tops:
                data["topics"].extend(tops)
        return self.load_response(data)

    def query_host(self, user: str)-> 'json':
        ''' query github API '''
        api_url = self.host_data.api
        return self.query_api(f"{api_url}/users/{user}/repos", user)

