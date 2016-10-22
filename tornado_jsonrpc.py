import json
from copy import deepcopy
from sys import exc_info

from tornado.web import RequestHandler

MAX_ERROR_MESSAGE_LENGTH = 200

PROTOCOL_VERSIONS = ('2.0',)


class JSONRPCHandler(RequestHandler):  # noqa

    def initialize(self, views):  # noqa
        self.views = views  # noqa

    async def post(self, *args, **kwargs):
        try:
            request_body = json.loads(self.request.body.decode())
            if not request_body:
                raise InvalidJSON

            if not (isinstance(request_body, dict) or isinstance(request_body, list)):
                raise InvalidJSON
        except (UnicodeDecodeError, json.JSONDecodeError) as exception:
            self.write(_get_encoded_response({'id': None, 'result': None, 'error': _get_error(exception)}))
            return

        if isinstance(request_body, list):
            responses = []

            for i in request_body:
                response = await _get_response(self, self.views, i)
                if response:
                    responses.append(response)

            if responses:
                self.write(_get_encoded_response(responses))
        else:
            response = await _get_response(self, self.views, request_body)
            if response:
                self.write(_get_encoded_response(response))


def _get_error(exception):
    return {
        'code': getattr(exception, 'code', InternalError.code),
        'message': getattr(exception, 'message', str(exc_info()[0]))[:MAX_ERROR_MESSAGE_LENGTH],
        'data': getattr(exception, 'data', None)
    }


def _get_encoded_response(response):
    return json.dumps(response).encode()


async def _get_response(request, views, request_body):
    version = None
    request_id = None

    try:
        request_id = request_body.get('id')
        version = _get_version(request_body)
        result = await _get_result(request, _get_method(views, request_body), request_body.get('params'))
    except Exception as exception:
        return _get_with_protocol_version({'id': request_id, 'result': None, 'error': _get_error(exception)}, version)

    if request_id:
        return _get_with_protocol_version({'id': request_id, 'result': result, 'error': None}, version)


def _get_method(views, request_body):
    method = getattr(views, request_body.get('method', ''), None)
    if not method:
        raise MethodNotFound
    return method


def _get_version(request_body):
    version = request_body.get('jsonrpc')
    if version and version not in PROTOCOL_VERSIONS:
        raise InvalidVersion
    return version


async def _get_result(request, method, params):
    if params is None:
        return await method(request)

    elif isinstance(params, list):
        return await method(request, *params)

    elif isinstance(params, dict):
        return await method(request, **params)

    raise InvalidParams


def _get_with_protocol_version(response, version):
    updated_response = deepcopy(response)
    if version:
        updated_response['jsonrpc'] = version
    return updated_response


class InvalidJSON(Exception):
    code = -32700
    message = 'Parse error'
    data = None


class InvalidVersion(Exception):
    code = -32600
    message = 'Invalid Request'
    data = None


class MethodNotFound(Exception):
    code = -32601
    message = 'Method not found'
    data = None


class InvalidParams(Exception):
    code = -32602
    message = 'Invalid params'
    data = None


class InternalError(Exception):
    code = -32603
    message = 'Internal error'
    data = None
