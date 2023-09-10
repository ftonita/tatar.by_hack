import json
from random import randint
from time import sleep
from aiogram import types
from bot.loader import *
from bot.const import *
from datetime import datetime
from bot import telegramcalendar
from aiogram.types import InputFile
import random

state_list = {}

progress = {}

money = {}

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    id = str(message.from_user.id)
    state_list[id] = 0
    progress[id] = 0
    if await db.verification(message.from_user.id):
        await message.answer(text=WELCOME_TEXT, parse_mode='HTML')
    else:
        await db.add_user(message.from_user.id)
        await message.answer(text=WELCOME_TEXT, parse_mode='HTML')
        
        
@dp.message_handler(lambda m: m.text == STUDY_BTN_TEXT)
async def start_message(message: types.Message):
    id = str(message.from_user.id)
    state_list[id] = 5
    progress[id] = 0
    await bot.send_message(message.from_user.id, NEW_GAME_TEXT, reply_markup=new_game_markup)


@dp.message_handler(content_types="text")
async def text_handler(message: types.Message):
    id = str(message.from_user.id)
    print(state_list[id])
    progress[id] = 0
    if state_list[id] == 0:
        await db.set_user_row(id, 'nickname', message.text)
        state_list[id] = 1
        await bot.send_message(message.from_user.id, NICKNAME_OK_TEXT, reply_markup=start_markup)
    else:
        if message.text == START_BUTTON_TEXT:
            await bot.send_message(message.from_user.id, SUCCESS_SIGNUP_TEXT, reply_markup=main_menu_markup)
            nickname = await db.get_user_row(id, 'nickname')
            profile = PROFILE_TEXT.replace('[nickname]', nickname)
            await bot.send_message(message.from_user.id, profile)
        elif message.text == PERS_BTN_TEXT:
            nickname = await db.get_user_row(id, 'nickname')
            profile = PROFILE_TEXT.replace('[nickname]', nickname)
            await bot.send_message(message.from_user.id, profile)


@dp.callback_query_handler(lambda c: c.data == 'new_game')
async def callback_change_email(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    id = str(callback_query.from_user.id)
    progress[id] = 0
    for i in range(len(QUESTION)):
        if i == progress[id]:
            current_question = QUESTION[i]
            question = current_question.split('/')[0]
            correct_answer = current_question.split('/')[1]
            other_answers = current_question.split('/')[2:5]
            other_answers.append(correct_answer)
            print(other_answers)
            break
    answer_markup = InlineKeyboardMarkup(row_width=2)
    btn_lst = []
    question_text = f"Вопрос №{progress[id] + 1}\n\n❓❓❓ <i>{question}</i>"
    for i in other_answers:
        if i == correct_answer:
            ans_btn = InlineKeyboardButton(text=f'{i}', callback_data='question/true')
        else:
            ans_btn = InlineKeyboardButton(text=f'{i}', callback_data='question/false')
        btn_lst.append(ans_btn) 
    random.shuffle(btn_lst)
    for i in btn_lst:
        answer_markup.insert(i)
    ans_cancel_btn = InlineKeyboardButton('🏳 Сдаться', callback_data='question/surrender')
    answer_markup.add(ans_cancel_btn)
    if len(current_question.split('/')) == 5:
        await bot.send_message(callback_query.from_user.id, question_text, reply_markup=answer_markup, parse_mode='html')
    else:
        filename = current_question.split('/')[5]
        photo = InputFile(f'./images/{filename}')
        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo, caption=question_text, reply_markup=answer_markup)
            

from aiogram.types import ReplyKeyboardRemove

@dp.callback_query_handler(lambda c: 'question' in c.data)
async def callback_change_email(callback_query: types.CallbackQuery):
    await bot.edit_message_text(f'<i>{callback_query.message.text}</i>', callback_query.from_user.id, callback_query.message.message_id)
    id = str(callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)
    if 'true' in callback_query.data:
        progress[id] += 1
        if progress[id] < len(QUESTION):
            next_que = InlineKeyboardMarkup(row_width=1)
            next_button = InlineKeyboardButton("➡️ Следующий вопрос", callback_data='question/next')
            next_que.add(next_button)
            await bot.send_message(callback_query.from_user.id, '🔥 Супер! Это правильный ответ', reply_markup=next_que)
        else:
            await bot.send_message(callback_query.from_user.id, '🎊 Поздравляем!\n\nВы правильно ответили на все вопросы в сегодняшней викторине.\n\nВаше вознаграждение:<b> +3000000 </b>💰', reply_markup=main_menu_markup, parse_mode='HTML')
    elif 'false' in callback_query.data:
        await bot.send_message(callback_query.from_user.id, f'❌ К сожалению, это неправильный ответ!\n\n<b>Игра окончена!</b>\n\nВы дошли до {progress[id]} раунда.', reply_markup=main_menu_markup, parse_mode='HTML')
        progress[id] = 0
    elif 'surrender' in callback_query.data:
        await bot.send_message(callback_query.from_user.id, f'🏳 Вы отказались от вопроса!\n\n<b>Игра окончена!</b>\n\Вы дошли до {progress[id]} раунда.', reply_markup=main_menu_markup, parse_mode='HTML')
        progress[id] = 0
    elif 'next' in callback_query.data:
        for i in range(len(QUESTION)):
            if i == progress[id]:
                current_question = QUESTION[int(i)]
                question = current_question.split('/')[0]
                correct_answer = current_question.split('/')[1]
                other_answers = current_question.split('/')[2:5]
                other_answers.append(correct_answer)
                answer_markup = InlineKeyboardMarkup(row_width=2)
                btn_lst = []
                question_text = f"Вопрос №{progress[id] + 1}\n\n❓❓❓ <i>{question}</i>"
                break
        for i in other_answers:
            if i == correct_answer:
                ans_btn = InlineKeyboardButton(text=f'{i}', callback_data='question/true')
            else:
                ans_btn = InlineKeyboardButton(text=f'{i}', callback_data='question/false')
            btn_lst.append(ans_btn) 
        random.shuffle(btn_lst)
        for i in btn_lst:
            answer_markup.insert(i)
        ans_cancel_btn = InlineKeyboardButton('🏳 Сдаться', callback_data='question/surrender')
        answer_markup.add(ans_cancel_btn)
        if len(current_question.split('/')) == 5:
            await bot.send_message(callback_query.from_user.id, question_text, reply_markup=answer_markup, parse_mode='html')
        else:
            filename = current_question.split('/')[5]
            photo = InputFile(f'./images/{filename}')
            await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo, caption=question_text, reply_markup=answer_markup)
            # await bot.send_message(callback_query.from_user.id, question_text, reply_markup=answer_markup, parse_mode='html')
    state_list[id] = 1