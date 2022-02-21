from email.message import Message
import telebot
from telebot import util
from secrets import TELEGRAM_TOKEN, CHAT_ID

class Telegram_Bot:
    def __init__(self) -> None:
        TOKEN = TELEGRAM_TOKEN
        self.tb = telebot.TeleBot(TOKEN)	#create a new Telegram Bot object

        # Upon calling this function, TeleBot starts polling the Telegram servers for new messages.
        # - interval: int (default 0) - The interval between polling requests
        # - timeout: integer (default 20) - Timeout in seconds for long polling.
        # - allowed_updates: List of Strings (default None) - List of update types to request 
        # self.tb.infinity_polling(interval=0, timeout=20)

        # getMe
        self.user = self.tb.get_me()

        # # getUpdates
        # updates = tb.get_updates()
        # # or
        self.updates = self.tb.get_updates(1234,100,20) #get_Updates(offset, limit, timeout):

    def send_message(self, message):
        # sendMessage
        self.tb.send_message(CHAT_ID, message)
        # self.tb.me

    def new_file(self, course, section, file_name, url):
        # msg = util.types.MessageEntity(util.types.MessageEntity,util.l) 
                # message = f"""
        #     Course = {self.storage.course_name} \n
        #     Section = {self.storage.section_name} \n
        #     File Name = {file_name} \n
        #     Download Link = {url}
        # """
        message = f"""\n
            **קורס** = {course}\n
            **נושא** = {section}\n
            **שם הקובץ** = {file_name}\n
            **לינק** = {url}
        """
        self.tb.send_message(CHAT_ID, message)


############################
    # # setWebhook
    # tb.set_webhook(url="http://example.com", certificate=open('mycert.pem'))
    # # unset webhook
    # tb.remove_webhook()


    

    # # editMessageText
    # tb.edit_message_text(new_text, chat_id, message_id)

    # # forwardMessage
    # tb.forward_message(to_chat_id, from_chat_id, message_id)

    # # All send_xyz functions which can take a file as an argument, can also take a file_id instead of a file.
    # # sendPhoto
    # photo = open('/tmp/photo.png', 'rb')
    # tb.send_photo(chat_id, photo)
    # tb.send_photo(chat_id, "FILEID")

    # # sendAudio
    # audio = open('/tmp/audio.mp3', 'rb')
    # tb.send_audio(chat_id, audio)
    # tb.send_audio(chat_id, "FILEID")

    # ## sendAudio with duration, performer and title.
    # tb.send_audio(CHAT_ID, file_data, 1, 'eternnoir', 'pyTelegram')

    # # sendVoice
    # voice = open('/tmp/voice.ogg', 'rb')
    # tb.send_voice(chat_id, voice)
    # tb.send_voice(chat_id, "FILEID")

    # # sendDocument
    # doc = open('/tmp/file.txt', 'rb')
    # tb.send_document(chat_id, doc)
    # tb.send_document(chat_id, "FILEID")

    # # sendSticker
    # sti = open('/tmp/sti.webp', 'rb')
    # tb.send_sticker(chat_id, sti)
    # tb.send_sticker(chat_id, "FILEID")

    # # sendVideo
    # video = open('/tmp/video.mp4', 'rb')
    # tb.send_video(chat_id, video)
    # tb.send_video(chat_id, "FILEID")

    # # sendVideoNote
    # videonote = open('/tmp/videonote.mp4', 'rb')
    # tb.send_video_note(chat_id, videonote)
    # tb.send_video_note(chat_id, "FILEID")

    # # sendLocation
    # tb.send_location(chat_id, lat, lon)

    # # sendChatAction
    # # action_string can be one of the following strings: 'typing', 'upload_photo', 'record_video', 'upload_video',
    # # 'record_audio', 'upload_audio', 'upload_document' or 'find_location'.
    # tb.send_chat_action(chat_id, action_string)

    # # getFile
    # # Downloading a file is straightforward
    # # Returns a File object
    # import requests
    # file_info = tb.get_file(file_id)

    # file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))

