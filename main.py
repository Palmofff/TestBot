import telebot

token = 'tg_toker'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_instructions(message):
    instructions = {"Привет! Отправь мне адрес кошелька на Binance ,"+
          "и я покажу последние 10 транзакций этого кошелька."}
    bot.send_message(message.chat.id, instructions)

bot.polling()