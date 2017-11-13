from contextlib import contextmanager
import os


@contextmanager
def remove_envvars(envvar_list):
    preservation_list = dict()
    for envvar in envvar_list:
        if envvar in os.environ:
            preservation_list[envvar] = os.environ[envvar]
            os.environ.pop(envvar)
    yield

    for envvar, val in preservation_list.items():
        os.environ[envvar] = val


@contextmanager
def add_envvars(envar_dict):
    for var in envar_dict:
        assert(var not in os.environ)
    for var, val in envar_dict.items():
        os.environ[var] = val

    yield

    for var in envar_dict:
        os.environ.pop(var)
