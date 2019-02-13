"""Functions so that the user may input config elements

"""

from functools import wraps

from keypass_sync.config import validate


def with_default(message: str, default_value):
    """Prompt the user, replace empty inputs with default values

    Args:
        message (str): Message to prompt the user with
        default_value (str): Default value to use

    Returns:
        User input if not empty, else the default value
    """
    input_result = input(message + f'\n[{default_value}]: ')
    if input_result == '':
        return default_value
    return input_result


def repeat_ask_until_valid(prompter: callable, validator: callable,
                           *prompt_args):
    """Repeatedly call `prompter` until `validator` validates the output

    If the result is not valid, the validator's indication is shown before
    re-prompting.

    Args:
        prompter (callable): Ask the user for input
        validator (callable): validator for the input given by the user in
            response to `prompter`
        *prompt_args: Arguments to give to the prompter

    Returns:
        Valid user input
    """
    user_input, error_message = validator(prompter(*prompt_args))
    while error_message:
        print(error_message),
        user_input, error_message = validator(prompter(*prompt_args))
    return user_input


def repeat_ask_until_valid_decorator(validator):
    """Turn a regular prompter into a repeat-until-valid one (Decorator)

    Args:
        validator (callable): validator for the input given by the user in
            response to `prompter`

    Returns:
        callable: prompter-until-valid
    """
    def decorator(f):
        @wraps(f)
        def helper(*prompt_args):
            return repeat_ask_until_valid(f, validator, *prompt_args)
        return helper
    return decorator


@repeat_ask_until_valid_decorator(validate.is_file_and_exists)
def credential_file_path(root_path, default):
    """Ask for the path to the google OAuth 2.0 Id file

    Validity: the resulting path should point to an existing file

    Args:
        root_path (str): path to which the file will be copied
        default (str): a default path

    Returns:
        the path
    """
    # Getting credential_file_path
    return with_default(
        f'Path to the "ID clients OAuth 2.0" (a copy will be made '
        f'to {root_path})', default_value=default)


@repeat_ask_until_valid_decorator(validate.is_file_and_exists)
def local_file_path(default):
    """Ask for the path to the database to sync

    Validity: the resulting path should point to an existing file

    Args:
        default (str): a default path

    Returns:
        the path
    """
    return with_default(
        f'Path to keypass database on local machine', default_value=default)


@repeat_ask_until_valid_decorator(validate.cloud_file_id)
def cloud_file_id(default):
    """Ask for the cloud-file's id

    Validity: is not empty

    Args:
        default (str): a default value

    Returns:
        the id
    """
    return with_default(
        f'Id of the file on google drive', default)
