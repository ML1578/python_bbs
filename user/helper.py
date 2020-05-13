import requests
from django.conf import settings


def get_access_token(authorization_code):
    args = settings.WB_ACCESS_TOKEN_ARGS.copy()
    args['code'] = authorization_code
    response = requests.post(settings.WB_ACCESS_TOKEN_API, data=args)
    result = response.json()
    if 'error' not in result:
        access_token = result['access_token']
        uid = result['uid']
        return access_token, uid
    else:
        return None, None


def get_wb_user_info(access_token, uid):
    args = settings.WB_USER_SHOw_ARGS.copy()
    args['access_token'] = access_token
    args['uid'] = uid
    response = requests.get(settings.WB_USER_SHOW_API, params=args)
    result = response.json()
    if 'error' not in result:
        nickname = result['access_token']
        icon = result['avatar_large']
        return nickname, icon
    else:
        return None, None
