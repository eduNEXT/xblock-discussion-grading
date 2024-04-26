"""
Discussion Grading Django application initialization.
"""

from django.apps import AppConfig


class DiscussionGradingConfig(AppConfig):
    """
    Configuration for the Discussion Grading Django application.
    """

    name = "discussion_grading"

    plugin_app = {
        "settings_config": {
            "lms.djangoapp": {
                "common": {"relative_path": "settings.common"},
                "test": {"relative_path": "settings.test"},
                "production": {"relative_path": "settings.production"},
            },
            "cms.djangoapp": {
                "common": {"relative_path": "settings.common"},
                "test": {"relative_path": "settings.test"},
                "production": {"relative_path": "settings.production"},
            },
        },
    }
