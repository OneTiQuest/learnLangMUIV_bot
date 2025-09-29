import json
from telebot import TeleBot, types
import markups
from query import update_exersise


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
    
    def change(self):
        raise NotImplementedError("Нет дочерней реализации")

"""
Недостающее слово
"""
class MissingWord(Exersise):
    def __init__(self, exersise, bot: TeleBot, user_id):
        super().__init__(exersise, bot, user_id)

    def send_message(self):
        self.bot.send_message(self.user_id, f"<b>Отправьте пропущенное слово:</b>\n\n{self.name}", parse_mode="HTML", reply_markup=markups.remove_markup())

    def change(self):
        def save_data(message):
            if message.content_type != "text":
                self.bot.send_message(self.user_id, f"Неверный формат")
                self.change()
                return
            
            data = {"success_answer": message.text.lower().strip()}
            update_exersise(self.id, json.dumps(data))
            self.bot.send_message(message, f"Правильный ответ успешно изменен ✅", reply_markup=markups.get_next_markup())

        msg = self.bot.send_message(self.user_id, f"Введите недостающее слово для правильного ответа:", reply_markup=markups.remove_markup())
        self.bot.register_next_step_handler(msg, save_data)

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
    
    def change(self):
        def save_success(message):
            if message.content_type != "text":
                self.bot.send_message(self.user_id, f"Неверный формат")

                msg = self.bot.send_message(self.user_id, f"Выберите правильный ответ:", reply_markup=self.gen_markup())
                self.bot.register_next_step_handler(msg, save_success)
            
            if message.text not in self.data.get("answers"):
                self.bot.send_message(self.user_id, f"Выберите ответ из списка")

                msg = self.bot.send_message(self.user_id, f"Выберите правильный ответ:", reply_markup=self.gen_markup())
                self.bot.register_next_step_handler(msg, save_success)
            
            data = {"success_answer": message.text}

            update_exersise(self.id, data)
            self.bot.reply_to(message, f"Правильный ответ успешно изменен ✅", reply_markup=markups.get_next_markup())


        def save_answers(message):
            if message.content_type != "text":
                self.bot.send_message(self.user_id, f"Неверный формат")
                self.change()
                return
            
            answers = [a.lower().strip() for a in message.text.split(",")]
            self.data = {"answers": answers}

            update_exersise(self.id, self.data)
            self.bot.reply_to(message, f"Список ответов успешно изменен ✅")

            msg = self.bot.send_message(self.user_id, f"Выберите правильный ответ:", reply_markup=self.gen_markup())
            self.bot.register_next_step_handler(msg, save_success)

        msg = self.bot.send_message(self.user_id, f"Введите возможные варианты ответа через запятую:", reply_markup=markups.remove_markup())
        self.bot.register_next_step_handler(msg, save_answers)

"""
Аудио
"""
class Audio(Exersise):
    def __init__(self, exersise, bot: TeleBot, user_id):
        super().__init__(exersise, bot, user_id)
    
    def send_message(self):
        if not self.data:
            return super().parse_data()
        
        with open(f"{self.data.get('path')}", 'rb') as audio:
            self.bot.send_message(self.user_id, f"Прослушайте запись")
            self.bot.send_audio(self.user_id, audio, reply_markup=self.gen_markup())

    def change(self):
        def save_data(message):
            if message.content_type != "audio":
                self.bot.send_message(self.user_id, f"Неверный формат")
                self.change()
                return

            try:

                file_info = self.bot.get_file(message.audio.file_id)
                downloaded_file = self.bot.download_file(file_info.file_path)

                filename = f"./media/audio/{message.audio.file_id}.mp3" 
                
                with open(filename, 'wb') as new_file:
                    new_file.write(downloaded_file)

                data = {"path": filename}

                update_exersise(self.id, data)
                self.bot.reply_to(message, f"Контент успешно изменен ✅", reply_markup=markups.get_next_markup())

            except Exception as e:
                self.bot.reply_to(message, f"Ошибка сохранения: {e}")

        msg = self.bot.send_message(self.user_id, f"Отправьте аудиофайл", reply_markup=markups.remove_markup())
        self.bot.register_next_step_handler(msg, save_data)


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
    
    def change(self):
        def save_data(message):
            if message.content_type != "text":
                self.bot.send_message(self.user_id, f"Неверный формат")
                self.change()
                return
            
            data = {
                "content": {
                    "type": "text",
                    "data": message.text
                }
            }
            update_exersise(self.id, data)
            self.bot.reply_to(self.user_id, "Контент успешно изменен ✅", reply_markup=markups.get_next_markup())

        msg = self.bot.send_message(f"Введите текст теоритического упражнения:", reply_markup=markups.remove_markup())
        self.bot.register_next_step_handler(msg, save_data)


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