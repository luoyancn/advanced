import webob.dec
from webob.exc import HTTPBadRequest


class Route(object):

    @webob.dec.wsgify
    def __call__(self, req):
        if req.content_type != 'application/json':
            return HTTPBadRequest(message='Only application/json was suppored')
        action_args = req.environ['wsgiorg.routing_args'][1]
        method = getattr(self, action_args['action'])
        action_args.pop('action')
        action_args.pop('controller')
        try:
            resp = method(req, **action_args)
        except TypeError:
            action_args['body'] = req.body
            resp = method(req, **action_args)

        return resp
