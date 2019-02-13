"""Package providing what is needed to sync a file with the drive

"""

import hashlib
from pathlib import Path

from google_services import drive

from keypass_sync.utilities import logger, log_and_exit, \
    create_folder_if_needed


def get_hash(data: bytearray)->str:
    """Return the hexadecimal hash of file

    Args:
        data (bytearray): data to hash

    Returns:
        hash
    """
    return hashlib.sha3_512(data).hexdigest()


def was_updated(data: bytearray, reference_hash: str)->bool:
    """Check if the hash of `file` is different from the reference hash

    Args:
        data (bytearray): data to check
        reference_hash (string): reference hash

    Returns:
        true if the hash is different, else false
    """
    return get_hash(data) != reference_hash


def update_conflict_exists(data_1: bytearray, data_2: bytearray,
                           reference_hash: str)->bool:
    """Check if there is an update conflict between two data chunks

    There is a conflict if both files were updated

    Args:
        data_1 (bytearray): data to compare 1/2
        data_2 (bytearray): data to compare 2/2
        reference_hash (str): hash with which to compare the file hashes when
            looking for changes

    Returns:
        true if there is a conflict
    """
    return was_updated(data_1, reference_hash) \
           and was_updated(data_2, reference_hash)


def read_data_from_file(path: Path)->bytearray:
    """Load the data (bytes) from path

    Args:
        path (Path): where to read the data from

    Returns:
        the binary data contained at path
    """
    return path.read_bytes()


def cache_data_hash(data: bytearray, cache_entry_name: str,
                    cache_folder_path: Path) -> bytearray:
    """Cache the hash of data into `cache_folder_path`

    Args:
        data (bytearray):
        cache_entry_name (str):
        cache_folder_path (Path):

    Returns:
        the data
    """
    (create_folder_if_needed(cache_folder_path) / cache_entry_name).write_text(
        get_hash(data))
    return data


def load_entry_from_cache(cache_entry_name: str, cache_folder_path: Path):
    """

    Args:
        cache_entry_name (str):
        cache_folder_path (Path):

    Returns:
        the cache value if there is some, else None
    """
    if (cache_folder_path / cache_entry_name).exists():
        return (cache_folder_path / cache_entry_name).read_text()
    return None


def update_cloud(data: bytearray, cloud_file_id: str,
                 cache_folder_path: Path, file_name: str)->None:
    """Replace the data in the cloud with `data`

    Args:
        data (bytearray):
        cloud_file_id(str):
        cache_folder_path(Path):
        file_name(str): name to give to the file on the cloud
    """
    logger.info('Updating cloud file with local one')
    (cache_folder_path / 'tmp').write_bytes(data)
    if drive.update_file(
            cache_folder_path / 'tmp', cloud_file_id,
            file_name=file_name).get('id') is not None:
        # Success !
        cache_data_hash(data, 'file.sha', cache_folder_path)
        (cache_folder_path / 'tmp').unlink()
        logger.info('Success')
        logger.debug(f'New sha: {get_hash(data)}')


def update_local(local_file_path: Path, data: bytearray,
                 cache_folder_path: Path)->None:
    """Replace the local file content with `data`

    Args:
        local_file_path:
        data:
        cache_folder_path:
    """
    logger.info('Updating local file with cloud one')
    local_file_path.write_bytes(data)
    cache_data_hash(data, 'file.sha', cache_folder_path)
    logger.info('Success')


def sync(local_file_path: Path, cloud_file_id: str, cache_folder_path: Path):
    """Perform a sync operation between the local and the cloud data

    Args:
        local_file_path (Path): path to the file containing the local data
        cloud_file_id (str): id of the cloud file containing the remote data
        cache_folder_path (Path): path to the folder containing the
            references-hashes of the data
    """
    # Load files
    local_file = read_data_from_file(local_file_path)
    cloud_file = drive.download_file(cloud_file_id)
    cached_sha = load_entry_from_cache('file.sha', cache_folder_path)

    if cached_sha is None:
        # This is the first time we sync
        if was_updated(local_file, get_hash(cloud_file)):
            log_and_exit(
                f'Could not sync keypass database {local_file_path} with '
                f'cloud file {cloud_file_id}: both were updated since the '
                f'last sync operation. Please merge them manually using the '
                f'`force-update` option.')
        cache_data_hash(local_file, 'file.sha', cache_folder_path)
        cached_sha = load_entry_from_cache('file.sha', cache_folder_path)

    # Check for conflicts
    if update_conflict_exists(local_file, cloud_file, cached_sha):
        # Stop if a conflict was found
        log_and_exit(
            f'Could not sync keypass database {local_file_path} with '
            f'cloud file {cloud_file_id}: both were updated since the '
            f'last sync operation. Please merge them manually using the '
            f'`force-update` option.')

    # Do sync
    if was_updated(local_file, cached_sha):
        update_cloud(local_file, cloud_file_id, cache_folder_path,
                     local_file_path.name)

    if was_updated(cloud_file, cached_sha):
        update_local(local_file_path, cloud_file, cache_folder_path)
