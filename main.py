import datetime
import telebot
import requests

token = 'tg_token'
bscan_api_key = 'bscan_api_key'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_instructions(message):
    instructions = {"Привет! Отправь мне адрес кошелька на Binance ,"+
          "и я покажу последние 10 транзакций этого кошелька."}
    bot.send_message(message.chat.id, instructions)

@bot.message_handler(func=lambda message: True)
def get_wallet_transactions(message):
    try:
        wallet_address = message.text.strip()

        url = f"https://api.bscscan.com/api?module=account&action=txlist&address={wallet_address}&apikey={bscan_api_key}"
        response = requests.get(url)
        transactions = response.json().get('result', [])

        transaction_list = []
        for txn in transactions[-10:]:
            txn_hash = txn['hash']
            timestamp = datetime.utcfromtimestamp(int(txn['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S')
            transaction_list.append(f"Транзакция: [{txn_hash}]({f'https://bscscan.com/tx/{txn_hash}'}), Время: {timestamp}")

        bot.send_message(message.chat.id, "\n".join(transaction_list), parse_mode='Markdown')
    except Exception as error:
        bot.send_message(message.chat.id, "Произошла ошибка! " + str(error))

bot.polling()