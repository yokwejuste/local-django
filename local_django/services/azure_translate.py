from django.conf import settings
import requests

class AzureClient:
    """
    Azure Translation Client that uses the Azure Cognitive Services Translator.
    """
    def __init__(self):
        self.subscription_key = settings.AZURE_TRANSLATE_KEY
        self.endpoint = settings.AZURE_TRANSLATE_ENDPOINT

    def translate_text(self, text, source_lang='en', target_lang='fr'):
        """
        Translate text using Azure Cognitive Services Translator.
        :param text: Text to be translated.
        :param source_lang: Source language code.
        :param target_lang: Target language code.
        :return: Translated text.
        """
        path = '/translate'
        url = f"{self.endpoint}{path}"
        params = {
            'api-version': '3.0',
            'from': source_lang,
            'to': [target_lang]
        }
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key,
            'Content-type': 'application/json'
        }
        body = [{'text': text}]
        response = requests.post(url, params=params, headers=headers, json=body)
        response_json = response.json()
        return response_json[0]['translations'][0]['text']
