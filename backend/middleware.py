import json

from django.utils.deprecation import MiddlewareMixin
from backend.logging_utils import log


class RequestLoggingMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION', None)
            if token:
                parts = token.split(' ')
                token = parts[1] if len(parts) > 1 else None
            end_point = request.path
            payload = request.body.decode('utf-8')
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError:
                payload = None
            log(level='info', token=token, endpoint=end_point, payload=payload)
        except Exception as e:
            log(level='error', message=str(e))
        return None
