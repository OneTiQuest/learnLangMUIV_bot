import json
from telebot import TeleBot, types
import markups


class Exersise():
    id: int
    name: str
    data: str
    bot: TeleBot
    user_id: int

    def __init__(self, exersise, bot: TeleBot, user_id):
        self.id = exersise[0]
        self.name = exersise[1]
        self.data = exersise[3]
        self.bot = bot
        self.user_id = user_id

        if self.data:
            self.data = json.loads(self.data)

    def send(self):
        self.send_message()

    def save_data(self):
        pass

    def send_message(self):
        self.bot.send_message(self.user_id, f"<b>{self.name}</b>\n\n{self.parse_data()}", reply_markup=self.gen_markup(), parse_mode="HTML")
        
    def gen_markup(self):
        return markups.get_next_markup()
    
    def parse_data(self):
        if not self.data:
            return 'Данных упражнения нет.'
        
        return self.data

"""
Недостающее слово
"""
class MissingWord(Exersise):
    def __init__(self, exersise, bot: TeleBot, user_id):
        super().__init__(exersise, bot, user_id)

    def send_message(self):
        self.bot.send_message(self.user_id, f"<b>Отправьте пропущенное слово:</b>\n\n{self.name}", parse_mode="HTML", reply_markup=types.ReplyKeyboardRemove())

"""
Правильный вариант
"""
class CorrectOption(Exersise):
    def __init__(self, exersise, bot: TeleBot, user_id):
        super().__init__(exersise, bot, user_id)

    def send_message(self):
        self.bot.send_message(self.user_id, f"<b>Выберите правильный вариант ответа:</b>\n\n{self.name}", reply_markup=self.gen_markup(), parse_mode="HTML")

    def gen_markup(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        for answer in self.data.get("answers"):
            markup.add(types.KeyboardButton(f"{answer}"))

        return markup

"""
Аудио
"""
class Audio(Exersise):
    def __init__(self, exersise, bot: TeleBot, user_id):
        super().__init__(exersise, bot, user_id)
    
    def send_message(self):
        if not self.data:
            return super().parse_data()
        
        with open(f"{self.data.get('path')}/{self.id}.mp3", 'rb') as audio:
            self.bot.send_message(self.user_id, f"Прослушайте запись")
            self.bot.send_audio(self.user_id, audio, reply_markup=self.gen_markup())


"""
О чем говорится в тексте
"""
class WhatText(Exersise):
    def __init__(self, exersise, bot: TeleBot, user_id):
        super().__init__(exersise, bot, user_id)

"""
Теория
"""
class Theory(Exersise):
    def __init__(self, exersise, bot: TeleBot, user_id):
        super().__init__(exersise, bot, user_id)
    
    def parse_data(self):
        if not self.data:
            return super().parse_data()
        
        content_arr = self.data.get("content")
        text = ''

        if content_arr:
            for content in content_arr:
                type_content = content.get("type")
                data_content = content.get("data")

                text += data_content

        return text


# Фабрика с параметром
class ExersiseFactory:
    @staticmethod
    def create_exersise(exersise, bot, user_id) -> Exersise:
        exersise_type = int(exersise[5])

        if exersise_type == 1:
            return MissingWord(exersise, bot, user_id)
        
        elif exersise_type == 2:
            return CorrectOption(exersise, bot, user_id)
        
        elif exersise_type == 3:
            return Audio(exersise, bot, user_id)
        
        elif exersise_type == 4:
            return WhatText(exersise, bot, user_id)
        
        elif exersise_type == 5:
            return Theory(exersise, bot, user_id)
        
        else:
            raise ValueError(f"Неизвестный тип упражнения: {exersise_type}")