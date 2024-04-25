"""
Tests for XBlockDiscussionGrading
"""

from django.test import TestCase
from xblock.fields import ScopeIds
from xblock.test.toy_runtime import ToyRuntime

from discussion_grading import XBlockDiscussionGrading


class TestXBlockDiscussionGrading(TestCase):
    """Tests for XBlockDiscussionGrading"""

    def test_my_student_view(self):
        """Test the basic view loads."""
        scope_ids = ScopeIds("1", "2", "3", "4")
        block = XBlockDiscussionGrading(ToyRuntime(), scope_ids=scope_ids)
        frag = block.student_view()
        as_dict = frag.to_dict()
        content = as_dict["content"]
        self.assertIn(
            '<div class="discussion_grading_block"></div>',
            content,
            "XBlock did not render correct student view",
        )
