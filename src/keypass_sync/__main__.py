"""Cli-usage entry-point

"""

import sys
import pprint
from keypass_sync.utilities import logger, log_and_exit
from keypass_sync import config
from keypass_sync.sync_utils import sync, update_cloud, update_local, \
    read_data_from_file, drive


if __name__ == "__main__":
    logger.info('start of the project cration script')
    logger.info(f'script argument: {pprint.pformat(sys.argv)}')

    if len(sys.argv) > 1 and (sys.argv[1] == 'help' or sys.argv[1] == '-h'):
        print('\n'
              'Utility to sync a file on change with a google-drive file.\n\n'
              'Usage:\n\n'
              'python -m keypass_sync [sync] -> sync file with drive ('
              'fails if both were updated since last sync)\n\n'
              'python -m keypass_sync init -> setup SSO & file to think\n\n'
              'python -m keypass_sync force-update cloud -> overwrite the '
              'file on the cloud without checking for conflicts\n\n'
              'python -m keypass_sync force-update local -> overwrite the '
              'local file without checking for conflicts\n\n'
              '\n'
              'All commands can be followed with a `name` argument to '
              'choose between multiple files to sync:\n'
              'python -m keypass_sync sync [name]\n'
              'python -m keypass_sync init [name]\n'
              'python -m keypass_sync force-update cloud [name]\n'
              'python -m keypass_sync force-update local [name]')
        exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        version = '_'.join(sys.argv[2:])
        config.init(version)
        exit(0)

    if len(sys.argv) == 1 or sys.argv[1] == 'sync':
        version = '_'.join(sys.argv[2:])
        options = config.load(version)
        sync(*options)
        exit(0)

    if sys.argv[1] == 'force-update':
        if sys.argv[2] not in ['cloud', 'local']:
            log_and_exit(f'invalid argument for force operation: expected '
                          f'`force [local | cloud]`, got `force {sys.argv[2]}`')

        version = '_'.join(sys.argv[3:])

        local_file_path, cloud_file_id, cache_path = config.load(version)
        if sys.argv[2] == 'cloud':
            update_cloud(read_data_from_file(local_file_path), cloud_file_id,
                         cache_path, file_name=local_file_path.name)

        if sys.argv[2] == 'local':
            update_local(local_file_path, drive.download_file(cloud_file_id),
                         cache_path)
