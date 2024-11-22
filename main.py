import telebot
from telebot import types
import glob
import threading
import time
import schedule
import database
import config

API_TOKEN = config.TOKEN

bot = telebot.TeleBot(API_TOKEN)
#logger = logging.Logger()
helloText = "Вас приветствует бот консалтингового Агентства Expert Marketing🚀\n\nДля доступа к чеклисту «Лучшие ценовые стратегии» и полезным материалам для роста бизнеса нажмите кнопку  \"Получить\" 👇"

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    
    photo1 = open('img/Базовый фон.png', 'rb')
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Получить 📚', callback_data='yes');
    markup.add(btn1)
    bot.send_photo(message.from_user.id, photo1, caption=helloText, reply_markup=markup)

    photo1.close()
    
    database.addUser( message.from_user.id, message.date, 1, message.from_user.username)
  
    #записываем пользователя и через 3 дня присылаем ему смску счастья, а потом опять

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        #код сохранения данных, или их обработки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn = types.KeyboardButton(text='Отлично, спасибо!🤝')
        markup.add(btn)
        bot.send_message(call.message.chat.id, 'Эти файлы могут помочь бизнесу вырасти без вложений, за счет собственных ресурсов\n\nРекомендуем ознакомится с каждым 😉')
        send_files(call.message, 'files/mat1/')
        bot.send_message(call.message.chat.id, 'Уверены, эти материалы помогут развить ваш бизнес!', reply_markup= markup)
        

@bot.message_handler(content_types=['text'])
def secondMaterials(message):
    if (message.text == 'Отлично, спасибо!🤝'):
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'И ещё немного материалов для создания качественных презентаций 🤝', reply_markup=markup)
        send_files(message, 'files/mat2/')

def send_files(message, path):
    for filename in glob.glob(f'{path}*.*'):
        with open(filename, 'rb') as f:
            bot.send_document(message.chat.id, f)


def send_spam(id, spam_number):
    text1 = "⚠️Топ-5 ошибок при анализе цен конкурентов⚠️\n\nПривет👋\n\nВы уже начали работать с материалами? Надеемся, что они помогут в вашем бизнесе!\n\n❕Сегодня мы хотим поделиться ещё одной полезной информацией: Топ-5 распространённых ошибок при анализе цен конкурентов, которые могут стоить бизнесу прибыли. Проверьте, не делаете ли вы их:\n\n1️⃣ Сравнение только по цене – важно учитывать не только цену, но и ценность, которую предлагает конкурент\n\n2️⃣ Использование устаревших данных – регулярное обновление информации поможет избежать неправильных выводов\n\n3️⃣ Недооценивание скидок и акций конкурентов – недооценка их влияния на клиентов может привести к потере рынка\n\n4️⃣ Игнорирование динамики рынка – важно отслеживать изменения в ценах, особенно во время сезонных колебаний\n\nПостарайтесь учесть эти моменты при формировании своей стратегии!\n\nЕсли интересно узнать больше о том, как мы можем помочь вашему бизнесу – жми на кнопку 👇"
    text2 = "⚠️Как позиционировать свой продукт по отношению к конкурентам?⚠️\n\nПривет👋\n\n❕Сегодня пара советов о том, что стоит учитывать при позиционировании. Важно, чтобы ваш бизнес выделялся не только ценой. Вот несколько советов, как это сделать:\n\n1️⃣ Фокус на уникальные преимущества – не просто рассказывайте, чем ваш продукт отличается от конкурентов, а показывайте, как он решает проблемы клиентов лучше\n\n2️⃣ Поддержка до и после покупки – чем чаще и понятнее для клиента вы с ним взаимодействуете, тем лучше. Обеспечьте поддержку на всех этапах покупки\n\n3️⃣ Стратегия коммуникации – убедитесь, что каждый ваш канал продвижения, от сайта до рекламы – транслирует одно и то же ключевое сообщение: почему клиенты должны выбрать именно вас\n\nИ помните, ценность всегда побеждает цену, если она чётко донесена до клиента!\n\nЕсли интересно узнать больше о том, как мы можем помочь вашему бизнесу – жми на кнопку 👇"
    

    if spam_number == 1:
        text = text1
        photo = open('img/пост1.png', 'rb')

    elif spam_number == 2:
        text = text2
        photo = open('img/пост2.png', 'rb')
    else:
        return

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Оставить заявку 📬', url="https://ex-ma.ru/fos");
    markup.add(btn1)

    bot.send_photo(id, photo, caption=text, reply_markup=markup)



def spam():
    list_for_spamming = []

    list_for_spamming = database.checkUsers()
    if not list_for_spamming:
        print("пользователей нет лол")
            
    else:
        print("ЮЗЕРЫ ЕСТЬ УРА")
        sym_to_remove = "(),"
        for user in list_for_spamming:
            tmp = str(user[0])
            for char in sym_to_remove:
                tmp = tmp.replace(char, "")
            send_spam(int(tmp), user[1])

def shedule_func():
    schedule.every().minute.do(spam)
    while True:
        time.sleep(1)
        schedule.run_pending()

threading.Thread(target=shedule_func).start()

bot.infinity_polling()