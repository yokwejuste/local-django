import boto3
from django.conf import settings


def translate_text(text, source_lang='en', target_lang='fr'):
    """
    Translate a given text from source language to target language using AWS Translate.

    :param text: Text to be translated.
    :param source_lang: Source language code (e.g., 'en').
    :param target_lang: Target language code (e.g., 'fr').
    :return: Translated text.
    """
    aws_access_key_id = settings.AWS_TRANSLATE_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_TRANSLATE_SECRET_ACCESS_KEY
    region_name = settings.AWS_TRANSLATE_REGION

    client = boto3.client(
        'translate',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_lang,
        TargetLanguageCode=target_lang
    )

    return response['TranslatedText']
