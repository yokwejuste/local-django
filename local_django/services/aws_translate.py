import boto3
from django.conf import settings

class AWSClient:
    """
    AWS Translation Client that uses the AWS Translate service.
    """
    def __init__(self):
        self.client = boto3.client(
            'translate',
            aws_access_key_id=settings.AWS_TRANSLATE_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_TRANSLATE_SECRET_ACCESS_KEY,
            region_name=settings.AWS_TRANSLATE_REGION
        )

    def translate_text(self, text, source_lang='en', target_lang='fr'):
        """
        Translate text using AWS Translate.
        :param text: Text to be translated.
        :param source_lang: Source language code.
        :param target_lang: Target language code.
        :return: Translated text.
        """
        response = self.client.translate_text(
            Text=text,
            SourceLanguageCode=source_lang,
            TargetLanguageCode=target_lang
        )
        return response['TranslatedText']
