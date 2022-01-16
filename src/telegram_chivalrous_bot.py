from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from pyowm import OWM
from pyowm.caches.lrucache import LRUCache
from Constants import Constants

constants = Constants()

open_weather_map = OWM(Constants.WEATHER_API_KEY)
registry = open_weather_map.city_id_registry()

anyCommand = False


def start(bot, update):
    update.message.reply_text(constants.WELCOME_MESSAGE)


def about(bot, update):
    update.message.reply_text(constants.ABOUT_MESSAGE)


def weather(bot, update):
    global anyCommand

    update.message.reply_text(Constants.COMMAND_WEATHER_QUESTION)
    anyCommand = True


def messages(bot, update):
    global anyCommand

    if anyCommand:
        city = update.message.text.split(',')

        if len(city) == 1:
            city_weather, name = get_weather_info(city[0], -1)
        else:
            city_weather, name = get_weather_info(city[0], city[1])

        degree_sign = u'\N{DEGREE SIGN}'
        weather_status = city_weather.get_status()
        weather_temperature = str(int(city_weather.get_temperature(unit='celsius')['temp']))
        update.message.reply_text(name + '\n' + weather_status + '\n' + weather_temperature + degree_sign + 'C')
        anyCommand = False
    else:
        update.message.reply_text(Constants.ERROR_NOT_SELECTED_COMMAND)


def get_weather_info(city, country):
    if country == -1:
        id_results = registry.ids_for(city, matching='nocase')
    else:
        city = city.strip()
        country = country.strip()
        country = country.upper()
        id_results = registry.ids_for(city, country=country, matching='nocase')

    id = id_results[0][0]
    name = id_results[0][1] + ', ' + id_results[0][2]
    city_weather = open_weather_map.weather_at_id(id).get_weather()
    return city_weather, name


def main():
    updater = Updater(constants.TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler(Constants.COMMAND_START, start))
    dp.add_handler(CommandHandler(Constants.COMMAND_ABOUT, about))
    dp.add_handler(CommandHandler(Constants.COMMAND_WEATHER, weather))

    dp.add_handler(MessageHandler(Filters.text, messages))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
