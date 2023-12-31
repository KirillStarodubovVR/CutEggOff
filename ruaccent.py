import json
import os
import re
from os.path import join as join_path

from text_split import split_by_sentences


class RUAccent:
    vowels = "аеёиоуыэюя"

    def __init__(self):
        self.omographs = None
        self.accents = None
        self.workdir = os.getcwd()

    def load(self, custom_accent=None, custom_omographs=None):
        if custom_omographs is None:
            custom_omographs = {}

        if custom_accent is None:
            custom_accent = {}

        self.omographs = json.load(
            open(
                join_path(self.workdir, "dictionaries", "file_omo.json"),
                encoding="utf-8",
            )
        )
        custom_omographs = {
            key: value
            for key, value in custom_omographs.items()
            if key not in self.omographs
        }

        self.omographs.update(custom_omographs)

        self.accents = json.load(
            open(
                join_path(self.workdir, "dictionaries", "file_norm.json"),
                encoding="utf-8",
            )
        )
        custom_accent = {
            key: value
            for key, value in custom_accent.items()
            if key not in self.accents
        }

        self.accents.update(custom_accent)

    def split_by_words(self, string):
        result = re.findall(r"\w*(?:\+\w+)*|[^\w\s]+", string.lower())
        return [res for res in result if res]

    def process_all(self, text):
        """Ядро всей программы. Тут текст проходит через ряд функций,
        где по итогу получается строка с проставленными ударениями
        Input:
        text: string

        Output:
        accented_sentence: list[string]
        omographs_list: list[string]
        unknown_list: list[string]
        """
        accented_sentence = []
        omographs_list = []
        unknown_list = []

        sentences = split_by_sentences(text)
        outputs = []
        for sentence in sentences:
            text = self.split_by_words(sentence)

            founded_omographs = self._process_omographs(text)
            omographs_list.extend(founded_omographs)

            processed_text, unknown_words = self._process_accent(
                text, founded_omographs
            )
            unknown_list.extend(unknown_words)

            processed_text = " ".join(processed_text)
            processed_text = self.delete_spaces_before_punc(processed_text)

            accented_sentence.append(processed_text)

        omographs_list = [
            f"{key}: {value}" for elem in omographs_list for key, value in elem.items()
        ]
        return accented_sentence, list(set(omographs_list)), list(set(unknown_list))

    def _process_yo(self, text):
        splitted_text = text

        for i, word in enumerate(splitted_text):
            splitted_text[i] = self.yo_words.get(word, word)
        return splitted_text

    def _process_omographs(self, text):
        splitted_text = text

        founded_omographs = []
        for i, word in enumerate(splitted_text):
            variants = self.omographs.get(word)
            if variants:
                founded_omographs.append({word: self.omographs[word]["acc_variants"]})

        return founded_omographs

    def _process_accent(self, text, founded_omographs):
        splitted_text = text
        unknown_words = []
        for i, word in enumerate(splitted_text):
            stressed_word = self.accents.get(word, word)

            if stressed_word in [list(d.keys())[0] for d in founded_omographs]:
                splitted_text[i] = word

            elif stressed_word != word:
                splitted_text[i] = stressed_word["accent"]

            else:
                if sum(word.count(vowel) for vowel in RUAccent.vowels) > 1:
                    unknown_words.append(word)
                splitted_text[i] = word

        return splitted_text, unknown_words

    def delete_spaces_before_punc(self, text):
        punc = "!\"#$%&'()*,./:;<=>?@[\\]^_`{|}~"
        for char in punc:
            text = text.replace(" " + char, char)
        return text


# # Example usage:
# ru_accent = RUAccent()
# ru_accent.load()
#
# text_to_process = "В этом замке совершенно нет ни одного замка. Наверно я не буду ругаться с нига нига нига из-за этого сучонка"
# processed_text = ru_accent.process_all(text_to_process)
#
# print(processed_text)
