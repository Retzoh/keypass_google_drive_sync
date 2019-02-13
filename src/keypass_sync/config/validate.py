"""Functions to validate config elements / user inputs

"""

from keypass_sync.utilities import sanitize_path, log_and_exit


def credential_folder_path(candidate: str):
    """Check that given credential_folder_path candidate is valid

    Credential_folder_path contains at least `client_id.json` or `token.json`

    Args:
        candidate (str): the credential path candidate

    Returns:
        if valid:
          candidate, False
        if not:
           candidate, indication
    """
    candidate = sanitize_path(candidate)
    if not (candidate / 'token.json').exists() \
            and not (candidate / 'client_id.json').exists():
        return candidate, (
            f'No credential data (token.json of client_id.json) were found at'
            f'{candidate}.')

    return candidate, False


def cloud_file_id(candidate: str):
    """Check that given cloud_file_id candidate is valid

    Just check that it is not blank. It's validity cannot be tested now as
    the appropriate services are not instantiated yet.

    An id of a file that does not exist would pass here and probably raise a
    runtime error later

    Args:
        candidate (str): the cloud_file_id candidate

    Returns:
        if valid:
          candidate, False
        if not:
           candidate, indication
    """
    if candidate == '':
        return candidate, (
            f'Google-drive file id should not be blank.')
    return candidate, False


def is_file_and_exists(candidate: str):
    """Check that the given candidate is valid

    It is invalid if:

    * It is empty
    * It does not point to anything existing in the file system
    * It does not point to a file

    Args:
        candidate (str): the file-path candidate

    Returns:
        if valid:
          candidate, False
        if not:
           candidate, indication

    """
    if candidate == '':
        return candidate, (
            f'The Path to the file to sync should not be empty.')

    if not sanitize_path(candidate).exists():
        return candidate, (
            f'The path {candidate} does not exist.')

    # is_file_and_exists points to a file
    if not sanitize_path(candidate).is_file():
        return candidate, (
            f'The path {candidate} does not point to a file.')

    return candidate, False


def config(candidate: dict, context_msg: str= '')->dict:
    """Validate a config candidate

    A valid config should contain:

    * A `credential_folder_path` entry pointing to an existing folder
      containing at least a `client_id.json` or `token.json` file. The
      validity of those files will be checked later by the google_services
      package (https://github.com/Retzoh/google_services_wrapper).
    * A `local_file_path` pointing to an existing file
    * A non-empty `cloud_file_id`
    * A non-empty `cache_folder` entry

    Args:
        candidate (dict): the config candidate to validate
        context_msg (str): context message to append before rasing errors

    Raises:
        ValueError if a config element is invalid

    Returns:
        the config: dict containing the saved/default values
    """

    #
    _, error_msg = credential_folder_path(candidate["credential_folder_path"])
    log_and_exit(error_msg + context_msg) if error_msg else ''

    _, error_msg = cloud_file_id(candidate['cloud_file_id'])
    log_and_exit(error_msg + context_msg) if error_msg else ''

    _, error_msg = is_file_and_exists(candidate['local_file_path'])
    log_and_exit(error_msg + context_msg) if error_msg else ''

    # cache_folder is specified
    assert candidate['cache_folder'] != ''

    return candidate
