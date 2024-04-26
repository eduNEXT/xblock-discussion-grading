"""This module contains enums used in the Discussion Grading XBlock."""

from enum import Enum

from discussion_grading.utils import _


class DiscussionGradingMethod(Enum):
    """
    Enum for discussion grading method.

    - MINIMUM_PARTICIPATIONS: Learners are graded based on the minimum number of participations
    - AVERAGE_PARTICIPATIONS: Learners are graded based on the average number of participations
    """

    MINIMUM_PARTICIPATIONS = _("Minimum Participations")
    AVERAGE_PARTICIPATIONS = _("Average Participations")
