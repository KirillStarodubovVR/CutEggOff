# Ударение-Анализатор Текста от команды "ОтрубИ"

![image](https://github.com/KirillStarodubovVR/CutEggOff/assets/89096305/f49c66dc-ffee-4c7a-b9fe-da2c1f259a08)

Разработка алгоритма контекстной расстановки ударений в текстах книг на русском языке и реализация пользовательского интерфейса в рамках учебного хакатона.

## Описание выбранного алгоритма
Этот проект разрабатывается с целью создания алгоритма, способного анализировать тексты книг и автоматически расставлять ударения в словах с учетом контекста. В качестве исходных данных алгоритм получает тек Алгоритм использует словари ударений для определения ударений в словах.

https://drive.google.com/file/d/1JkRfLGDzZ0_nvFSpgAiQJ-zvaH7Z6SQk/view?usp=sharing - Зилязняк основной
https://drive.google.com/file/d/1S93IRMIxuTl16NARJSFv-WNO6zckzwqe/view?usp=sharing - Зилязняк омографы


В основе алгоритма словарь более чем на 3 млн. слов, собранный из [Акцентологического корпуса](https://ruscorpora.ru/corpus/accent) проекта "Национальный корпус русского языка". Словарь содержит все возможные словоформы. Также используется словарь омографов, полученный из того же источника.

### Возможности и ограничения

- Анализ контекста предложения.
- Сравнение слова с предоставленным словарем (словарной статьей).
- Расстановка ударений по тексту книги.
- Выделение многозначных случаев расстановки ударений.
- Выделение слов, для которых невозможно найти ударение в словарях.
- Возможность загрузки дополнительных словарей.

### Добавление нового словаря
Реализована возможность добавить собственный словарь омографов ```omograph_dictionary``` и ударений ```accent_dictionary```
```
ru_accent.load(custom_accent=accent_dictionary, custom_omographs=omograph_dictionary)
```

### Эксперименты с алгоритмом

<hr>
<details>
  <summary>Code details - click to open</summary>
        
```python 

```
</details>
<hr>

## Варианты использования

### Использование в интерпретаторе 
Структура программы выглядит следующим образом:
```bash
│   README.md
│   ruaccent.py
│   text_split.py
│
├───dictionaries
│       .gitattributes
│       accents.json
│       omographs.json
│
├───expand_dict
│   │   all_accents.tsv
│   │   join_dicts.ipynb
│   │   join_dicts.py
│   │   README.md
│   │
│   └───data_from_russian_accentuation
│           wordforms.dat
│
├───test_data
│       test_1_5000.csv
│       test_2_5000.csv
│
└───__pycache__
        text_split.cpython-311.pyc
```
Для корректной работы словари должны быть расположены в папке dictionaries
Для начала работы с ruaccent необходимо создать объект класс RUAccent
```
ru_accent = RUAccent()
```
Реализована возможность добавить собственный словарь омографов ```omograph_dictionary``` и ударений ```accent_dictionary```
```
ru_accent.load(custom_accent=accent_dictionary, custom_omographs=omograph_dictionary)
```
Всё что дальше требуется это загрузить текст в ```ru_accent.process_all(text=your_text)```
И программа вернёт 3 списка. Список из предложений текста с расставленными ударениями, список с омографами и список с неизвестными словами.
```
text_to_process = "В этом замке совершенно нет ни одного замка. Наверно я не буду ругаться с нига из-за этого сучонка"
processed_text = ru_accent.process_all(text_to_process)
print(processed_text)
```
### Развертывание на базе gradio
Попробовать демо-версию алгоритма можно [здесь.](https://huggingface.co/spaces/Shakhovak/RU_ACCENT)

![image](https://github.com/KirillStarodubovVR/CutEggOff/assets/89096305/4d15fab8-e67f-4ee3-86aa-029f079f1c32)

### Развертывание на базе flask

## Дальнейшее развитие проекта
- Можно сделать подсвечивание омографов и неизвестных слов. Добавление в список не только слов, но и контекста.
- Поработать над расширением и обновлением словаря на основе предоставленных Заказчиком.
- Дополнить пользовательский интерфейс



## Вклад в проект

При создании алгоритма команда вдохновлялись решениями:

- :pencil: https://github.com/einhornus/russian_accentuation/
- :pencil: https://github.com/Den4ikAI/ruaccent


## Команда
:stuck_out_tongue_winking_eye:
- Кирилл, Анна - код анализатора текста
- Александр, Андрей, Екатерина, Дмитрий - словари
