

class Trainer:
    def __init__(self, user_id, words_to_learn):
        self.user_id = user_id
        self.words_to_learn = words_to_learn
        self.current_word_index = 0

    def get_current_word(self):
        return self.words_to_learn[self.current_word_index]

    def get_current_translation(self):
        return self.get_current_word()['translate'].lower()

    def check_answer(self, user_answer):
        return user_answer == self.get_current_translation()