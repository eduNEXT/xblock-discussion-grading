"""DiscussionGrading XBlock."""

from __future__ import annotations

import pkg_resources
from django.utils import translation
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.utils.resources import ResourceLoader


class XBlockDiscussionGrading(XBlock):
    """
    DiscussionGrading XBlock provides a way to grade discussions in Open edX.
    """

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

    def student_view(self, context: dict = None) -> Fragment:
        """
        Create primary view of the XBlockDiscussionGrading, shown to students when viewing courses.

        Args:
            context (dict, optional): A dict containing data to be used in the view. Defaults to None.

        Returns:
            Fragment: The fragment to be displayed.
        """
        if context:
            pass  # TO-DO: do something based on the context.
        html = self.resource_string("static/html/discussion_grading.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/discussion_grading.css"))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(
                self.runtime.local_resource_url(self, statici18n_js_url)
            )

        frag.add_javascript(self.resource_string("static/js/src/discussion_grading.js"))
        frag.initialize_js("XBlockDiscussionGrading")
        return frag

    @staticmethod
    def workbench_scenarios():
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
        for code in (locale_code, lang_code, "en"):
            loader = ResourceLoader(__name__)
            if pkg_resources.resource_exists(
                loader.module_name, text_js.format(locale_code=code)
            ):
                return text_js.format(locale_code=code)
        return None

    @staticmethod
    def get_dummy() -> str:
        """
        Generate initial i18n with dummy method.
        """
        return translation.gettext_noop("Dummy")
