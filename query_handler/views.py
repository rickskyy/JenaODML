from rest_framework import status
from query_handler.services.fuzzy_query_service import FuzzyQueryService

from rest_framework.decorators import api_view
from rest_framework.response import Response
from six.moves.urllib.parse import urlencode
import requests
import json


FUSEKI_ENDPOINT = 'http://ec2-18-218-42-40.us-east-2.compute.amazonaws.com:3030'


@api_view(['POST'])
def query_handler_sparql(request):

    if request.method == 'POST':
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        url = FUSEKI_ENDPOINT + '/odml-tdb/sparql'

        if request.query_params:
            url += '?' + urlencode(request.query_params)
        response = requests.request('POST', url, headers=headers)

        return Response(status=response.status_code, data=json.loads(response.text))


@api_view(['GET', 'POST'])
def query_handler_fuzzy_sparql(request):

    if request.method == 'POST':
        # TODO handle validation
        request_body = json.loads(request.body)
        if request_body:

            # query = 'FIND sec(name, type) prop(name) HAVING Recording, Date'
            # dataset = '<http://ec2-18-218-42-40.us-east-2.compute.amazonaws.com:3030/odml-tdb/data/drosophila>'

            query = request_body['query']
            dataset = request_body['dataset']

            headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            url = FUSEKI_ENDPOINT + '/odml-tdb/sparql'

            service = FuzzyQueryService()
            sparql_queries_list = service.fuzzy_to_sparql(query, dataset)
            response_list = service.execute_queries(sparql_queries_list, url, headers)
            return Response(status=status.HTTP_200_OK, data=response_list)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)
