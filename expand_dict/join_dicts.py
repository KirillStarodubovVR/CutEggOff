import pandas as pd
import pickle
from tqdm import tqdm


def add_accent(text):
    accent_pos = text.find('^')
    return text[:accent_pos] + text[accent_pos+1] + '\u0301' + text[accent_pos+2:]


print('...открываю словари')
with open(file="data_from_russian_accentuation/wordforms.dat", mode='rb') as f:
    wordforms = pickle.loads(f.read())

df = pd.read_csv('all_accents.tsv', sep='\t', names=['word', 'accentuated'])
df['with_accent'] = df['accentuated'].apply(add_accent)

dictionary2add = dict(zip(df['word'], df['with_accent']))
wordforms_keys = set(wordforms.keys())
dictionary2add_keys = set(dictionary2add.keys()).difference(wordforms_keys)

print('...объединяю словари')
for key in tqdm(dictionary2add_keys):
    wordforms[key] = [{'accentuated': dictionary2add[key], 
                        'form': '',
                        'lemma': ''}]

print('...сохраняю результат')
with open('wordforms_plus_all_accents.dat', 'wb') as f:
    pickle.dump(wordforms, f)

print('...готово')