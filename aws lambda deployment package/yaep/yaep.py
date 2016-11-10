"""
YAEP - Yet Another Environment Package

"""

import os
import ConfigParser
from .utils import SectionHeader, str_to_bool
from .exceptions import UnsetException


def env(key, default=None, convert_booleans=True, boolean_map=None,
        sticky=False, type_class=unicode):
    """
    Retrieves key from the environment.
    """
    value = os.getenv(key, default)

    if value == default and default == UnsetException:
        raise UnsetException('{} was unset, but is required.'.format(
            key
        ))

    if sticky and value == default:
        os.environ[key] = str(value)

    if convert_booleans and isinstance(value, str):
        value = str_to_bool(value, boolean_map)

        # This is sort of a weird situation - if we've autoconverted
        # a boolean, we don't want to change its type. If somebody
        # doesn't want this behavior they should set convert_booleans
        # to false.
        if isinstance(value, bool):
            type_class = bool

    # If we've just used the default or if it's None, just return that
    if value is None or value == default:
        return value
    else:
        return type_class(value)


def populate_env(env_file='.env'):
    env_file = os.getenv('ENV_FILE', env_file)

    if os.path.exists(env_file):
        with open(env_file) as ef:
            env_data = ConfigParser.SafeConfigParser()
            env_data.optionxform = str
            env_data.readfp(SectionHeader(ef))

        for key, value in env_data.items(SectionHeader.header):
            os.environ[key] = str(value)
