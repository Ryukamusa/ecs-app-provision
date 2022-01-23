import sys
import boto3

def __get_session_config():
    key, secret, region, profile = None, None, None, None
    default_region = 'eu-west-1'
    if len(sys.argv) == 1:
        profile = 'personalacc'
    elif len(sys.argv) == 2:
        profile = sys.argv[1]
    elif len(sys.argv) == 3:
        key, secret = sys.argv[1:]
        region = default_region
    else:
        key, secret, region = sys.argv[1:]

    return key, secret, region, profile

def get_session():
    __key, __secret, __region, __profile = __get_session_config()
    return boto3.Session(aws_access_key_id = __key, aws_secret_access_key = __secret, region_name = __region, profile_name = __profile)

session = get_session()