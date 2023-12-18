# Ударение-Анализатор Текста от команды "ОтрубИ"

![image](https://github.com/KirillStarodubovVR/CutEggOff/assets/89096305/f49c66dc-ffee-4c7a-b9fe-da2c1f259a08)

Разработка алгоритма контекстной расстановки ударений в текстах книг на русском языке и реализация пользовательского интерфейса в рамках учебного хакатона.

## Описание выбранного алгоритма
Этот проект разрабатывается с целью создания алгоритма, способного анализировать тексты книг и автоматически расставлять ударения в словах с учетом контекста. В качестве исходных данных алгоритм получает текст на русском языке и вовзращает 3 файла: текст с ударениями, список омографов, список ненайденных в словаре слов (см. диаграмму ниже).

![image](https://github.com/KirillStarodubovVR/CutEggOff/assets/89096305/c7047f4c-0a89-4e1a-ad78-abbbed3c640a)

В основе словарей - полная акцентуированная парадигма по А. А. Зализняку, дополненная акцентологическим коррусом проекта "Национальный корпус русского языка" (НКРЯ).

| Словарь | Источник  | Обработанный словарь   |Формат|
| :---:   | :---: | :---: | :---: |
| Зализняк А.А.  и   НКРЯ. Словоформы| [www.speakrus.ru](https://web.archive.org/web/20200705182909/http://www.speakrus.ru/dict/)   [ruscorpora.ru](https://ruscorpora.ru/corpus/accent)| [space](https://huggingface.co/spaces/Shakhovak/RU_accent_flask/resolve/main/dictionaries/file_norm.json?download=true)   |json. Пример: **"абажуром"**:{"accent":"абаж+уром","src_info":"['zaliznyak','russian_accentuation']"}|
| Зализняк А.А.    и    НКРЯ. Омографы| [www.speakrus.ru](https://web.archive.org/web/20200705182909/http://www.speakrus.ru/dict/)          [ruscorpora.ru](https://ruscorpora.ru/corpus/accent)  | [space](https://huggingface.co/spaces/Shakhovak/RU_accent_flask/resolve/main/dictionaries/file_omo.json?download=true)   |json. Пример: **"антициклонами"**:{"acc_variants":"[('+антицикл+онами', ['zaliznyak']), ('антицикл+онами', ['russian_accentuation'])]"}|

### Возможности
- Анализ контекста предложения.
- Сравнение слова с предоставленным словарем (словарной статьей).
- Расстановка ударений по тексту книги.
- Выделение многозначных случаев расстановки ударений.
- Выделение слов, для которых невозможно найти ударение в словарях.
- Возможность загрузки дополнительных словарей.

### Добавление нового словаря
Реализована возможность добавить собственный словарь омографов ```omograph_dictionary``` и ударений ```accent_dictionary```. Словари должны совпадать по формату данных (json), так и по содержанию, как в таблице выше.
```
ru_accent.load(custom_accent=accent_dictionary, custom_omographs=omograph_dictionary)
```

### Ограничения
- Алгоритм работает только с русским языком
- Возможность расстановки ударения ограничено размером словаря
- Не проведена ё-фикация словарей и алгоритма (если слово будет написано с буквой ё или е в разных контекстах, оно будет трактоваться по-разному)
  
### Эксперименты с алгоритмом
Алгоритмы проверялись на тестовых данных (2 выборки по 5 тыс. текстов) - небольших текстах с ударениями, собранных с НКРЯ. В качестве метрики качества был выбрана **accuracy**, которая рассчитывалась как % exact match по словам без учета односложных слов и омографов.

Были проведены следующие эксперименты:
- :hammer_and_wrench: Использование объединенного словаря омографов и словоформ; итеративный поиск ударения на основе выделенно леммы с помощью библиотеки spacy (код можно посмотреть [здесь](https://github.com/KirillStarodubovVR/CutEggOff/tree/anna_branch) в отдельной ветке данного репозитория).
- :hammer_and_wrench: Использование отдельных словарей омографом и словоформ; прямой поиск слов в словарях.


| Алгоритм | Качество   | Комментарий    |
| :---:   | :---: | :---: |
| Сводный словарь  | 66%   | С учетом омографов для проверки итеративности и поиска на основе лемм   |
| Отдельные словари НКРЯ  | 94%   | Без учета омографов, есть риск bias так как выборка из тех же данных, что и словарь   |
| :star: Отдельные словари Зализняк А.А. + НКРЯ  | 90%   | Без учета омографов   |

Был выбран последний алгоритм, так как он более академически выверен и частично снижает bais и потенциальные ошибки в НКРЯ.

## Варианты использования

### Использование в интерпретаторе 

Структура программы в репозитории выглядит следующим образом:

```bash
│   README.md
│   ruaccent.py - основной файл алгоритма
│   text_split.py - разбивка на слова
│   web_interface.py - для запуска UI
|
├───templates - оформление веб-интерфейса
│       index.html
|       result.html
|
├───dictionaries
│       .gitattributes
│       accents.json - словарь словоформ
│       omographs.json - словарь омографов
│   
├───test_data
│       test_1_5000.csv - тестовая выборка на основе НКРЯ
│       test_2_5000.csv - тестовая выборка на основе НКРЯ
|       metrics_review.ipynb - блокнот с расчетом метрики
```
Для корректной работы словари ([словоформы](https://huggingface.co/spaces/Shakhovak/RU_accent_flask/resolve/main/dictionaries/file_norm.json?download=true),[омографы](https://huggingface.co/spaces/Shakhovak/RU_accent_flask/resolve/main/dictionaries/file_omo.json?download=true)) нужно скачать с указанных ссылок в папку dictionaries.

Для начала работы с ruaccent необходимо создать объект класс RUAccent
```
ru_accent = RUAccent()
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
<hr>
<details>
  <summary>Code details - click to open</summary>

</details>
<hr>


## Вклад в проект

При создании алгоритма команда вдохновлялись решениями:

- :pencil: https://github.com/einhornus/russian_accentuation/
- :pencil: https://github.com/Den4ikAI/ruaccent


## Команда
:stuck_out_tongue_winking_eye:
- Кирилл, Анна - код анализатора текста
- Александр, Андрей, Екатерина, Дмитрий - словари
