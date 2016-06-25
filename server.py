import os
import routes
import routes.middleware
import sys
import webob.dec
from webob.exc import HTTPNotFound


class Server(object):

    def __init__(self, conf):
        self.conf = conf
        self.mapper = routes.Mapper()
        api_path = 'api'
        for dirpath, dirnames, filenames in os.walk(api_path):
            for fname in filenames:
                root, ext = os.path.splitext(fname)
                if ext != '.py' or root == '__init__':
                    continue
                classname = '%s%s%s' % (root[0].upper(), root[1:], 'API')
                classpath = ('%s.%s' % (dirpath, root))
                __import__(classpath)
                clazz = getattr(sys.modules[classpath], classname)()
                self.mapper.resource(root, root, controller=clazz)
        self._router = routes.middleware.RoutesMiddleware(self._dispatch,
                                                          self.mapper)

    @webob.dec.wsgify
    def __call__(self, req):
        return self._router

    @staticmethod
    @webob.dec.wsgify
    def _dispatch(req):
        match = req.environ['wsgiorg.routing_args'][1]
        if not match:
            return HTTPNotFound()
        app = match['controller']
        return app


def public_factory(global_conf, **local_conf):
    conf = global_conf.copy()
    conf.update(local_conf)
    return Server(conf)
