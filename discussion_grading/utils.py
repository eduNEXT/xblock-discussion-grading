"""
Utilities for controlled navigation xblock.
"""

from discussion_grading.constants import ATTR_KEY_ANONYMOUS_USER_ID, ATTR_KEY_USERNAME


def _(text):
    """
    Make '_' a no-op so we can scrape strings.
    """
    return text


def get_username(user) -> str:
    """
    Get username from user object.

    Args:
        user (XBlockUser): XBlock User object.

    Returns:
        str: Username.
    """
    return user.opt_attrs.get(ATTR_KEY_USERNAME)


def get_anonymous_user_id(user) -> str:
    """
    Get anonymous user id from user object.

    Args:
        user (XBlockUser): XBlock User object.

    Returns:
        str: Anonymous user id.
    """
    return user.opt_attrs.get(ATTR_KEY_ANONYMOUS_USER_ID)
