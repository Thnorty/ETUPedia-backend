import logging

import bcrypt
from rest_framework.authtoken.models import Token

from api.models import Profile

logger = logging.getLogger('django')

FIXED_SALT = b'$2b$12$Q3ETT03uWBzVcrK1rGX4Vu'

def log(level='info', message=None, ip_address=None, token=None, endpoint=None, payload=None, request=None, app_version=None):
    request_owner_info = None

    if token is not None:
        try:
            token = Token.objects.get(key=token)
            profile = Profile.objects.get(user=token.user)
            request_owner_info = {
                'student_id': profile.student.id,
                'student_name': profile.student.name,
                'student_surname': profile.student.surname,
                'student_mail': profile.student.mail_etu if profile.student.mail_etu is not None else profile.student.mail_other,
            }
        except Token.DoesNotExist:
            request_owner_info = None
    elif request is not None and request.auth is not None:
        profile = Profile.objects.get(user=request.auth.user)
        request_owner_info = {
            'student_id': profile.student.id,
            'student_name': profile.student.name,
            'student_surname': profile.student.surname,
            'student_mail': profile.student.mail_etu if profile.student.mail_etu is not None else profile.student.mail_other,
        }
    elif request is not None and "email" in request.data:
        try:
            profile = Profile.objects.get(student__mail_etu=request.data["email"])
            request_owner_info = {
                'student_id': profile.student.id,
                'student_name': profile.student.name,
                'student_surname': profile.student.surname,
                'student_mail': profile.student.mail_etu if profile.student.mail_etu is not None else profile.student.mail_other,
            }
        except Profile.DoesNotExist:
            request_owner_info = {
                'student_id': None,
                'student_name': None,
                'student_surname': None,
                'student_mail': request.data["email"],
            }

    if payload and 'password' in payload:
        payload['password'] = bcrypt.hashpw(payload['password'].encode('utf-8'), FIXED_SALT).decode('utf-8')

    extra = {
        'ip_address': ip_address,
        'user': request_owner_info,
        'endpoint': endpoint,
        'payload': payload,
        'app_version': app_version
    }

    if level == 'info':
        logger.info(message, extra=extra)
    elif level == 'warning':
        logger.warning(message, extra=extra)
    elif level == 'error':
        logger.error(message, extra=extra)
    elif level == 'critical':
        logger.critical(message, extra=extra)
    else:
        logger.debug(message, extra=extra)
