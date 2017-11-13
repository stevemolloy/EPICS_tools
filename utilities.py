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
