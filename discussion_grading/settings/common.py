"""
Settings for the Discussion Grading XBlock.
"""


def plugin_settings(settings):
    """
    Read / Update necessary common project settings.
    """
    settings.DISCUSSION_GRADING_COMMENTS_BACKEND = "discussion_grading.edxapp_wrapper.backends.comments_q_v1"
    settings.DISCUSSION_GRADING_SUBMISSIONS_BACKEND = "discussion_grading.edxapp_wrapper.backends.submissions_q_v1"
