import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from local_django.po_utils import update_po_file, extract_strings, get_default_po_file_path
from local_django.translation_manager import TranslationManager


class Command(BaseCommand):
    help = 'Translate .po file messages using the configured translation service (AWS or Azure).'

    def add_arguments(self, parser):
        parser.add_argument(
            'po_file_path',
            type=str,
            nargs='?',
            help='Path to the .po file to be translated. If not provided, the default path from LOCALE_PATHS will be used for all languages.'
        )
        parser.add_argument(
            '--source-lang',
            type=str,
            help='Source language code. If not provided, the source language will be set to settings.LANGUAGE_CODE.'
        )
        parser.add_argument(
            '--target-lang',
            type=str,
            help='Target language code. If not provided, translations will be performed for all languages specified in settings.LANGUAGES.'
        )
        parser.add_argument(
            '--specific-langs',
            type=str,
            nargs='+',
            help='Specify a list of languages (e.g., "fr de es") to translate only these languages. Overrides --target-lang if provided.'
        )

    def handle(self, *args, **options):
        translation_manager = TranslationManager()

        source_lang = options.get('source_lang') or settings.LANGUAGE_CODE

        target_languages = [lang_code for lang_code, _ in settings.LANGUAGES]
        specific_langs = options.get('specific_langs')
        if specific_langs:
            target_languages = specific_langs

        po_file_path = options['po_file_path']

        if not po_file_path:
            for target_lang in target_languages:
                default_po_file_path = get_default_po_file_path(target_lang)
                if default_po_file_path:
                    self.translate_po_file(default_po_file_path, source_lang, target_lang, translation_manager)
                else:
                    self.stdout.write(
                        self.style.WARNING(f"No .po file found for language '{target_lang}' in LOCALE_PATHS."))
        else:
            if not os.path.isfile(po_file_path):
                raise CommandError(f"File '{po_file_path}' does not exist.")
            target_languages = [options['target_lang']] if options['target_lang'] else target_languages
            for target_lang in target_languages:
                self.translate_po_file(po_file_path, source_lang, target_lang, translation_manager)

    def translate_po_file(self, po_file_path, source_lang, target_lang, translation_manager):
        """
        Translates the given .po file from source language to target language.

        :param po_file_path: Path to the .po file.
        :param source_lang: Source language code.
        :param target_lang: Target language code.
        :param translation_manager: Instance of the TranslationManager.
        """
        self.stdout.write(f"Reading .po file: {po_file_path} for language '{target_lang}'...")

        strings_to_translate = extract_strings(po_file_path)

        if not strings_to_translate:
            self.stdout.write(self.style.SUCCESS(f"No strings to translate in '{target_lang}'. Skipping."))
            return

        self.stdout.write(f"Translating {len(strings_to_translate)} strings from {source_lang} to {target_lang}...")

        translations = {}
        for string in strings_to_translate:
            translated_text = translation_manager.translate(string, source_lang, target_lang)
            translations[string] = translated_text
            self.stdout.write(f"Translated '{string}' to '{translated_text}'")

        self.stdout.write(f"Updating .po file: {po_file_path} with translated strings...")
        update_po_file(po_file_path, translations)

        self.stdout.write(
            self.style.SUCCESS(f"Translation completed and .po file updated successfully for '{target_lang}'!"))
