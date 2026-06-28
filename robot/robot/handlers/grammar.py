from telebot import types


def register_grammar_handlers(bot, quiz_manager, get_user_level=None, get_user_lang=None):
    exercise_sessions = {}

    def resolve_level(user_id):
        return get_user_level(user_id) if get_user_level else None

    def resolve_lang(user_id):
        return get_user_lang(user_id) if get_user_lang else 'zh'

    def start_exercise(chat_id, user_id, lang='zh'):
        exercise = quiz_manager.build_exercise(level=resolve_level(user_id), user_id=user_id, lang=lang)
        if not exercise:
            if lang == 'en':
                bot.send_message(chat_id, "No grammar exercises available right now.")
            else:
                bot.send_message(chat_id, "暂时没有可用的变格/变位练习题。")
            return

        exercise_sessions[user_id] = exercise
        if lang == 'en':
            bot.send_message(
                chat_id,
                "✍️ Grammar Drill\n\n"
                f"{exercise['prompt']}\n\n"
                "Type your answer. Send /cancel to exit.",
            )
        else:
            bot.send_message(
                chat_id,
                "✍️ 变格/变位练习\n\n"
                f"{exercise['prompt']}\n\n"
                "请直接发送答案。发 /cancel 退出。",
            )

    @bot.message_handler(commands=["exercise"])
    def handle_exercise_command(message):
        lang = resolve_lang(message.from_user.id)
        start_exercise(message.chat.id, message.from_user.id, lang)

    @bot.callback_query_handler(func=lambda call: call.data == "exercise_start")
    def handle_exercise_button(call):
        bot.answer_callback_query(call.id)
        lang = resolve_lang(call.from_user.id)
        start_exercise(call.message.chat.id, call.from_user.id, lang)

    @bot.message_handler(func=lambda message: exercise_sessions.get(message.from_user.id) is not None)
    def handle_exercise_answer(message):
        user_id = message.from_user.id
        lang = resolve_lang(user_id)
        answer = (message.text or "").strip()
        exercise = exercise_sessions.pop(user_id)
        is_correct = quiz_manager.check_answer(exercise["answers"], answer)

        quiz_manager.save_result(
            user_id=user_id,
            mode="exercise",
            ru_word=exercise["ru_word"],
            zh_word=exercise["zh_word"],
            user_answer=answer,
            correct_answer=exercise["display_answer"],
            is_correct=is_correct,
        )

        if is_correct:
            result_text = "✅ Correct!" if lang == 'en' else "✅ 回答正确！"
        else:
            if lang == 'en':
                result_text = f"❌ Wrong.\nCorrect answer: {exercise['display_answer']}"
            else:
                result_text = f"❌ 回答错误。\n正确答案：{exercise['display_answer']}"

        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_again = "Next Drill" if lang == 'en' else "再来一题"
        btn_quiz = "Quiz" if lang == 'en' else "去测验"
        markup.add(
            types.InlineKeyboardButton(btn_again, callback_data="exercise_start"),
            types.InlineKeyboardButton(btn_quiz, callback_data="quiz_start"),
        )
        bot.reply_to(message, f"{result_text}\n\n{exercise['explanation']}", reply_markup=markup)

    def reset_user(user_id):
        exercise_sessions.pop(user_id, None)

    return reset_user