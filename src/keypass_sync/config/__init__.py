"""Manage sync configuration:

Which file to sync, with which google account, with which file on the drive.

See https://github.com/Retzoh/google_services_wrapper for the google-api SSO
integration
"""

import json
import pprint
from google_services import config as services_config

from keypass_sync.utilities import logger, sanitize_path, \
    create_folder_if_needed
from keypass_sync.config import ask_user
from keypass_sync.config.validate import config as validate_config

default_config_path = '~/.keypass_google_drive_sync/'


def get_config_file_path(version):
    return sanitize_path(default_config_path) / version


def _read(version: str= 'default')->dict:
    """Load desired config fom the filesystem

    The config should contain:

    * A `credential_folder_path` entry pointing to a folder
      containing at least a `client_id.json` or `token.json` file. The
      validity of those files will be checked later by the google_services
      package (https://github.com/Retzoh/google_services_wrapper).
    * A `local_file_path` telling where the file to sync is, on the local
      machine
    * A `cloud_file_id` entry containing the google-drive-id of the file to
      sync
    * A `cache_folder` entry telling where the script may cache data

    Args:
        version (str): version of the configuration to use

    Returns:
        dict containing the saved/default values
    """
    logger.info('loading config')
    logger.debug(f'version: {version}')
    # Setting default values
    config = dict(
        credential_folder_path='',
        local_file_path='',
        cloud_file_id='',
        cache_folder=default_config_path + f'{version}_cache/')

    # Update them with saved ones
    config_file_path = get_config_file_path(version)
    logger.debug(f'config path: {config_file_path}')
    if config_file_path.exists():
        with config_file_path.open("r") as config_file:
            saved_config = json.load(config_file)
        config.update(saved_config)

    logger.debug(f'Loaded config: {pprint.pformat(config)}')
    return config


def load(version: str='')->tuple:
    """Load, validate and process the config for the specified version

    The processing consists of:

    * Setting the path for the google-api SSO token for the google_services
      package (https://github.com/Retzoh/google_services_wrapper)
    * Return the config elements, ready to be fed to the other scripts (e.g.
      sync, ...)

    Args:
        version(str): version of the configuration to use

    Returns:
        (local_file_path: pathlib.Path, cloud_file_id: str,
        cache_folder: pathlib.Path)
    """
    if version == '':
        version = 'default'

    config = validate_config(_read(version), context_msg=(
            f' Please make sure that you have followed the '
            f'instructions at '
            f'https://github.com/Retzoh/keypass_google_drive_sync to download'
            f'a google-SSO token and run `python -m keypass-sync init`. '
            f'Config version: {version}.'))

    if 'credential_folder_path' in config.keys():
        logger.info('setting credential path')
        services_config.default.credential_path = config[
            'credential_folder_path']

    return (sanitize_path(config['local_file_path']),
            config['cloud_file_id'],
            sanitize_path(config['cache_folder']))


def _write(config: dict, version: str= 'default')->dict:
    """Save a config

    The config should contain:

    * A `credential_folder_path` entry pointing to an existing folder
      containing at least a `client_id.json` or `token.json` file. The
      validity of those files will be checked later by the google_services
      package (https://github.com/Retzoh/google_services_wrapper).
    * A `local_file_path` telling where the file to sync is, on the local
      machine
    * A `cloud_file_id` entry containing the google-drive-id of the file to
      sync
    * A `cache_folder` entry telling where the script may cache data

    Args:
        config (dict): the config elements to _write
        version (str): version of the configuration to use

    Returns:
        the config, dict containing the saved/default values
    """
    logger.info('saving config')

    logger.debug(f'version: {version}')

    create_folder_if_needed(get_config_file_path(version).parent)
    with get_config_file_path(version).open("w") as config_file:
        json.dump(config, config_file)

    logger.debug(f'Saved config: {pprint.pformat(config)}')
    return config


def init(version: str='')->None:
    """Setup everything to be able to sync a file

    The setup steps are:

    * Ask the user for the config elements
    * Copy the OAuth 2 Id file to the inter-data folder (
      ~/.keypass_google_drive_sync/)
    * Validate the config elements
    * Save the config

    Args:
        version (str): version of the configuration to use
    """

    if version == '':
        version = 'default'
    config = _read(version)

    print('Setting up the configuration for the syncing utility with '
          'google-cloud.')
    _ = input('Make sure that your have followed the instructions about:\n'
              '- how to download your google-SSO token\n'
              '- getting the id of the keypass database on the cloud\n'
              'at https://github.com/Retzoh/keypass_google_drive_sync.\n'
              '[Ok]')

    root_path = create_folder_if_needed(
        sanitize_path(default_config_path) / f'{version}_SSO')

    (root_path / 'client_id.json')\
        .write_text(
        sanitize_path(
            ask_user.credential_file_path(
                root_path, config['credential_folder_path'] + '/client_id.json')
        ).read_text())
    config['credential_folder_path'] = str(root_path)

    # Getting local_file_path
    config["local_file_path"] = ask_user.local_file_path(
        config['local_file_path'])

    config["cloud_file_id"] = ask_user.cloud_file_id(config['cloud_file_id'])

    _write(validate.config(config, version), version)
