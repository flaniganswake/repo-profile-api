""" Github/Bitbucket/Aggregation API calls
    flaniganswake@protonmail.com """
from abc import abstractmethod
from collections import namedtuple
from copy import deepcopy
from datetime import datetime
from functools import reduce
from http.client import HTTPException
import json
from multiprocessing.pool import ThreadPool
from urllib import request
from urllib.error import HTTPError, URLError
from app_impl.utils import init_logging

logger = init_logging("user_profiles_api", "repo.log")
HostData = namedtuple('HostData', 'base api hdr')


class RepoAPIData:
    ''' general api base class '''

    def __init__(self, host_data: HostData):
        ''' init host/json data '''
        self.host_data = host_data
        self.response = self.init_response()
        self.response["timestamp"] = f"{datetime.now():%Y-%m-%d-%H:%M:%S}"

    def init_response(self):
        ''' init json data '''
        with open("app_impl/resp.json") as f:
            data = f.read()
            return json.loads(data)

    def get_response(self):
        ''' retrieve response '''
        return self.response

    def dump_response(self):
        ''' dump json data '''
        with open("app_impl/temp.json", "w+") as f:
            f.write(json.dumps(self.response))

    def load_response(self, data: dict):
        ''' load json data '''
        def load(resp, _data):
            if isinstance(resp, dict):
                result = deepcopy(resp)
                for key, _ in result.items():
                    if key in result and isinstance(result[key], dict):
                        result[key] = load(result[key], _data)
                    elif key in data:
                        result[key] += deepcopy(_data[key])
                        if isinstance(result[key], list):
                            result[key] = sorted(
                                list(set([s.lower() for s in result[key]])))
                            result["count"] = len(result[key])
                return result
            return resp
        self.response = load(self.response, data)
        return self.response

    def api_call(self, url: str)-> 'json':
        ''' api call '''
        pool = ThreadPool(processes=2)
        async_result = pool.apply_async(self.async_api_call, (url,))
        return async_result.get()

    def async_api_call(self, url: str)-> 'json':
        ''' async api call '''
        result = ""
        try:
            req = request.Request(url, headers=self.host_data.hdr)
            with request.urlopen(req) as response:
                result = response.read()
        except (HTTPException, HTTPError, URLError) as e:
            result = [{"Error": f"{e} from {req}"}]
            return result
        return json.loads(result)

    def query_api(self, url: str, user: str)-> 'json':
        ''' api call from route '''
        json_result = self.api_call(url)
        if isinstance(json_result, list) and json_result[0].get("Error"):
            return [{'Error': 'No user data available.'}]
        # return json_result  # entire result for testing
        return [self.parse_data(json_result, user)]

    @abstractmethod
    def parse_data(self, _repos: 'json', user: str)-> 'json':
        ''' abstract data parser '''

    @abstractmethod
    def query_host(self, _user: str):
        ''' query specific host API '''

    @classmethod
    def aggregate(cls, json_list: list)-> 'json':
        ''' aggregate user data '''
        def merge(one, two):
            if isinstance(two, dict):
                result = deepcopy(one)
                for key, value in two.items():
                    if key in result and isinstance(result[key], dict):
                        result[key] = merge(result[key], value)
                    else:
                        result[key] += deepcopy(value)
                        if isinstance(result[key], list):
                            result[key] = sorted(list(set(result[key])))
                return result
            return two
        return [reduce(merge, json_list)]
