"""
Tests for XBlockDiscussionGrading
"""

import re
from unittest.mock import Mock, patch

from django.test import TestCase
from xblock.fields import ScopeIds
from xblock.test.toy_runtime import ToyRuntime

from discussion_grading import XBlockDiscussionGrading


class TestXBlockDiscussionGrading(TestCase):
    """Tests for XBlockDiscussionGrading"""

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
