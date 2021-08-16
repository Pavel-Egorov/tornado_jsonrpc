JSON RPC implementation for tornado
===================================

This implementation follow JSONRPC 2.0 specification.

REQUIREMENTS
------------

    python >= 3.5 (async/await is used in the package)

INSTALLATION
------------

    pip install tornado_jsonrpc

USAGE
-----

It is so simple:

1. Just create `views.py`

        def some_view(request: RequestHandler, *args, **kwargs):  # 
            """
            args: positional params, which You pass when call jsonrpc method
            kwargs: named params, which You pass when call jsonrpc method
            """

            return {'foo': 'bar'}  # any JSON serializable object (dict or list for example)

2. And then create `tornado_app.py`, where You define tornado Application:

        from tornado_jsonrpc import JSONRPCHandler
        from tornado.ioloop import IOLoop
        from tornado.web import Application

        from your_package import views

        Application(
            [
                ('/api', views.JSONRPCHandler, dict(views=views)),
            ],
        ).listen(8888)

        IOLoop.current().start()

3. You can also use CORSIgnoreJSONRPCHandler to receive requests from all sources
or WithCredentialsJSONRPCHandler to also receive cookies with request.

CONTRIBUTE
----------

If You have found an error or want to offer changes - create a pull request, and I will review it as soon as possible!
