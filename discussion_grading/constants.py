"""This module contains the constants used in the Discussion Grading XBlock."""

from enum import Enum
from discussion_grading.utils import _


class GradingMethod(Enum):
    """
    Enum for discussion grading method.

    - MINIMUM_INTERVENTIONS: Learners are graded based on the minimum number of interventions
    - AVERAGE_INTERVENTIONS: Learners are graded based on the average number of interventions
    """

    MINIMUM_INTERVENTIONS = _("Minimum Interventions")
    AVERAGE_INTERVENTIONS = _("Average Interventions")
