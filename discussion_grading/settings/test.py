"""
Django settings for discussion_grading project to be used in translation commands.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os

BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = os.getenv("DJANGO_SECRET", "open_secret")

# Application definition

INSTALLED_APPS = (
    "statici18n",
    "discussion_grading",
)

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# statici18n
# https://django-statici18n.readthedocs.io/en/latest/settings.html

LOCALE_PATHS = [os.path.join(BASE_DIR, "discussion_grading", "locale")]

LANGUAGES = [
    ("en", "English - Source Language"),
    ("es_419", "Spanish (Latin America)"),
    ("es_ES", "Spanish (Spain)"),
]

STATICI18N_DOMAIN = "text"
STATICI18N_NAMESPACE = "DiscussionGradingI18N"
STATICI18N_PACKAGES = ("discussion_grading",)
STATICI18N_ROOT = "discussion_grading/public/js"
STATICI18N_OUTPUT_DIR = "translations"

# XBlock backends settings
DISCUSSION_GRADING_COMMENTS_BACKEND = "discussion_grading.edxapp_wrapper.backends.comments_q_v1_test"
DISCUSSION_GRADING_SUBMISSIONS_BACKEND = "discussion_grading.edxapp_wrapper.backends.submissions_q_v1_test"
