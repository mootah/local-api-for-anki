# -*- coding:utf-8 -*-
import re
import json
import urllib.parse
from ..base import (WebService, register, export)


@register('Local API')
class LocalAPI(WebService):

    def __init__(self):
        super(LocalAPI, self).__init__()
        self._local_word = ''

    @property
    def word(self):
        return self._local_word

    @word.setter
    def word(self, value):
        value = value.replace("<br>", " ")
        value = re.sub(r'</?\w+[^>]*>', '', value)
        self._local_word = value

    @property
    def _quote_word(self):
        return urllib.parse.quote(self._local_word, safe='')

    def _get_from_api(self):
        url = f'http://127.0.0.1:19634/fastwq/{self._quote_word}'
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
