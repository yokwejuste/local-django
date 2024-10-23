import os

from django.conf import settings

from local_django.po_utils import extract_strings, update_po_file
from local_django.services.aws_translate import AWSClient
from local_django.services.azure_translate import AzureClient

try:
    from local_django.services.helsinki import HelsinkiTranslationModel

    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False


class TranslationManager:
    """
    Manages the translation service to be used (either AWS, Azure, or Custom).
    Ensures that only one service is configured and used at a time.
    """

    def __init__(self):
        self.service = self.get_translation_service()

    def get_translation_service(self):
        """
        Determine which translation service to use based on the `TRANSLATION_MANAGER` setting or configured credentials.

        :return: An instance of the selected translation service.
        """
        translation_manager = getattr(settings, 'TRANSLATION_MANAGER', '').upper()

        if translation_manager == 'AWS':
            if not self.is_aws_configured():
                raise ValueError("AWS is set as the TRANSLATION_MANAGER, but AWS credentials are not configured.")
            return AWSClient()

        elif translation_manager == 'AZURE':
            if not self.is_azure_configured():
                raise ValueError("Azure is set as the TRANSLATION_MANAGER, but Azure credentials are not configured.")
            return AzureClient()

        elif translation_manager == 'CUSTOM':
            if not TRANSFORMERS_AVAILABLE:
                raise ImportError(
                    "The 'transformers' library is not installed. Please install it using `pip install local-django[transformers]`.")
            return HelsinkiTranslationModel()

        elif translation_manager:
            raise ValueError(
                f"Invalid TRANSLATION_MANAGER value '{translation_manager}'. Use 'AWS', 'AZURE', or 'CUSTOM'.")

        # Fallback to automatically detect based on configuration
        if self.is_aws_configured() and not self.is_azure_configured() and TRANSFORMERS_AVAILABLE:
            return AWSClient()
        elif self.is_azure_configured() and not self.is_aws_configured() and TRANSFORMERS_AVAILABLE:
            return AzureClient()
        elif TRANSFORMERS_AVAILABLE and not self.is_aws_configured() and not self.is_azure_configured():
            return HelsinkiTranslationModel()
        else:
            raise ValueError(
                "No valid translation service is configured. Please configure AWS, Azure, or a Custom model in Django settings."
            )

    def is_aws_configured(self):
        """
        Check if AWS credentials are configured.
        """
        return all([
            hasattr(settings, 'AWS_TRANSLATE_ACCESS_KEY_ID'),
            hasattr(settings, 'AWS_TRANSLATE_SECRET_ACCESS_KEY'),
            hasattr(settings, 'AWS_TRANSLATE_REGION')
        ])

    def is_azure_configured(self):
        """
        Check if Azure credentials are configured.
        """
        return all([
            hasattr(settings, 'AZURE_TRANSLATE_KEY'),
            hasattr(settings, 'AZURE_TRANSLATE_ENDPOINT')
        ])

    def translate(self, text, source_lang='en', target_lang='fr'):
        """
        Translate the given text using the configured translation service.
        :param text: Text to be translated.
        :param source_lang: Source language code.
        :param target_lang: Target language code.
        :return: Translated text.
        """
        if not self.service:
            raise ValueError("No translation service is configured.")
        return self.service.translate_text(text, source_lang, target_lang)

    def translate_po_file(self, po_file_path, source_lang='en', target_lang='fr'):
        """
        Translate the content of a single .po file using the configured translation service.

        :param po_file_path: Path to the .po file.
        :param source_lang: Source language code.
        :param target_lang: Target language code.
        """
        # Check if the .po file exists
        if not os.path.isfile(po_file_path):
            raise FileNotFoundError(f"The .po file at '{po_file_path}' does not exist.")

        print(f"Reading .po file: {po_file_path}...")
        strings_to_translate = extract_strings(po_file_path)

        if not strings_to_translate:
            print("No strings found to translate. Exiting.")
            return

        print(f"Translating {len(strings_to_translate)} strings from {source_lang} to {target_lang}...")

        translations = {}
        for string in strings_to_translate:
            translated_text = self.translate(string, source_lang, target_lang)
            translations[string] = translated_text
            print(f"Translated: '{string}' -> '{translated_text}'")

        print(f"Updating .po file: {po_file_path} with translated strings...")
        update_po_file(po_file_path, translations)
        print("Translation completed and .po file updated successfully!")

    def translate_all(self, source_lang='en', target_lang='fr'):
        """
        Translate all .po files in the LOCALE_PATHS directory using the configured translation service.

        :param source_lang: Source language code.
        :param target_lang: Target language code.
        """
        locale_paths = getattr(settings, 'LOCALE_PATHS', [])

        if not locale_paths:
            raise ValueError("No LOCALE_PATHS defined in Django settings.")

        print(f"Translating all .po files in LOCALE_PATHS using {self.service.__class__.__name__}...")

        for locale_path in locale_paths:
            for root, dirs, files in os.walk(locale_path):
                for file in files:
                    if file.endswith(".po"):
                        po_file_path = os.path.join(root, file)
                        print(f"Translating file: {po_file_path}")
                        self.translate_po_file(po_file_path, source_lang, target_lang)
