"""
API Gateway — single entry point that proxies requests to the correct
backend service (Step 102). A real gateway would also handle auth, rate
limiting, and SSL termination; this demonstrates just the routing concept.
"""
from flask import Flask, request, Response
import requests

app = Flask(__name__)

SERVICE_MAP = {
    'courses': 'http://127.0.0.1:5001',
    'students': 'http://127.0.0.1:5002',
}


@app.route('/api/<resource>', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/<resource>/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/<resource>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(resource, path):
    target_base = SERVICE_MAP.get(resource)
    if target_base is None:
        return {'error': f'No service registered for /{resource}'}, 404

    target_url = f'{target_base}/api/{resource}/{path}'
    try:
        upstream = requests.request(
            method=request.method,
            url=target_url,
            headers={k: v for k, v in request.headers if k.lower() != 'host'},
            json=request.get_json(silent=True),
            params=request.args,
            timeout=5,
        )
    except requests.ConnectionError:
        return {'error': f'{resource} service unavailable'}, 503

    return Response(upstream.content, status=upstream.status_code, content_type=upstream.headers.get('Content-Type'))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
