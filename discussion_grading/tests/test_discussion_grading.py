"""
Tests for XBlockDiscussionGrading
"""

import json
import re
from http import HTTPStatus
from unittest.mock import Mock, patch

from django.test import TestCase
from requests.exceptions import ConnectionError as RequestsConnectionError
from xblock.fields import ScopeIds
from xblock.test.toy_runtime import ToyRuntime

from discussion_grading import XBlockDiscussionGrading
from discussion_grading.discussion_grading import MAX_SCORE, MIN_SCORE, DiscussionGradingMethod


class DiscussionGradingXBlockTestMixin(TestCase):
    """Mixin for the XBlockDiscussionGrading tests."""

    def setUp(self) -> None:
        """Set up the test suite."""
        self.runtime = ToyRuntime()
        self.block = XBlockDiscussionGrading(
            runtime=self.runtime,
            field_data={},
            scope_ids=ScopeIds("1", "2", "3", "4"),
        )

        self.block.grading_method = "discussion"
        self.block.weight = 1
        self.block.max_attempts = None
        self.block.number_of_participations = 1
        self.block.instructions_text = "Instructions"
        self.block.button_text = "Button"
        self.block.attempts = 0
        self.block.raw_score = None
        self.block.submission_uuid = None
        self.block.course_id = "test-course-id"


class TestXBlockDiscussionGrading(DiscussionGradingXBlockTestMixin):
    """Tests for XBlockDiscussionGrading"""

    @patch.object(XBlockDiscussionGrading, "get_weighted_score")
    def test_student_view(self, mock_get_weighted_score: Mock):
        """Test the basic view loads."""
        mock_get_weighted_score.return_value = 0

        fragment = self.block.student_view()

        self.assertIn(
            re.sub("[\n ]", "", fragment.content),
            '<divclass="discussion-grading-block"><p>Instructions</p>'
            '<buttonid="calculate-grade">Button</button>'
            '<pid="score">Yourscoreis:0/1</p>'
            '<pid="error-message"></p></div>',
        )

    @patch.object(XBlockDiscussionGrading, "get_student_item_dict")
    @patch("discussion_grading.discussion_grading.create_submission")
    def test_create_submission(self, mock_create_submission: Mock, mock_get_student_item_dict: Mock):
        """Test the `create_submission` method."""
        user_stats = {"threads": 5, "responses": 3, "replies": 2}
        submission_data = {"uuid": "test-uuid"}
        mock_create_submission.return_value = submission_data
        student_item_dict = {
            "student_id": "student_id",
            "course_id": self.block.block_course_id,
            "item_id": self.block.block_id,
            "item_type": "item_type",
        }
        mock_get_student_item_dict.return_value = student_item_dict

        self.block.create_submission(user_stats)

        mock_create_submission.assert_called_once_with(student_item_dict, user_stats)
        self.assertEqual(self.block.submission_uuid, submission_data["uuid"])

    @patch.object(XBlockDiscussionGrading, "get_student_item_dict")
    @patch("discussion_grading.discussion_grading.get_score")
    def test_get_weighted_score(self, mock_get_score: Mock, mock_get_student_item_dict: Mock):
        """Test the get_weighted_score method."""
        mock_get_student_item_dict.return_value = {
            "student_id": "student_id",
            "course_id": self.block.block_course_id,
            "item_id": self.block.block_id,
            "item_type": "item_type",
        }
        mock_get_score.return_value = {"points_earned": 5}

        result = self.block.get_weighted_score()

        self.assertEqual(result, 5)

        # Test when get_score returns None
        mock_get_score.return_value = None

        result = self.block.get_weighted_score()

        self.assertEqual(result, 0)

    def test_get_score_minimum_participations(self):
        """Test the `get_score` method."""
        self.block.grading_method = DiscussionGradingMethod.MINIMUM_PARTICIPATIONS.name

        # Test when number of participations is greater than or equal to the required number
        user_stats = {"threads": 1, "responses": 1, "replies": 1}
        self.block.number_of_participations = 1

        result = self.block.get_score(user_stats)

        self.assertEqual(result, MAX_SCORE)

        # Test when number of participations is less than the required number
        self.block.number_of_participations = 4

        result = self.block.get_score(user_stats)

        self.assertEqual(result, MIN_SCORE)

    def test_get_score_weighted_participations(self):
        """Test the `get_score` method."""
        self.block.grading_method = DiscussionGradingMethod.WEIGHTED_PARTICIPATIONS.name

        # Test when number of participations is greater than or equal to the required number
        user_stats = {"threads": 1, "responses": 1, "replies": 0}
        self.block.number_of_participations = 1

        result = self.block.get_score(user_stats)

        self.assertEqual(result, MAX_SCORE)

        # Test when number of participations is less than the required number
        self.block.number_of_participations = 3

        result = self.block.get_score(user_stats)

        self.assertEqual(result, 2 / 3)

    @patch("discussion_grading.discussion_grading.XBlockDiscussionGrading.current_user")
    @patch("discussion_grading.discussion_grading.get_username")
    def test_get_user_stats_user_found(self, mock_get_username: Mock, mock_current_user: Mock):
        """Test the `get_user_stats` method when the user is found."""
        mock_get_username.return_value = "test_user"
        mock_current_user.return_value = "test_user"
        course_user_stats = [
            {"username": "test_user", "threads": 2, "responses": 3, "replies": 4},
            {"username": "other_user", "threads": 1, "responses": 2, "replies": 3},
        ]

        result = self.block.get_user_stats(course_user_stats)

        self.assertEqual(result, {"threads": 2, "responses": 3, "replies": 4})

    @patch("discussion_grading.discussion_grading.XBlockDiscussionGrading.current_user")
    @patch("discussion_grading.discussion_grading.get_username")
    def test_get_user_stats_user_not_found(self, mock_get_username: Mock, mock_current_user: Mock):
        """Test the `get_user_stats` method when the user is not found."""
        mock_get_username.return_value = "test_user"
        mock_current_user.return_value = "test_user"
        course_user_stats = [
            {"username": "other_user", "threads": 1, "responses": 2, "replies": 3},
        ]

        result = self.block.get_user_stats(course_user_stats)

        self.assertEqual(result, {})


