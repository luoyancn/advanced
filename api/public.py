import json
from webob import Response
from route import Route


class PublicAPI(Route):

    def create(self, req, body):
        return Response(status=202, body=body, content_type='application/json')

    def index(self, req):
        body = {'method': 'index'}
        return json.dumps(body)

    def show(self, req, id):
        body = {id: 'Call the method show'}
        return Response(body=json.dumps(body), content_type='application/json')

    def update(self, req, id, body):
        return Response(status=202, body=body, content_type='application/json')

    def delete(self, req, id):
        return Response(status=204, content_type='application/json')
