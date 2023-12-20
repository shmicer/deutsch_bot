from config.database import data_collection

DATA = list(data_collection.find())

WORDS = list([word['word'] for word in DATA])
ANSWERS = list([word['translate'] for word in DATA])

TRANSLATE_DIRECTIONS = ['DE-RU', 'RU-DE']