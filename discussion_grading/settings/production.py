"""
Settings for the Discussion Grading XBlock.
"""


def plugin_settings(settings):
    """
    Read / Update necessary common project settings.
    """
    settings.DISCUSSION_GRADING_COMMENTS_BACKEND = getattr(settings, "ENV_TOKENS", {}).get(
        "DISCUSSION_GRADING_COMMENTS_BACKEND", settings.DISCUSSION_GRADING_COMMENTS_BACKEND
    )
