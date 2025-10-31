import json
from telebot import TeleBot, types
from bot.api import HttpClient
import bot.markups as markups


class Exersise:
    id: int
    name: str
    data: str
    bot: TeleBot
    chat_id: int

    def __init__(self, exersise, bot: TeleBot, chat_id):
        self.id = exersise[0]
        self.name = exersise[1]
        self.data = exersise[3]
        self.bot = bot
        self.chat_id = chat_id

        if self.data:
            self.data = json.loads(self.data)

    def send(self):
        self.send_message()

    def save_data(self):
        pass

    def send_message(self):
        self.bot.send_message(
            self.chat_id,
            f"<b>{self.name}</b>\n\n{self.parse_data()}",
            reply_markup=self.gen_markup(),
            parse_mode="HTML",
        )

    def gen_markup(self):
        return markups.get_next_markup()

    def parse_data(self):
        if not self.data:
            return "Данных упражнения нет."

        return self.data

    def change(self):
        raise NotImplementedError("Нет дочерней реализации")


"""
Недостающее слово
"""


class MissingWord(Exersise):
    def send_message(self):
        self.bot.send_message(
            self.chat_id,
            f"<b>Отправьте пропущенное слово:</b>\n\n{self.name}",
            parse_mode="HTML",
            reply_markup=markups.remove_markup(),
        )

    def change(self):
        def save_data(message):
            if message.content_type != "text":
                self.bot.send_message(self.chat_id, f"Неверный формат")
                self.change()
                return

            data = {"success_answer": message.text.lower().strip()}

            http_client = HttpClient(self.chat_id)
            http_client.patch(f"/exercises/{self.id}", data=data)

            self.bot.reply_to(
                message,
                f"Правильный ответ успешно изменен ✅",
                reply_markup=markups.get_next_markup(),
            )

        msg = self.bot.send_message(
            self.chat_id,
            f"Введите недостающее слово для правильного ответа:",
            reply_markup=markups.remove_markup(),
        )
        self.bot.register_next_step_handler(msg, save_data)


"""
Правильный вариант
"""


class CorrectOption(Exersise):
    def send_message(self):
        self.bot.send_message(
            self.chat_id,
            f"<b>Выберите правильный вариант ответа:</b>\n\n{self.name}",
            reply_markup=self.gen_markup(),
            parse_mode="HTML",
        )

    def gen_markup(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        for answer in self.data.get("answers"):
            markup.add(types.KeyboardButton(f"{answer}"))

        return markup

    def change(self):
        def save_success(message):
            if message.content_type != "text":
                self.bot.send_message(self.chat_id, f"Неверный формат")

                msg = self.bot.send_message(
                    self.chat_id,
                    f"Выберите правильный ответ:",
                    reply_markup=self.gen_markup(),
                )
                self.bot.register_next_step_handler(msg, save_success)

            if message.text not in self.data.get("answers"):
                self.bot.send_message(self.chat_id, f"Выберите ответ из списка")

                msg = self.bot.send_message(
                    self.chat_id,
                    f"Выберите правильный ответ:",
                    reply_markup=self.gen_markup(),
                )
                self.bot.register_next_step_handler(msg, save_success)

            data = {"success_answer": message.text}

            http_client = HttpClient(self.chat_id)
            http_client.patch(f"/exercises/{self.id}", data=data)

            self.bot.reply_to(
                message,
                f"Правильный ответ успешно изменен ✅",
                reply_markup=markups.get_next_markup(),
            )

        def save_answers(message):
            if message.content_type != "text":
                self.bot.send_message(self.chat_id, f"Неверный формат")
                self.change()
                return

            answers = [a.lower().strip() for a in message.text.split(",")]
            self.data = {"answers": answers}

            http_client = HttpClient(self.chat_id)
            http_client.patch(f"/exercises/{self.id}", data=self.data)

            self.bot.reply_to(message, f"Список ответов успешно изменен ✅")

            msg = self.bot.send_message(
                self.chat_id,
                f"Выберите правильный ответ:",
                reply_markup=self.gen_markup(),
            )
            self.bot.register_next_step_handler(msg, save_success)

        msg = self.bot.send_message(
            self.chat_id,
            f"Введите возможные варианты ответа через запятую:",
            reply_markup=markups.remove_markup(),
        )
        self.bot.register_next_step_handler(msg, save_answers)


"""
Аудио
"""


class Audio(Exersise):
    def send_message(self):
        if not self.data:
            return super().parse_data()
        try:
            with open(f"{self.data.get('path')}", "rb") as audio:
                self.bot.send_message(self.chat_id, f"Прослушайте запись")
                self.bot.send_audio(self.chat_id, audio, reply_markup=self.gen_markup())
        except Exception as err:
            markups.get_next_markup()

    def change(self):
        def save_data(message):
            if message.content_type != "audio":
                self.bot.send_message(self.chat_id, f"Неверный формат")
                self.change()
                return

            try:

                file_info = self.bot.get_file(message.audio.file_id)
                downloaded_file = self.bot.download_file(file_info.file_path)

                filename = f"./media/audio/{message.audio.file_id}.mp3"

                with open(filename, "wb") as new_file:
                    new_file.write(downloaded_file)

                data = {"path": filename}

                http_client = HttpClient(self.chat_id)
                http_client.patch(f"/exercises/{self.id}", data=data)

                self.bot.reply_to(
                    message,
                    f"Контент успешно изменен ✅",
                    reply_markup=markups.get_next_markup(),
                )

            except Exception as e:
                self.bot.reply_to(message, f"Ошибка сохранения: {e}")

        msg = self.bot.send_message(
            self.chat_id, f"Отправьте аудиофайл", reply_markup=markups.remove_markup()
        )
        self.bot.register_next_step_handler(msg, save_data)


"""
О чем говорится в тексте
"""


class WhatText(Exersise):
    pass


"""
Теория
"""


class Theory(Exersise):
    def parse_data(self):
        if not self.data:
            return super().parse_data()

        content_arr = self.data.get("content")
        text = ""

        if content_arr:
            for content in content_arr:
                type_content = content.get("type")
                data_content = content.get("data")

                text += data_content

        return text

    def change(self):
        def save_data(message):
            if message.content_type != "text":
                self.bot.send_message(self.chat_id, f"Неверный формат")
                self.change()
                return

            data = {"content": [{"type": "text", "data": message.text}]}

            http_client = HttpClient(self.chat_id)
            http_client.patch(f"/exercises/{self.id}", data=data)

            self.bot.reply_to(
                message,
                "Контент успешно изменен ✅",
                reply_markup=markups.get_next_markup(),
            )

        msg = self.bot.send_message(
            self.chat_id,
            f"Введите текст теоритического упражнения:",
            reply_markup=markups.remove_markup(),
        )
        self.bot.register_next_step_handler(msg, save_data)


# Фабрика с параметром
class ExersiseFactory:
    @staticmethod
    def create_exersise(exersise, bot, chat_id) -> Exersise:
        exersise_type = int(exersise[5])

        if exersise_type == 1:
            return MissingWord(exersise, bot, chat_id)

        elif exersise_type == 2:
            return CorrectOption(exersise, bot, chat_id)

        elif exersise_type == 3:
            return Audio(exersise, bot, chat_id)

        elif exersise_type == 4:
            return Theory(exersise, bot, chat_id)

        else:
            raise ValueError(f"Неизвестный тип упражнения: {exersise_type}")
