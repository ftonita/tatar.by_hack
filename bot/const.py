from aiogram import types
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton, KeyboardButtonPollType
# State constants
WELCOME_TEXT = """
Привет! Добро пожаловать в Симулятор Татарина

Вы не зарегистрированы в боте!

Придумайте себе никнейм!
"""

NICKNAME_OK_TEXT = """
Регистрация практически закончена..

Жми кнопку, чтобы начать!

"""

SUCCESS_SIGNUP_TEXT = """
👑 Регистрация прошла успешно!
"""

PROFILE_TEXT = """
<b>Профиль</b>

Никнейм: [nickname]

Энергия: 9/10

Баланс: 12345 💰

Уровень: 4.21

Позиция в рейтинге: 1/777
"""

NEW_GAME_REQUEST = 'Ты хочешь начать новую игру?'

NEW_GAME_TEXT = """
<b>Новая игра</b>

Главный приз: 3 000 000 💰

<i>Правила:

- Только один правильный ответ;
- При неправильном ответе игра заканчивается и Вы теряете все заработанные за игру деньги!

<b>Продолжить?</b>
</i>
"""

# - В игре 15 вопросов;
# - На каждый дается по 1 минуте;
# - Вы можете забрать накопленные деньги в любой момент и завершить игру!

START_BUTTON_TEXT = '🚀 Начать'

STUDY_BTN_TEXT = '🎯 Новая игра'
PERS_BTN_TEXT = '🧕 Профиль'
RATING_BNT_TEXT = '🏆 Рейтинг'
SHOP_BTN_TEXT = '🪆 Магазин'
SETTINGS_BTN_TEXT = '⚙️ Настройки'

start_button = KeyboardButton(START_BUTTON_TEXT)
start_markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
start_markup.add(start_button)

main_menu_markup = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)

main_menu_markup.add(STUDY_BTN_TEXT, PERS_BTN_TEXT)
main_menu_markup.add(RATING_BNT_TEXT, SHOP_BTN_TEXT)
main_menu_markup.add(SETTINGS_BTN_TEXT)

new_game_markup = InlineKeyboardMarkup(row_width=2)

new_game_start_btn = InlineKeyboardButton("✅ Старт игры", callback_data='new_game')

new_game_markup.add(new_game_start_btn)

QUESTION = ['Как с татарского переводится слово "ыштан"/шаровары/рубаха/платье/нагрудник', 'Как с татарского переводится "Сүз боткасы"/пустословие/сухоцветы/словосочетание/молчание', 'Как с татарского переводится фразеологизм "Эт булдым"/устал как собака/вот где собака зарыта/а ларчик просто открывался/щенячьи нежности', 'Как с татарского переводится фразеологизм "Шаштыру"/сводить с ума/выходить из себя/надувать губы/души не чаять', "Какой женский аксессуар изображён на фотографии?/чулпы/тастары/серьги/нагрудники/pic1.jpeg", 'Откуда взяты эти строчки "Мин алтын матур чәчәк"?/из песни/из сказки/из поэмы/из стихотворения', "В каком году распалось Казанское ханство?/1552/1550/1450/1616"]