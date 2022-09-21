import os


def load_env_var(name: str, vartype: type = str, default: str = None):
    var = os.environ.get(name, default)
    if vartype == bool and var.lower() in ('0', 'false', ''):
        var = False
    if var is None:
        raise EnvironmentError
    else:
        return vartype(var)


REDIS_HOST = load_env_var('REDIS_HOST', str, 'localhost')
REDIS_LOCAL_PORT = load_env_var('REDIS_LOCAL_PORT', str, '6379')
DB = load_env_var('REDIS_DB_INDEX', int, '0')
CHARSET = load_env_var('CHARSET', str, 'utf-8')
DECODE_RESPONSES = load_env_var('DECODE_RESPONSES', bool, 'True')
