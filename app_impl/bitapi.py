""" API impl for bitbucket
    flaniganswake@protonmail.com """
from app_impl.api import HostData, RepoAPIData

# curl https://api.bitbucket.org/2.0/repositories/<user>
BIT_API_URL = "https://api.bitbucket.org/2.0"
BIT_BASE_URL = "https://bitbucket.org"
BIT_API_HDR = {}


class BitbucketRepoAPIData(RepoAPIData):

    def __init__(self):
        params = HostData(BIT_BASE_URL, BIT_API_URL, BIT_API_HDR)
        super().__init__(params)

    def parse_data(self, repos: 'json', user: str)-> 'json':
        ''' get the bitbucket repo names '''
        data = {
            "followers": 0,
            "watchers": 0,
            "originals": [],
            "forks": [],
            "languages": []
        }

        # parse bitbucket repositories
        repos = repos.get("values")
        for repo in repos:

            # repo names
            name = repo.get("full_name", "")
            if name:
                link = self.host_data.base + f"/{name}"
                if repo.get("fork", False):
                    data["forks"].append(link)
                else:
                    data["originals"].append(link)

            # watchers
            slug = repo.get("slug", "")
            if slug:
                api_url = self.host_data.api
                data["watchers"] += len(
                    self.api_call(
                        f"{api_url}/repositories/{user}/{slug}/watchers"))

            # languages
            language = repo.get("language", "")
            if language:
                data["languages"].append(language)

        # followers
        api_url = self.host_data.api
        data["followers"] += len(
            self.api_call(f"{api_url}/teams/{user}/followers"))

        return self.load_response(data)

    def query_host(self, user: str)-> 'json':
        ''' query bitbucket API '''
        api_url = self.host_data.api
        return self.query_api(f"{api_url}/repositories/{user}", user)

