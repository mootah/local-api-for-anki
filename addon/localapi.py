# -*- coding:utf-8 -*-

import json
from ..base import (WebService, register, export)


@register('Local API')
class LocalAPI(WebService):

    def __init__(self):
        super(LocalAPI, self).__init__()

    def _get_from_api(self):
        url = f'http://127.0.0.1:19634/fastwq/{self.quote_word}'
        data = self.get_response(url)
        try:
            response = json.loads(data)
            return {
                'lemma': response.get('lemma', ''),
                'ipa_word': response.get('ipa_word', ''),
                'ipa_sentence': response.get('ipa_sentence', ''),
                'cefr': response.get('cefr', ''),
                'frequency': response.get('frequency', '')
            }
        except (json.JSONDecodeError, KeyError):
            return {}

    @export('Lemma')
    def fld_lemma(self):
        return self._get_field('lemma')

    @export('Word IPA')
    def fld_ipa_word(self):
        return self._get_field('ipa_word')

    @export('Sentence IPA')
    def fld_ipa_sentence(self):
        return self._get_field('ipa_sentence')

    @export('CEFR')
    def fld_cefr(self):
        return self._get_field('cefr')

    @export('Frequency')
    def fld_frequency(self):
        return self._get_field('frequency')

