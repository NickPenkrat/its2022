Реализация использует пренатренированный алгоритм YOLOv4. Возможна имплементация других алгоритмов трекинга.
Для запуска:
1. Загрузить следующие файлы:
    -- yolo config: https://drive.google.com/file/d/1-GrU7277IyT22CpJO-2jT5FUuYRz3mqJ/view?usp=sharing
    -- yolo weights: https://drive.google.com/file/d/1J1Wzt16LYq2dcgPgZE_yniBL5Ea7g-sl/view?usp=sharing
2. Ввести в консоль путь к папке с названием "images", содержащей изображения в формате PNG.
3. Ввести в консоль путь к YOLO весам и YOLO конфигу.
4. Визуализация работы алгоритма сохраняется в папку "output", данные для каждого кадра в "yaml_files/output.yaml".