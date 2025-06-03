from flask import Flask, request
from app import app

def handler(request):
    """Handle a request to the serverless function."""
    return app.wsgi_app(
        environ={
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https',
            'wsgi.input': request.body,
            'wsgi.errors': request.body,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'REQUEST_METHOD': request.method,
            'PATH_INFO': request.path,
            'SERVER_NAME': 'vercel.app',
            'SERVER_PORT': '443',
            'HTTP_HOST': request.headers.get('host', 'vercel.app'),
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'QUERY_STRING': request.query,
            'HTTP_USER_AGENT': request.headers.get('user-agent', ''),
            'HTTP_ACCEPT': request.headers.get('accept', ''),
            'HTTP_ACCEPT_LANGUAGE': request.headers.get('accept-language', ''),
            'HTTP_ACCEPT_ENCODING': request.headers.get('accept-encoding', ''),
            'HTTP_COOKIE': request.headers.get('cookie', ''),
            'HTTP_CONNECTION': request.headers.get('connection', ''),
            'wsgi.url_scheme': request.headers.get('x-forwarded-proto', 'https'),
            'REMOTE_ADDR': request.headers.get('x-real-ip', ''),
            'CONTENT_TYPE': request.headers.get('content-type', ''),
            'CONTENT_LENGTH': request.headers.get('content-length', ''),
        },
        start_response=lambda status, headers: None
    ) 