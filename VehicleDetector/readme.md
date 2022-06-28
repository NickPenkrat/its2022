1. Обработка данных детекта: запустить yaml_parser.py, ввести путь до папки с данными детекта для каждого кадра в формате YAML. Полученный результат будет сохранен в файлах output.yaml (данные для каждого кадра) и output_track_storage.yaml (словарь объектов и всех принадлежащих им прямоугольников).
2. Визуализация результата: запустить save_data.py, ввести путь до папки с кадрами и YAML-файла с результатом работы yaml-parser.py.
3. Matching треков: 
   1. Предварительно клонировать репозиторий https://github.com/magicleap/SuperGluePretrainedNetwork, переместить в SuperGluePretrainedNetwork файл superGlue/npz_pairs.py и заменить файл assets/scannet_sample_pairs_with_gt.txt на superGlue/scannet_sample_pairs_with_gt.txt.
   2. Выполнить файл set-segments.py, чтобы получить набор сегментов для каждого найденного объекта с камеры.
   3. Выполнить файл npz_pairs.py в репозитории, указав путь к сегментам первой и второй камеры — получится множество NPZ файлов для всех пар сегментов.
   4. Выполнить файл track_matching.py.
   Результатом работы будет файл output_matched.yaml с измененными данными со второй камеры и визуализация этих данных в папке output.