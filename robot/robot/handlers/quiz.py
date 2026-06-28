import uuid
from telebot import types


MODE_LABELS = {
    "ru_to_zh": "俄语 → 中文",
    "zh_to_ru": "中文 → 俄语",
}

MODE_LABELS_EN = {
    "ru_to_zh": "Russian → English",
    "zh_to_ru": "English → Russian",
}


def register_quiz_handlers(bot, quiz_manager, get_user_level=None, get_user_lang=None):
    quiz_sessions = {}
    quiz_progress = {}
    temp_count = {}

    def resolve_level(user_id):
        return get_user_level(user_id) if get_user_level else None

    def resolve_lang(user_id):
        return get_user_lang(user_id) if get_user_lang else 'zh'

    def ask_quiz_count(chat_id, lang='zh'):
        markup = types.InlineKeyboardMarkup(row_width=2)
        if lang == 'en':
            markup.add(
                types.InlineKeyboardButton("5 Questions", callback_data="quiz_count:5"),
                types.InlineKeyboardButton("10 Questions", callback_data="quiz_count:10"),
                types.InlineKeyboardButton("20 Questions", callback_data="quiz_count:20"),
                types.InlineKeyboardButton("Unlimited", callback_data="quiz_count:0"),
            )
            bot.send_message(chat_id, "🧠 How many questions would you like?", reply_markup=markup)
        else:
            markup.add(
                types.InlineKeyboardButton("5 题", callback_data="quiz_count:5"),
                types.InlineKeyboardButton("10 题", callback_data="quiz_count:10"),
                types.InlineKeyboardButton("20 题", callback_data="quiz_count:20"),
                types.InlineKeyboardButton("无限", callback_data="quiz_count:0"),
            )
            bot.send_message(chat_id, "🧠 想做多少题？", reply_markup=markup)

    def send_mode_menu(chat_id, lang='zh'):
        markup = types.InlineKeyboardMarkup(row_width=1)
        if lang == 'en':
            markup.add(
                types.InlineKeyboardButton("Russian → English", callback_data="quiz_mode:ru_to_zh"),
                types.InlineKeyboardButton("English → Russian", callback_data="quiz_mode:zh_to_ru"),
            )
            bot.send_message(chat_id, "🧠 Select quiz mode:", reply_markup=markup)
        else:
            markup.add(
                types.InlineKeyboardButton("俄语 → 中文", callback_data="quiz_mode:ru_to_zh"),
                types.InlineKeyboardButton("中文 → 俄语", callback_data="quiz_mode:zh_to_ru"),
            )
            bot.send_message(chat_id, "🧠 请选择测验模式：", reply_markup=markup)

    def send_question(chat_id, user_id, mode, lang='zh'):
        progress = quiz_progress.get(user_id)
        if progress and progress["total"] > 0 and progress["current"] >= progress["total"]:
            total = progress["total"]
            correct = progress["correct"]
            percent = int(correct / total * 100) if total > 0 else 0
            if lang == 'en':
                bot.send_message(chat_id, f"🎉 Quiz Complete!\n\n✅ Correct: {correct}/{total}\n📊 Accuracy: {percent}%")
            else:
                bot.send_message(chat_id, f"🎉 本轮测验完成！\n\n✅ 正确：{correct}/{total}\n📊 正确率：{percent}%")
            quiz_progress.pop(user_id, None)
            return

        question = quiz_manager.build_quiz_question(mode=mode, level=resolve_level(user_id), lang=lang)
        if not question:
            if lang == 'en':
                bot.send_message(chat_id, "Not enough words in bank. Need at least 4.")
            else:
                bot.send_message(chat_id, "题库单词不足，至少需要 4 个单词才能生成选择题。")
            return

        question_id = uuid.uuid4().hex[:8]
        quiz_sessions[question_id] = {
            "user_id": user_id,
            "question": question,
        }

        labels = ["A", "B", "C", "D"]
        markup = types.InlineKeyboardMarkup(row_width=1)
        for index, option in enumerate(question["options"]):
            markup.add(
                types.InlineKeyboardButton(
                    f"{labels[index]}. {option}",
                    callback_data=f"quiz_pick:{question_id}:{index}",
                )
            )

        progress_text = ""
        if progress and progress["total"] > 0:
            if lang == 'en':
                progress_text = f"(Question {progress['current'] + 1}/{progress['total']})\n"
            else:
                progress_text = f"（第 {progress['current'] + 1}/{progress['total']} 题）\n"

        mode_label = MODE_LABELS_EN[mode] if lang == 'en' else MODE_LABELS[mode]

        bot.send_message(
            chat_id,
            f"🧠 Quiz: {mode_label}\n{progress_text}\n{question['prompt']}",
            reply_markup=markup,
        )

    @bot.message_handler(commands=["quiz"])
    def handle_quiz_command(message):
        lang = resolve_lang(message.from_user.id)
        ask_quiz_count(message.chat.id, lang)

    @bot.callback_query_handler(func=lambda call: call.data == "quiz_start")
    def handle_quiz_start(call):
        bot.answer_callback_query(call.id)
        lang = resolve_lang(call.from_user.id)
        ask_quiz_count(call.message.chat.id, lang)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("quiz_count:"))
    def handle_quiz_count(call):
        count = int(call.data.split(":")[1])
        bot.answer_callback_query(call.id)
        temp_count[call.from_user.id] = count
        lang = resolve_lang(call.from_user.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        if lang == 'en':
            markup.add(
                types.InlineKeyboardButton("Russian → English", callback_data="quiz_mode:ru_to_zh"),
                types.InlineKeyboardButton("English → Russian", callback_data="quiz_mode:zh_to_ru"),
            )
            bot.edit_message_text("🧠 Select quiz mode:", call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            markup.add(
                types.InlineKeyboardButton("俄语 → 中文", callback_data="quiz_mode:ru_to_zh"),
                types.InlineKeyboardButton("中文 → 俄语", callback_data="quiz_mode:zh_to_ru"),
            )
            bot.edit_message_text("🧠 请选择测验模式：", call.message.chat.id, call.message.message_id, reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("quiz_mode:"))
    def handle_quiz_mode(call):
        mode = call.data.split(":", 1)[1]
        lang = resolve_lang(call.from_user.id)
        if mode not in MODE_LABELS:
            bot.answer_callback_query(call.id, "Unknown mode" if lang == 'en' else "未知测验模式")
            return
        bot.answer_callback_query(call.id)

        user_id = call.from_user.id
        total = temp_count.pop(user_id, 0)
        quiz_progress[user_id] = {"mode": mode, "total": total, "correct": 0, "current": 0}

        start_msg = f"Starting: {MODE_LABELS_EN[mode]}" if lang == 'en' else f"开始测验：{MODE_LABELS[mode]}"
        bot.edit_message_text(start_msg, call.message.chat.id, call.message.message_id)
        send_question(call.message.chat.id, user_id, mode, lang)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("quiz_next:"))
    def handle_next_question(call):
        mode = call.data.split(":", 1)[1]
        bot.answer_callback_query(call.id)

        user_id = call.from_user.id
        lang = resolve_lang(user_id)
        progress = quiz_progress.get(user_id)

        if progress and progress["total"] > 0 and progress["current"] >= progress["total"]:
            total = progress["total"]
            correct = progress["correct"]
            percent = int(correct / total * 100) if total > 0 else 0
            if lang == 'en':
                bot.edit_message_text(
                    f"🎉 Quiz Complete!\n\n✅ Correct: {correct}/{total}\n📊 Accuracy: {percent}%",
                    call.message.chat.id,
                    call.message.message_id,
                )
            else:
                bot.edit_message_text(
                    f"🎉 本轮测验完成！\n\n✅ 正确：{correct}/{total}\n📊 正确率：{percent}%",
                    call.message.chat.id,
                    call.message.message_id,
                )
            quiz_progress.pop(user_id, None)
            return

        send_question(call.message.chat.id, user_id, mode, lang)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("quiz_pick:"))
    def handle_quiz_answer(call):
        _, question_id, index_text = call.data.split(":", 2)
        session = quiz_sessions.pop(question_id, None)
        lang = resolve_lang(call.from_user.id)
        if not session:
            bot.answer_callback_query(call.id, "This question has expired." if lang == 'en' else "这道题已过期，请重新开始。")
            return

        if session["user_id"] != call.from_user.id:
            bot.answer_callback_query(call.id, "This is not your question." if lang == 'en' else "这不是你的题目哦。")
            quiz_sessions[question_id] = session
            return

        question = session["question"]
        choice_index = int(index_text)
        user_answer = question["options"][choice_index]
        is_correct = choice_index == question["correct_index"]

        quiz_manager.save_result(
            user_id=call.from_user.id,
            mode=f"quiz_{question['mode']}",
            ru_word=question["ru_word"],
            zh_word=question["zh_word"],
            user_answer=user_answer,
            correct_answer=question["correct_answer"],
            is_correct=is_correct,
        )

        progress = quiz_progress.get(call.from_user.id)
        if progress:
            progress["current"] += 1
            if is_correct:
                progress["correct"] += 1

        if is_correct:
            result_text = "✅ Correct!" if lang == 'en' else "✅ 回答正确！"
        else:
            if lang == 'en':
                result_text = f"❌ Wrong.\nCorrect answer: {question['correct_answer']}"
            else:
                result_text = f"❌ 回答错误。\n正确答案：{question['correct_answer']}"

        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_next = "Next Question" if lang == 'en' else "下一题"
        btn_switch = "Switch Mode" if lang == 'en' else "切换模式"
        markup.add(
            types.InlineKeyboardButton(btn_next, callback_data=f"quiz_next:{question['mode']}"),
            types.InlineKeyboardButton(btn_switch, callback_data="quiz_start"),
        )
        popup_text = "Correct!" if is_correct and lang == 'en' else ("Wrong!" if lang == 'en' else ("回答正确！" if is_correct else "回答错误"))
        bot.answer_callback_query(call.id, popup_text)
        bot.edit_message_text(
            f"{call.message.text}\n\n{result_text}",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup,
        )

    def reset_user(user_id):
        expired_ids = [qid for qid, session in quiz_sessions.items() if session["user_id"] == user_id]
        for question_id in expired_ids:
            quiz_sessions.pop(question_id, None)
        quiz_progress.pop(user_id, None)
        temp_count.pop(user_id, None)

    return reset_user