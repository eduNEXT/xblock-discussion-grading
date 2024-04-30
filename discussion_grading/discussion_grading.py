"""DiscussionGrading XBlock."""

from __future__ import annotations

import logging
from typing import Optional

import pkg_resources
from django.utils import translation
from requests.exceptions import ConnectionError as RequestsConnectionError
from web_fragments.fragment import Fragment
from xblock.completable import CompletableXBlockMixin
from xblock.core import XBlock
from xblock.fields import Float, Integer, Scope, String
from xblock.utils.resources import ResourceLoader
from xblock.utils.studio_editable import StudioEditableXBlockMixin

from discussion_grading.edxapp_wrapper.comments import get_course_user_stats
from discussion_grading.edxapp_wrapper.submissions import create_submission, get_score, set_score
from discussion_grading.enums import DiscussionGradingMethod
from discussion_grading.utils import _, get_anonymous_user_id, get_username

log = logging.getLogger(__name__)
loader = ResourceLoader(__name__)

ITEM_TYPE = "discussion_grading"
MAX_SCORE = 1
MIN_SCORE = 0


@XBlock.needs("i18n", "user")
class XBlockDiscussionGrading(StudioEditableXBlockMixin, CompletableXBlockMixin, XBlock):
    """
    DiscussionGrading XBlock provides a way to grade discussions in Open edX.
    """

    CATEGORY = "discussion_grading"

    has_score = True
    icon_class = "problem"

    display_name = String(
        display_name=_("Display Name"),
        help=_("The display name for this component."),
        default=_("Discussion Grading"),
        scope=Scope.settings,
    )

    grading_method = String(
        display_name=_("Grading Method"),
        help=_(
            "Defines the grading method to be used. When set to 'Minimum "
            "Participations', the learner will obtain the maximum score if the "
            "number of participations is greater than or equal to the number of "
            "participations required to pass, 0 otherwise. When set to 'Average "
            "Participations', the learner will obtain a score equal to the number "
            "of participations divided by the number of participations required "
            "to pass."
        ),
        values=[
            {"display_name": grading_method.value, "value": grading_method.name}
            for grading_method in DiscussionGradingMethod
        ],
        scope=Scope.settings,
        default=DiscussionGradingMethod.MINIMUM_PARTICIPATIONS.name,
    )

    max_attempts = Integer(
        display_name=_("Maximum Attempts"),
        help=_(
            "Defines the number of times a student can attempt to calculate the "
            "grade. If the value is not set, infinite attempts are allowed."
        ),
        values={"min": 0},
        default=None,
        scope=Scope.settings,
    )

    number_of_participations = Integer(
        display_name=_("Number of Participations"),
        help=_(
            "Defines the number of participations required to pass. If the number "
            "of learner participations is greater than or equal to this value, the "
            "student will pass with the maximum score regardless of the grading method."
        ),
        default=1,
        scope=Scope.settings,
    )

    weight = Integer(
        display_name=_("Problem Weight"),
        help=_(
            "Defines the number of points this problem is worth. If the value is "
            "not set, the problem is worth one point."
        ),
        default=1,
        scope=Scope.settings,
    )

    instructions_text = String(
        display_name=_("Instructions Text"),
        help=_("Defines the instructions text to be displayed to the student."),
        default=_(
            "Please press the button to calculate your grade according to the "
            "number of participations in the discussion forum.",
        ),
        scope=Scope.settings,
    )

    button_text = String(
        display_name=_("Button Text"),
        help=_("Defines the text to be displayed on the button."),
        default=_("Calculate Discussion Participation"),
        scope=Scope.settings,
    )

    attempts = Integer(
        help=_("Number of attempts taken by the student to calculate the grade."),
        default=0,
        scope=Scope.user_state,
    )

    raw_score = Float(
        display_name=_("Raw score"),
        help=_("The raw score for the assignment."),
        default=None,
        scope=Scope.user_state,
    )

    submission_uuid = String(
        display_name=_("Submission UUID"),
        help=_("The submission UUID for the assignment."),
        default=None,
        scope=Scope.user_state,
    )

    editable_fields = [
        "display_name",
        "grading_method",
        "max_attempts",
        "number_of_participations",
        "weight",
        "instructions_text",
        "button_text",
    ]

    def resource_string(self, path: str) -> str:
        """
        Handy helper for getting resources from our kit.

        Args:
            path (str): A path to the resource.

        Returns:
            str: The resource as a string.
        """
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def render_template(self, template_path: str, context: Optional[dict] = None) -> str:
        """
        Render a template with the given context.

        The template is translated according to the user's language.

        Args:
            template_path (str): The path to the template
            context(dict, optional): The context to render in the template

        Returns:
            str: The rendered template
        """
        return loader.render_django_template(template_path, context, i18n_service=self.runtime.service(self, "i18n"))

    @property
    def block_id(self) -> str:
        """
        Return the usage_id of the block.
        """
        return str(self.scope_ids.usage_id)

    @property
    def block_course_id(self) -> str:
        """
        Return the course_id of the block.
        """
        return str(self.course_id)

    @property
    def current_user(self):
        """
        Get the current user.
        """
        return self.runtime.service(self, "user").get_current_user()

    def student_view(self, _context: dict = None) -> Fragment:
        """
        Create primary view of the XBlockDiscussionGrading, shown to students when viewing courses.

        Args:
            context (dict, optional):
                A dict containing data to be used in the view. Defaults to None.

        Returns:
            Fragment: The fragment to be displayed.
        """
        frag = Fragment()

        # Add i18n js
        if statici18n_js_url := self._get_statici18n_js_url():
            frag.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        context = {
            "block": self,
            "weighted_score": self.get_weighted_score(),
        }

        frag.add_content(self.render_template("static/html/discussion_grading.html", context))
        frag.add_css(self.resource_string("static/css/discussion_grading.css"))
        frag.add_javascript(self.resource_string("static/js/src/discussion_grading.js"))
        frag.initialize_js("XBlockDiscussionGrading")
        return frag

    def get_weighted_score(self) -> int:
        """
        Return weighted score for the current user.

        Returns:
            int | None: The weighted score.
        """
        score = get_score(self.get_student_item_dict())
        return score.get("points_earned") if score else 0

    def get_student_item_dict(self) -> dict:
        """
        Return dict required by the submissions app.

        This allows creating and retrieving submissions for a particular student.

        Returns:
            dict: The student item dict.
        """
        return {
            "student_id": get_anonymous_user_id(self.current_user),
            "course_id": self.block_course_id,
            "item_id": self.block_id,
            "item_type": ITEM_TYPE,
        }

    def set_score(self) -> None:
        """
        Set the score for the current user.
        """
        set_score(self.submission_uuid, round(self.raw_score * self.weight), self.weight)

    def create_submission(self, user_stats: dict) -> None:
        """
        Get the submission for the current user.
        """
        submission_data = create_submission(self.get_student_item_dict(), user_stats)
        self.submission_uuid = submission_data.get("uuid")

    def get_score(self, user_stats: dict) -> int | float:
        """
        Get the grade for the current user based on the grading method and number of participations.

        Args:
            user_stats (dict): The number of participations for the current user.

        Returns:
            int | float: The grade for the current user.
        """
        number_of_participations = sum(user_stats.values())

        if number_of_participations >= self.number_of_participations:
            return MAX_SCORE

        if self.grading_method == DiscussionGradingMethod.MINIMUM_PARTICIPATIONS.name:
            return int(number_of_participations >= self.number_of_participations)
        elif self.grading_method == DiscussionGradingMethod.AVERAGE_PARTICIPATIONS.name:
            return number_of_participations / self.number_of_participations

        return MIN_SCORE

    def get_user_stats(self, course_user_stats: dict) -> dict:
        """
        Get the user stats for the current user. If the user is not found, return an empty dict.

        Args:
            course_user_stats (dict): The discussion stats for the course.

        These stats include the number of:
            * threads: learner create a post.
            * responses: learner respond to a post.
            * replies: learner comment on response.

        Example:
        >>> self.get_user_stats()
            {
                "threads": 1,
                "responses": 2,
                "replies": 3,
            }

        Returns:
            dict: The user stats for the current user.
        """
        username = get_username(self.current_user)
        for user_stat in course_user_stats:
            if user_stat.get("username") == username:
                return {
                    "threads": user_stat.get("threads"),
                    "responses": user_stat.get("responses"),
                    "replies": user_stat.get("replies"),
                }

        return {}

    @XBlock.json_handler
    def calculate_grade(self, _data: dict, _suffix: str = "") -> dict:
        """
        Calculate the grade for the student.

        The grading is calculated according to the discussion participations and grading method.

        Args:
            _data (dict): Additional data to be used in the calculation.
            _suffix (str, optional): Suffix for the handler. Defaults to "".

        Returns:
            dict: A dictionary containing the handler result.
        """
        if self.max_attempts and self.attempts >= self.max_attempts:
            return {
                "success": False,
                "message": _("You have reached the maximum number of attempts."),
            }

        try:
            course_user_stats = get_course_user_stats(self.block_course_id).get("user_stats")
        except RequestsConnectionError:
            return {
                "success": False,
                "message": _("Discussion forum is not enabled. Please contact the course team."),
            }

        user_stats = self.get_user_stats(course_user_stats)
        if not user_stats:
            return {
                "success": False,
                "message": _("Forum stats for user not found. Follow the instructions for the course and try again."),
            }

        self.raw_score = self.get_score(user_stats)

        if not self.submission_uuid:
            self.create_submission(user_stats)
            self.emit_completion(1)

        self.set_score()

        self.attempts += 1

        return {
            "success": True,
        }

    @staticmethod
    def workbench_scenarios() -> list[tuple[str, str]]:
        """Create canned scenario for display in the workbench."""
        return [
            (
                "XBlockDiscussionGrading",
                """<discussion_grading/>
             """,
            ),
            (
                "Multiple XBlockDiscussionGrading",
                """<vertical_demo>
                <discussion_grading/>
                <discussion_grading/>
                <discussion_grading/>
                </vertical_demo>
             """,
            ),
        ]

    @staticmethod
    def _get_statici18n_js_url() -> str | None:
        """
        Return the Javascript translation file for the currently selected language, if any.

        Defaults to English if available.
        """
        locale_code = translation.get_language()
        if locale_code is None:
            return None
        text_js = "public/js/translations/{locale_code}/text.js"
        lang_code = locale_code.split("-")[0]
        for code in (translation.to_locale(locale_code), lang_code, "en"):
            if pkg_resources.resource_exists(loader.module_name, text_js.format(locale_code=code)):
                return text_js.format(locale_code=code)
        return None

    @staticmethod
    def get_dummy() -> str:
        """
        Generate initial i18n with dummy method.
        """
        return translation.gettext_noop("Dummy")
