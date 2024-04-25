"""DiscussionGrading XBlock."""

import pkg_resources
from django.utils import translation
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblockutils.resources import ResourceLoader


class XBlockDiscussionGrading(XBlock):
    """
    DiscussionGrading XBlock provides a way to grade discussions in Open edX.
    """

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        """
        Create primary view of the XBlockDiscussionGrading, shown to students when viewing courses.
        """
        if context:
            pass  # TO-DO: do something based on the context.
        html = self.resource_string("static/html/discussion_grading.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/discussion_grading.css"))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        frag.add_javascript(self.resource_string("static/js/src/discussion_grading.js"))
        frag.initialize_js('XBlockDiscussionGrading')
        return frag

    @staticmethod
    def workbench_scenarios():
        """Create canned scenario for display in the workbench."""
        return [
            ("XBlockDiscussionGrading",
             """<discussion_grading/>
             """),
            ("Multiple XBlockDiscussionGrading",
             """<vertical_demo>
                <discussion_grading/>
                <discussion_grading/>
                <discussion_grading/>
                </vertical_demo>
             """),
        ]

    @staticmethod
    def _get_statici18n_js_url():
        """
        Return the Javascript translation file for the currently selected language, if any.

        Defaults to English if available.
        """
        locale_code = translation.get_language()
        if locale_code is None:
            return None
        text_js = 'public/js/translations/{locale_code}/text.js'
        lang_code = locale_code.split('-')[0]
        for code in (locale_code, lang_code, 'en'):
            loader = ResourceLoader(__name__)
            if pkg_resources.resource_exists(
                    loader.module_name, text_js.format(locale_code=code)):
                return text_js.format(locale_code=code)
        return None

    @staticmethod
    def get_dummy():
        """
        Generate initial i18n with dummy method.
        """
        return translation.gettext_noop("Dummy")