class TestDiscussionGradingXBlockHandlers(DiscussionGradingXBlockTestMixin):
    """
    Test suite for the MindMapXBlock JSON handlers.
    """

    def setUp(self) -> None:
        """
        Set up the test suite.
        """
        super().setUp()
        self.request = Mock(
            body=json.dumps({}).encode("utf-8"),
            method="POST",
            status_code_success=HTTPStatus.OK,
        )

    def test_calculate_grade_max_attemtps_error(self):
        """Test the `calculate_grade` handler when the maximum number of attempts is reached."""
        self.block.max_attempts = 1
        self.block.attempts = 1

        result = self.block.calculate_grade(self.request)

        self.assertEqual(
            result.json,
            {"success": False, "message": "You have reached the maximum number of attempts."},
        )

    @patch("discussion_grading.discussion_grading.get_course_user_stats")
    def test_calculate_grade_connection_error(self, mock_get_course_user_stats: Mock):
        """Test the `calculate_grade` handler when there is a connection error."""
        self.block.max_attempts = 10
        self.block.attempts = 1
        mock_get_course_user_stats.side_effect = RequestsConnectionError

        result = self.block.calculate_grade(self.request)

        self.assertEqual(
            result.json,
            {"success": False, "message": "Discussion forum is not enabled. Please contact the course team."},
        )

    @patch.object(XBlockDiscussionGrading, "get_user_stats")
    @patch("discussion_grading.discussion_grading.get_course_user_stats")
    def test_calculate_grade_empty_user_stats(self, mock_get_course_user_stats: Mock, mock_get_user_stats: Mock):
        """Test the `calculate_grade` handler when the user stats are not found."""
        mock_get_course_user_stats.return_value = {"user_stats": {}}
        mock_get_user_stats.return_value = {}

        result = self.block.calculate_grade(self.request)

        self.assertEqual(
            result.json,
            {
                "success": False,
                "message": "Forum stats for user not found. Follow the instructions for the course and try again.",
            },
        )

    @patch.object(XBlockDiscussionGrading, "set_score")
    @patch.object(XBlockDiscussionGrading, "create_submission")
    @patch("discussion_grading.discussion_grading.XBlockDiscussionGrading.current_user")
    @patch("discussion_grading.discussion_grading.get_username")
    @patch("discussion_grading.discussion_grading.get_course_user_stats")
    def test_calculate_grade_with_user_stats(
        self,
        mock_get_course_user_stats: Mock,
        mock_get_username: Mock,
        mock_current_user: Mock,
        mock_create_submission: Mock,
        mock_set_score: Mock,
    ):
        """Test the `calculate_grade` handler when the user stats are found."""
        mock_get_course_user_stats.return_value = {
            "user_stats": [{"threads": 1, "responses": 1, "replies": 1, "username": "john_doe"}]
        }
        mock_get_username.return_value = "john_doe"
        mock_current_user.return_value = "test-user"
        mock_create_submission.return_value = None

        result = self.block.calculate_grade(self.request)

        self.assertEqual(result.json, {"success": True})
        self.assertEqual(self.block.attempts, 1)
        mock_set_score.assert_called_once()
        mock_create_submission.assert_called_once()

    @patch.object(XBlockDiscussionGrading, "emit_completion")
    @patch.object(XBlockDiscussionGrading, "set_score")
    @patch.object(XBlockDiscussionGrading, "create_submission")
    @patch("discussion_grading.discussion_grading.XBlockDiscussionGrading.current_user")
    @patch("discussion_grading.discussion_grading.get_username")
    @patch("discussion_grading.discussion_grading.get_course_user_stats")
    def test_calculate_grade_with_user_with_submission_uuid(
        self,
        mock_get_course_user_stats: Mock,
        mock_get_username: Mock,
        mock_current_user: Mock,
        mock_create_submission: Mock,
        mock_set_score: Mock,
        mock_emit_completion: Mock,
    ):
        """Test the `calculate_grade` handler when the user has already submitted."""
        mock_get_course_user_stats.return_value = {
            "user_stats": [{"threads": 1, "responses": 1, "replies": 1, "username": "john_doe"}]
        }
        mock_get_username.return_value = "john_doe"
        mock_current_user.return_value = "test-user"
        self.block.submission_uuid = "test-submission-uuid"

        result = self.block.calculate_grade(self.request)

        self.assertEqual(result.json, {"success": True})
        self.assertEqual(self.block.attempts, 1)
        mock_create_submission.assert_not_called()
        mock_emit_completion.assert_not_called()
        mock_set_score.assert_called_once()
