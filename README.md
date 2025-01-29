# drawing_3D_-reconstruction
Высчитывает координаты подстанций

Структура проекта:
```python     
|-- docs                    # документация проекта
|
|-- .gitignore              # игнорируемые файлы при коммите в Git
|
|-- Makefile                # хранит команды настройки среды
|
|-- notebook                # хранит интерактивные блокноты
|
|-- README.MD               # Описание проекта
|
|-- src                     # Хранит исходники
|    |- init.py             # Делает src модулем  Python
|    |- config.py           # Хранит конфигурации
|    |- process.py          # обрабатывает данные перед обучением модели
|    |- run_notebook.py     # выполняет блокноты
|    |- train_model.py      # треннирует модель
|
|-- tests
|    |- init.py             # Делает tests модулем  Python
|    |- test_process.py     # Делает src модулем  Python
|    |- test_train_model.py # Делает src модулем  Python
|
|-- requirements.txt        # Необходимые библиотеки