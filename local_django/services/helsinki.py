from transformers import pipeline

class HelsinkiTranslationModel:
    """
    Custom translation service using a fine-tuned Hugging Face model that supports multiple languages.
    """

    def __init__(self, model_name="Helsinki-NLP/opus-mt"):
        """
        Initialize the custom translation model.

        :param model_name: The name or path of the multilingual fine-tuned translation model.
        """
        self.translator = pipeline("translation", model=model_name)

    def translate_text(self, text, source_lang, target_lang):
        """
        Translate a given text from the source language to the target language.

        :param text: The text to translate.
        :param source_lang: Source language code (e.g., 'en', 'fr', 'es', 'de').
        :param target_lang: Target language code (e.g., 'fr', 'es', 'de', 'en').
        :return: Translated text.
        """
        translated = self.translator(text, src_lang=source_lang, tgt_lang=target_lang)
        return translated[0]['translation_text']
