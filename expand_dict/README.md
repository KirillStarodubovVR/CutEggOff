Скрипт для объединения 2 словарей ([wordforms](https://github.com/einhornus/russian_accentuation/tree/master) и [all_accents](https://github.com/Koziev/NLP_Datasets/blob/master/Stress/all_accents.zip))

Новый словарь назовется `wordforms_plus_all_accents.dat`

Из-за отсутствия в `all_accents` словоформ и лемм, заполнил их как `''`. Вроде, в коде есть обработчик подобных ситуаций

Результирующий размер словаря примерно в 3 раза больше использованного в статье

Размер словаря превышает
 максимально разрешенный в github, так что сам словарь запушить не удалось
 
Запуск скрипта `cd expand_dict; python3 ./join_dicts.py`