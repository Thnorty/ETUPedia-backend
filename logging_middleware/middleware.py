import json

from django.utils.deprecation import MiddlewareMixin
from logging_middleware.logging_utils import log


class RequestLoggingMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        try:
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR', None)
            token = request.META.get('HTTP_AUTHORIZATION', None)
            app_version = request.META.get('HTTP_APP_VERSION', None)
            if token:
                parts = token.split(' ')
                token = parts[1] if len(parts) > 1 else None
            end_point = request.path
            payload = request.body.decode('utf-8')
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError:
                payload = None
            log(level='info', ip_address=ip_address, token=token, endpoint=end_point, payload=payload, app_version=app_version)
        except Exception as e:
            log(level='error', message=str(e))
        return None
