from query_handler.services.fuzzy_finder import FuzzyFinder
from six.moves.urllib.parse import urlencode
from rest_framework.parsers import JSONParser
import json
import requests


class FuzzyQueryService:
    def __init__(self):
        pass

    @staticmethod
    def fuzzy_to_sparql(fuzzy_query, dataset):
        return FuzzyFinder().find(q_str=fuzzy_query, dataset=dataset)

    def execute_queries(self, query_list, url, headers):
        response_data_list = []

        for query in query_list:
            url_query = url + '?' + urlencode({'query': query})
            response = requests.request('POST', url_query, headers=headers)

            response_body = self._handle_response_data(response, query)
            if response_body:
                response_data_list.append(response_body)

        return response_data_list

    @staticmethod
    def _handle_response_data(response, query):
        if response.status_code == 200:
            response_body = json.loads(response.text)
            response_body['query'] = query
            return response_body

    def compose_response_from_multiple_queries(self, response_list):
        pass
