import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOCALE_PATHS = []

TRANSLATION_MANAGER = 'AWS'

AWS_TRANSLATE_ACCESS_KEY_ID = ''
AWS_TRANSLATE_SECRET_ACCESS_KEY = ''
AWS_TRANSLATE_REGION = ''

AZURE_TRANSLATE_KEY = ''
AZURE_TRANSLATE_ENDPOINT = 'https://api.cognitive.microsofttranslator.com/'
