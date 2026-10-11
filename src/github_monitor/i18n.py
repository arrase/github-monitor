import gettext
from pathlib import Path

DOMAIN = "github_monitor"
LOCALE_DIR = Path(__file__).parent / "locale"

# gettext picks the language from LANGUAGE, LC_ALL, LC_MESSAGES and LANG;
# fallback=True keeps the English source strings when no catalog matches.
translation = gettext.translation(DOMAIN, localedir=LOCALE_DIR, fallback=True)
_ = translation.gettext
ngettext = translation.ngettext
