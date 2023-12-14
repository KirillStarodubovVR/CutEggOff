import json
import os
import re
from os.path import join as join_path

from text_split import split_by_sentences


class RUAccent:
    def __init__(self):
        self.omographs = None
        self.accents = None
        self.workdir = os.getcwd()

    def load(self, custom_dict=None, custom_homographs=None):

        if custom_homographs is None:
            custom_homographs = {}

        if custom_dict is None:
            custom_dict = {}

        self.omographs = json.load(open(join_path(self.workdir, "dictionaries", "omographs.json"), encoding='utf-8'))

        self.omographs.update(custom_homographs)

        self.accents = json.load(open(join_path(self.workdir, "dictionaries", "accents.json"), encoding='utf-8'))

        self.accents.update(custom_dict)

        # self.yo_words = json.load(open("dictionaries/yo_words.json"), encoding='utf-8')

    def split_by_words(self, string):
        result = re.findall(r"\w*(?:\+\w+)*|[^\w\s]+", string.lower())
        return [res for res in result if res]

    def process_all(self, text):
        sentences = split_by_sentences(text)
        outputs = []
        for sentence in sentences:
            text = self.split_by_words(sentence)
            # processed_text = self._process_yo(text)
            processed_text = self._process_omographs(text)
            processed_text = self._process_accent(processed_text)
            processed_text = " ".join(processed_text)
            processed_text = self.delete_spaces_before_punc(processed_text)
            outputs.append(processed_text)
        return " ".join(outputs)

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
                founded_omographs.append(
                    {"word": word, "variants": variants, "position": i}
                )
        for omograph in founded_omographs:
            splitted_text[
                omograph["position"]
            ] = f"<w>{splitted_text[omograph['position']]}</w>"
            cls = omograph["variants"][0]  # Just take the first variant from the dictionary
            splitted_text[omograph["position"]] = cls
        return splitted_text

    def _process_accent(self, text):
        splitted_text = text

        for i, word in enumerate(splitted_text):
            stressed_word = self.accents.get(word, word)
            splitted_text[i] = stressed_word
        return splitted_text

    def delete_spaces_before_punc(self, text):
        punc = "!\"#$%&'()*,./:;<=>?@[\\]^_`{|}~"
        for char in punc:
            text = text.replace(" " + char, char)
        return text


# Example usage:
ru_accent = RUAccent()
ru_accent.load()

text_to_process = "В этом замке совершенно нет ни одного замка"
processed_text = ru_accent.process_all(text_to_process)

print(processed_text)
