from config.database import data_collection

WORDS = list(data_collection.find())

ANSWERS = list([word['translate'] for word in WORDS])