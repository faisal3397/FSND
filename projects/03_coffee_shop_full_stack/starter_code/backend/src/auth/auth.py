import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'fsnd3397.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee-shop-api'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
@DONE implement get_token_auth_header() method
'''


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)

    if not auth:
        raise AuthError({
            'code': 'missing_auth_header',
            'description': 'Expected Authorization Header'
        }, 401)

    split_header = auth.split()

    if split_header[0].lower() != 'bearer':
        raise AuthError({
            'code': 'header_invalid',
            'description': 'Expected Authorization Header to start with "Bearer"'
        }, 401)

    elif len(split_header) == 1:
        raise AuthError({
            'code': 'header_invalid',
            'description': 'Missing Token'
        }, 401)

    elif len(split_header) > 2:
        raise AuthError({
            'code': 'header_invalid',
            'description': 'Expected Authorization Header to be Bearer Token'
        }, 401)

    token = split_header[1]
    return token


'''
@DONE implement check_permissions(permission, payload) method
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions are not included in payload'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'The user is not allowed to do this operation'
        }, 403)

    return True


'''
@DONE implement verify_decode_jwt(token) method
'''


def verify_decode_jwt(token):
    # This part of the code was taken from the instructor's github repo which was forked by me,
    # it was a follow-along practice
    # https://github.com/faisal3397/FSND/blob/master/BasicFlaskAuth/app.py

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


'''
@DONE implement @requires_auth(permission) decorator method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
