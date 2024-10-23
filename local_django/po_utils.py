import os
import polib
from django.conf import settings


def read_po_file(file_path):
    """
    Read the .po file and extract the messages for translation.

    :param file_path: Path to the .po file.
    :return: A list of tuples with (msgid, msgstr) from the .po file.
    """
    po_file = polib.pofile(file_path)
    messages = [(entry.msgid, entry.msgstr) for entry in po_file]
    return messages


def update_po_file(file_path, translations):
    """
    Update the .po file with translated messages.

    :param file_path: Path to the .po file.
    :param translations: A dictionary of msgid to translated msgstr.
    :return: None
    """
    po_file = polib.pofile(file_path)
    for entry in po_file:
        if entry.msgid in translations:
            entry.msgstr = translations[entry.msgid]
    po_file.save()


def extract_strings(file_path):
    """
    Extract strings that need translation from a .po file.

    :param file_path: Path to the .po file.
    :return: A list of strings to be translated.
    """
    po_file = polib.pofile(file_path)
    strings_to_translate = [entry.msgid for entry in po_file if not entry.msgstr]
    return strings_to_translate


def get_default_po_file_path(language_code='en'):
    """
    Get the default .po file path from the `LOCALE_PATHS` setting in `settings.py`.

    :param language_code: Language code to find the .po file (e.g., 'en', 'fr').
    :return: Path to the .po file if found, None otherwise.
    """
    for locale_path in settings.LOCALE_PATHS:
        po_file_path = os.path.join(locale_path, language_code, 'LC_MESSAGES', 'django.po')
        if os.path.exists(po_file_path):
            return po_file_path
    return None
