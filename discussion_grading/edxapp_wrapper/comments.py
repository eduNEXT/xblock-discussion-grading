"""
Comments module generalized definitions.
"""

from importlib import import_module

from django.conf import settings


def get_course_user_stats(*args, **kwargs):
    """
    Wrapper for `get_course_user_stats` function in edx-platform.
    """
    backend_function = settings.DISCUSSION_GRADING_COMMENTS_MODULE_BACKEND
    backend = import_module(backend_function)

    return backend.get_course_user_stats(*args, **kwargs)
