import os

__all__ = ['get_default_email_address']


def get_default_email_address():
    """
    Try to get user email address from several standard positions.
    """
    # Which one should we use? getpass.getuser() or os.getenv('username')?
    # Another fallback option is to retrive user.email entry from Git config
    # file.
    username = os.getenv('USERNAME')
    userprofile = os.getenv('USERPROFILE')
    return f'{username}@{userprofile}'
