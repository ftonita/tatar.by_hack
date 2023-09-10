from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import calendar


def create_callback_data(action, year, month, day):
    return ";".join([action, str(year), str(month), str(day)])


def create_calendar(year=None, month=None) -> InlineKeyboardMarkup:
    now = datetime.datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = InlineKeyboardMarkup(row_width=10)
    # First row - Month and Year
    keyboard.row()

    keyboard.add(InlineKeyboardButton(calendar.month_name[month] + " " + str(year), callback_data=data_ignore))
    # keyboard.append(row)
    # Second row - Week Days
    keyboard.row()
    for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        keyboard.insert(InlineKeyboardButton(day, callback_data=data_ignore))

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        keyboard.row()
        for day in week:
            if day == 0:
                keyboard.insert(InlineKeyboardButton(
                    " ", callback_data=data_ignore))
            else:
                keyboard.insert(
                    InlineKeyboardButton(
                        str(day),
                        callback_data=create_callback_data(
                            "DAY", year, month, day),
                    )
                )
        keyboard.row()
    # Last row - Buttons
    keyboard.insert(InlineKeyboardButton("<", callback_data=create_callback_data("PREV-MONTH", year, month, day)))
    keyboard.insert(InlineKeyboardButton(" ", callback_data=data_ignore))
    keyboard.insert(InlineKeyboardButton(">", callback_data=create_callback_data("NEXT-MONTH", year, month, day)))
    # keyboard.append(row)
    keyboard.row()
    return keyboard


async def process_calendar_selection(bot, callback_query):
    ret_data = (False, None)
    query = callback_query
    (action, year, month, day) = query.data.split(";")
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        await bot.answer_callback_query(callback_query_id=query.id)
    elif action == "DAY":
        await bot.edit_message_text(
            text=query.message.text,
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
        )
        ret_data = True, datetime.datetime(int(year), int(month), int(day))
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        await bot.edit_message_text(
            text=query.message.text,
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(pre.year), int(pre.month)),
        )
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        await bot.edit_message_text(
            text=query.message.text,
            chat_id=query.from_user.id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(ne.year), int(ne.month)),
        )
    else:
        await bot.answer_callback_query(
            callback_query_id=query.id, text="Ошибка!"
        )
    return ret_data
