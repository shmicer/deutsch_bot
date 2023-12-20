

class Trainer:

    def __init__(self, user_id, words_to_learn, translate_direction):
        self.user_id = user_id
        self.words_to_learn = words_to_learn
        self.current_word_index = 0
        self.translate_direction = translate_direction

    def get_current_word_list(self):
        my_list = list(self.words_to_learn[self.current_word_index].values())[1:]
        match self.translate_direction:
            case 'de-ru':
                return my_list
            case 'ru-de':
                return my_list[::-1]

    def get_current_word(self):
        return self.get_current_word_list()[0].lower()

    def get_current_translation(self):
        return self.get_current_word_list()[1].lower()

    def check_answer(self, user_answer):
        return user_answer == self.get_current_translation()