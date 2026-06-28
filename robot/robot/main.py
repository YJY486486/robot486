import telebot
from telebot import types
from database.db_manager import DatabaseManager
from handlers.grammar import register_grammar_handlers
from handlers.quiz import register_quiz_handlers
from managers.quiz_manager import QuizManager
from managers.mistake_manager import MistakeManager

# 负责人 Token
TOKEN = '8712720637:AAE-ZK-13eC5x5eatyf_NWr8c1JhpIJ_Cf4'


class RusHelperBot:
    def __init__(self):
        self.bot = telebot.TeleBot(TOKEN)
        self.db = DatabaseManager()
        self.mistake_manager = MistakeManager(self.db)
        self.quiz_manager = QuizManager(self.db, mistake_manager=self.mistake_manager)
        self.user_states = {}
        self.temp_study_data = {}
        self.module_resetters = []
        self.mistake_sessions = {}
        self.user_lang = {}
        self._setup_handlers()

    def _setup_handlers(self):
        # --- [0] 公共逻辑提取：展示生词本 ---
        def show_my_vocabulary(chat_id, user_id):
            words = self.db.get_user_words(user_id)
            lang = self.user_lang.get(user_id, 'zh')
            if lang == 'en':
                empty_msg = "Your vocabulary is empty. Add some words!"
                title = "📖 --- Your Vocabulary --- 📖\n\n"
                flag = "🇬🇧"
            else:
                empty_msg = "您的生词本还是空的哦，快去添加吧！"
                title = "📖 --- 您的生词本 --- 📖\n\n"
                flag = "🇨🇳"

            if not words:
                self.bot.send_message(chat_id, empty_msg)
            else:
                response = title
                for i, (ru, zh) in enumerate(words, 1):
                    response += f"{i}. 🇷🇺 {ru}  ➡️  {flag} {zh}\n"
                self.bot.send_message(chat_id, response)

        # --- [1] 指令处理器 ---

        @self.bot.message_handler(commands=['view_words'])
        def handle_view_cmd(message):
            show_my_vocabulary(message.chat.id, message.from_user.id)

        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            user = message.from_user
            self.db.save_user(user.id, user.username, user.first_name)
            self.bot.reply_to(message, f"你好，{user.first_name}！我是俄语助手机器人。\n输入 /help 查看主菜单。")

        @self.bot.message_handler(commands=['help'])
        def handle_help(message):
            lang = self.user_lang.get(message.from_user.id, 'zh')
            markup = types.InlineKeyboardMarkup(row_width=2)

            if lang == 'en':
                title = "--- 🤖 Bot Menu ---"
                btn_lang = types.InlineKeyboardButton("🌐 Language", callback_data="set_lang")
                btn_level = types.InlineKeyboardButton("📊 My Level", callback_data="show_level_menu")
                btn_add = types.InlineKeyboardButton("➕ Vocabulary", callback_data="add_word_start")
                btn_view = types.InlineKeyboardButton("📖 My Words", callback_data="view_words")
                btn_help = types.InlineKeyboardButton("❓ HELP", callback_data="get_help")
                btn_study = types.InlineKeyboardButton("📚 Word Study", callback_data="study_words")
                btn_exercise = types.InlineKeyboardButton("✍️ Grammar Drill", callback_data="exercise_start")
                btn_quiz = types.InlineKeyboardButton("🧠 Quiz", callback_data="quiz_start")
                btn_review = types.InlineKeyboardButton("🔄 Review Mistakes", callback_data="review_mistakes")
            else:
                title = "--- 🤖 机器人功能菜单 ---"
                btn_lang = types.InlineKeyboardButton("🌐 语言设置（Language）", callback_data="set_lang")
                btn_level = types.InlineKeyboardButton("📊 我的水平", callback_data="show_level_menu")
                btn_add = types.InlineKeyboardButton("➕ 生词本", callback_data="add_word_start")
                btn_view = types.InlineKeyboardButton("📖 查看生词本", callback_data="view_words")
                btn_help = types.InlineKeyboardButton("❓ HELP", callback_data="get_help")
                btn_study = types.InlineKeyboardButton("📚 单词学习", callback_data="study_words")
                btn_exercise = types.InlineKeyboardButton("✍️ 变格练习", callback_data="exercise_start")
                btn_quiz = types.InlineKeyboardButton("🧠 随机测验", callback_data="quiz_start")
                btn_review = types.InlineKeyboardButton("🔄 专注错题", callback_data="review_mistakes")

            markup.add(btn_lang, btn_level, btn_add, btn_view, btn_help, btn_study, btn_exercise, btn_quiz, btn_review)
            self.bot.send_message(message.chat.id, title, reply_markup=markup)

        @self.bot.message_handler(commands=['level'])
        def quick_check_level(message):
            level = self.db.get_user_level(message.from_user.id)
            lang = self.user_lang.get(message.from_user.id, 'zh')
            if lang == 'en':
                self.bot.reply_to(message, f"🔍 Your current level: {level}")
            else:
                self.bot.reply_to(message, f"🔍 您当前的记录水平为：{level}")

        @self.bot.message_handler(commands=['cancel'])
        def handle_cancel(message):
            self.user_states[message.from_user.id] = None
            for reset in self.module_resetters:
                reset(message.from_user.id)
            lang = self.user_lang.get(message.from_user.id, 'zh')
            if lang == 'en':
                self.bot.reply_to(message, "Cancelled.")
            else:
                self.bot.reply_to(message, "已退出当前状态。")

        self.module_resetters.extend([
            register_grammar_handlers(self.bot, self.quiz_manager, get_user_level=self.db.get_user_level,
                                      get_user_lang=self.user_lang.get),
            register_quiz_handlers(self.bot, self.quiz_manager, get_user_level=self.db.get_user_level,
                                   get_user_lang=self.user_lang.get),
        ])

        # --- [2] 按钮回调处理器 ---

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            user_id = call.from_user.id
            lang = self.user_lang.get(user_id, 'zh')

            if call.data == "show_level_menu":
                self.bot.answer_callback_query(call.id)
                level = self.db.get_user_level(user_id)
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton("Beginner A0", callback_data="setlv_A0"),
                    types.InlineKeyboardButton("Elementary A1", callback_data="setlv_A1"),
                    types.InlineKeyboardButton("Intermediate A2", callback_data="setlv_A2")
                )
                if lang == 'en':
                    msg = f"Your level: {level}\nSelect new level:"
                else:
                    msg = f"您当前等级：{level}\n请选择修改："
                self.bot.send_message(call.message.chat.id, msg, reply_markup=markup)

            elif call.data.startswith("setlv_"):
                new_level = call.data.split("_")[1]
                self.db.update_user_level(user_id, new_level)
                self.bot.answer_callback_query(call.id, "OK!" if lang == 'en' else "成功！")
                if lang == 'en':
                    self.bot.edit_message_text(f"✅ Level set to: {new_level}", call.message.chat.id,
                                               call.message.message_id)
                else:
                    self.bot.edit_message_text(f"✅ 等级已设为：{new_level}", call.message.chat.id,
                                               call.message.message_id)

            elif call.data == "add_word_start":
                self.bot.answer_callback_query(call.id)
                self.user_states[user_id] = 'AWAITING_WORD'
                if lang == 'en':
                    self.bot.send_message(call.message.chat.id,
                                          "Enter word in format:\nRussian,Chinese\n(e.g. Привет,Hello)\nSend /cancel to exit.")
                else:
                    self.bot.send_message(call.message.chat.id,
                                          "请输入要添加的单词，格式为：\n俄语,中文\n(例如: Привет,你好)\n退出请发 /cancel")

            elif call.data == "set_lang":
                self.bot.answer_callback_query(call.id)
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(
                    types.InlineKeyboardButton("🇨🇳 中文", callback_data="lang_zh"),
                    types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
                )
                self.bot.send_message(call.message.chat.id, "🌐 请选择学习语言 / Choose language:", reply_markup=markup)

            elif call.data.startswith("lang_"):
                lang = call.data.split("_")[1]
                self.user_lang[user_id] = lang
                self.bot.answer_callback_query(call.id, "OK!" if lang == 'en' else "设置成功！")
                lang_name = "中文" if lang == "zh" else "English"
                self.bot.edit_message_text(f"✅ 学习语言已设为：{lang_name}", call.message.chat.id,
                                           call.message.message_id)

            elif call.data == "view_words":
                self.bot.answer_callback_query(call.id)
                show_my_vocabulary(call.message.chat.id, user_id)

            elif call.data == "get_help":
                self.bot.answer_callback_query(call.id)
                if self.user_lang.get(user_id, 'zh') == 'en':
                    self.bot.send_message(call.message.chat.id,
                                          "I'm your Russian learning assistant.\n"
                                          "Switch language anytime via 🌐 Language Settings."
                                          )
                else:
                    self.bot.send_message(call.message.chat.id,
                                          "我是你的俄语助手。\n随时点击 🌐 语言设置 切换语言。"
                                          )

            elif call.data == "study_words":
                self.bot.answer_callback_query(call.id)
                user_level = self.db.get_user_level(user_id)

                if user_level == '未设置' or self.db.get_word_count_by_level(user_level) < 10:
                    words = self.db.get_random_words(50)
                    if lang == 'en':
                        level_info = "(All levels)"
                    else:
                        level_info = "（使用全部词库）"
                else:
                    words = self.db.get_random_words(50, user_level)
                    if lang == 'en':
                        level_info = f"(Based on your {user_level} level)"
                    else:
                        level_info = f"（根据您的 {user_level} 等级推荐）"

                if not words:
                    if lang == 'en':
                        self.bot.send_message(call.message.chat.id, "📚 Word bank is empty. Please contact admin.")
                    else:
                        self.bot.send_message(call.message.chat.id, "📚 单词库暂时为空，请联系管理员。")
                    return

                self.temp_study_data[user_id] = words

                page_size = 10
                total_pages = (len(words) + page_size - 1) // page_size
                flag = "🇬🇧" if lang == "en" else "🇨🇳"

                if lang == 'en':
                    response = f"📖 --- Word Study {level_info} --- 📖\n\n"
                    response += f"📚 Page 1/{total_pages}\n"
                else:
                    response = f"📖 --- 单词学习 {level_info} --- 📖\n\n"
                    response += f"📚 第 1/{total_pages} 页\n"
                response += "─" * 20 + "\n"

                for i, word in enumerate(words[:10], 1):
                    ru = word[0]
                    if lang == 'en':
                        translation = word[2] if len(word) > 2 and word[2] else word[1]
                    else:
                        translation = word[1]
                    response += f"{i}. 🇷🇺 {ru}  →  {flag} {translation}\n"

                if lang == 'en':
                    response += "\n💡 Click buttons below to navigate"
                else:
                    response += "\n💡 点击下方按钮翻页"

                markup = types.InlineKeyboardMarkup(row_width=2)
                if total_pages > 1:
                    btn_next = "Next ▶️" if lang == 'en' else "下一页 ▶️"
                    markup.add(types.InlineKeyboardButton(btn_next, callback_data="study_page_1"))
                btn_back = "🔙 Menu" if lang == 'en' else "🔙 返回菜单"
                markup.add(types.InlineKeyboardButton(btn_back, callback_data="back_to_menu"))

                self.bot.send_message(call.message.chat.id, response, reply_markup=markup)

            elif call.data.startswith("study_page_"):
                self.bot.answer_callback_query(call.id)
                page_num = int(call.data.split("_")[2])

                if user_id not in self.temp_study_data:
                    if lang == 'en':
                        self.bot.send_message(call.message.chat.id, "Session expired. Please start again.")
                    else:
                        self.bot.send_message(call.message.chat.id, "会话已过期，请重新开始学习。")
                    return

                words = self.temp_study_data[user_id]
                page_size = 10
                total_pages = (len(words) + page_size - 1) // page_size

                start = page_num * page_size
                end = min(start + page_size, len(words))
                page_words = words[start:end]
                flag = "🇬🇧" if lang == "en" else "🇨🇳"

                if lang == 'en':
                    response = f"📖 --- Word Study --- 📖\n\n"
                    response += f"📚 Page {page_num + 1}/{total_pages}\n"
                else:
                    response = f"📖 --- 单词学习 --- 📖\n\n"
                    response += f"📚 第 {page_num + 1}/{total_pages} 页\n"
                response += "─" * 20 + "\n"

                for i, word in enumerate(page_words, start + 1):
                    ru = word[0]
                    if lang == 'en':
                        translation = word[2] if len(word) > 2 and word[2] else word[1]
                    else:
                        translation = word[1]
                    response += f"{i}. 🇷🇺 {ru}  →  {flag} {translation}\n"

                if lang == 'en':
                    response += "\n💡 Click buttons below to navigate"
                else:
                    response += "\n💡 点击下方按钮翻页"

                markup = types.InlineKeyboardMarkup(row_width=2)
                if page_num > 0:
                    btn_prev = "◀️ Prev" if lang == 'en' else "◀️ 上一页"
                    markup.add(types.InlineKeyboardButton(btn_prev, callback_data=f"study_page_{page_num - 1}"))
                if page_num < total_pages - 1:
                    btn_next = "Next ▶️" if lang == 'en' else "下一页 ▶️"
                    markup.add(types.InlineKeyboardButton(btn_next, callback_data=f"study_page_{page_num + 1}"))
                btn_back = "🔙 Menu" if lang == 'en' else "🔙 返回菜单"
                markup.add(types.InlineKeyboardButton(btn_back, callback_data="back_to_menu"))

                self.bot.edit_message_text(response, call.message.chat.id, call.message.message_id, reply_markup=markup)

            elif call.data == "review_mistakes":
                self.bot.answer_callback_query(call.id)
                user_id = call.from_user.id
                if not self.mistake_manager.has_mistakes(user_id):
                    if lang == 'en':
                        self.bot.send_message(call.message.chat.id, "🎉 No mistakes to review. Keep it up!")
                    else:
                        self.bot.send_message(call.message.chat.id, "🎉 暂时没有需要复习的错题，继续保持！")
                    return

                question = self.quiz_manager.build_quiz_question(mode="ru_to_zh", user_id=user_id)
                if not question:
                    if lang == 'en':
                        self.bot.send_message(call.message.chat.id, "Not enough words in bank.")
                    else:
                        self.bot.send_message(call.message.chat.id, "题库单词不足。")
                    return

                self.mistake_sessions[user_id] = question

                labels = ["A", "B", "C", "D"]
                markup = types.InlineKeyboardMarkup(row_width=1)
                for i, opt in enumerate(question["options"]):
                    markup.add(types.InlineKeyboardButton(f"{labels[i]}. {opt}", callback_data=f"mistake_pick:{i}"))

                if lang == 'en':
                    self.bot.send_message(call.message.chat.id, f"🔄 Mistake Review\n\n{question['prompt']}",
                                          reply_markup=markup)
                else:
                    self.bot.send_message(call.message.chat.id, f"🔄 错题复习\n\n{question['prompt']}",
                                          reply_markup=markup)

            elif call.data.startswith("mistake_pick:"):
                self.bot.answer_callback_query(call.id)
                choice_index = int(call.data.split(":")[1])

                question = self.mistake_sessions.get(user_id)
                if not question:
                    if lang == 'en':
                        self.bot.edit_message_text("Question expired. Please start again.", call.message.chat.id,
                                                   call.message.message_id)
                    else:
                        self.bot.edit_message_text("题目已过期，请重新开始。", call.message.chat.id,
                                                   call.message.message_id)
                    return

                user_answer = question["options"][choice_index]
                is_correct = choice_index == question["correct_index"]

                self.quiz_manager.save_result(
                    user_id=user_id,
                    mode="quiz_review",
                    ru_word=question["ru_word"],
                    zh_word=question["zh_word"],
                    user_answer=user_answer,
                    correct_answer=question["correct_answer"],
                    is_correct=is_correct,
                )

                if is_correct:
                    result_text = "✅ Correct!" if lang == 'en' else "✅ 回答正确！"
                else:
                    if lang == 'en':
                        result_text = f"❌ Wrong.\nCorrect answer: {question['correct_answer']}"
                    else:
                        result_text = f"❌ 回答错误。\n正确答案：{question['correct_answer']}"

                if self.mistake_manager.has_mistakes(user_id):
                    markup = types.InlineKeyboardMarkup(row_width=2)
                    btn_next = "Next" if lang == 'en' else "下一题"
                    btn_menu = "Menu" if lang == 'en' else "返回菜单"
                    markup.add(
                        types.InlineKeyboardButton(btn_next, callback_data="review_mistakes"),
                        types.InlineKeyboardButton(btn_menu, callback_data="back_to_menu"),
                    )
                else:
                    markup = types.InlineKeyboardMarkup()
                    btn_done = "🎉 Menu" if lang == 'en' else "🎉 返回菜单"
                    markup.add(types.InlineKeyboardButton(btn_done, callback_data="back_to_menu"))
                    if lang == 'en':
                        result_text += "\n\n🎉 All mistakes cleared!"
                    else:
                        result_text += "\n\n🎉 错题已全部清完！"

                self.bot.edit_message_text(
                    f"{call.message.text}\n\n{result_text}",
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=markup,
                )

            elif call.data == "back_to_menu":
                self.bot.answer_callback_query(call.id)
                lang = self.user_lang.get(user_id, 'zh')

                if lang == 'en':
                    title = "--- 🤖 Bot Menu ---"
                    btn_lang = types.InlineKeyboardButton("🌐 Language", callback_data="set_lang")
                    btn_level = types.InlineKeyboardButton("📊 My Level", callback_data="show_level_menu")
                    btn_add = types.InlineKeyboardButton("➕ Vocabulary", callback_data="add_word_start")
                    btn_view = types.InlineKeyboardButton("📖 My Words", callback_data="view_words")
                    btn_help = types.InlineKeyboardButton("❓ HELP", callback_data="get_help")
                    btn_study = types.InlineKeyboardButton("📚 Word Study", callback_data="study_words")
                    btn_exercise = types.InlineKeyboardButton("✍️ Grammar Drill", callback_data="exercise_start")
                    btn_quiz = types.InlineKeyboardButton("🧠 Quiz", callback_data="quiz_start")
                else:
                    title = "--- 🤖 机器人功能菜单 ---"
                    btn_lang = types.InlineKeyboardButton("🌐 语言设置", callback_data="set_lang")
                    btn_level = types.InlineKeyboardButton("📊 我的水平", callback_data="show_level_menu")
                    btn_add = types.InlineKeyboardButton("➕ 生词本", callback_data="add_word_start")
                    btn_view = types.InlineKeyboardButton("📖 查看生词本", callback_data="view_words")
                    btn_help = types.InlineKeyboardButton("❓ HELP", callback_data="get_help")
                    btn_study = types.InlineKeyboardButton("📚 单词学习", callback_data="study_words")
                    btn_exercise = types.InlineKeyboardButton("✍️ 变格练习", callback_data="exercise_start")
                    btn_quiz = types.InlineKeyboardButton("🧠 随机测验", callback_data="quiz_start")

                markup = types.InlineKeyboardMarkup(row_width=2)
                markup.add(btn_lang, btn_level, btn_add, btn_view, btn_help, btn_study, btn_exercise, btn_quiz)

                try:
                    self.bot.edit_message_text(title, call.message.chat.id,
                                               call.message.message_id, reply_markup=markup)
                except:
                    self.bot.send_message(call.message.chat.id, title, reply_markup=markup)

        # --- [3] 普通文本处理器 ---

        @self.bot.message_handler(func=lambda message: True)
        def handle_text(message):
            user_id = message.from_user.id
            text = message.text
            lang = self.user_lang.get(user_id, 'zh')

            if self.user_states.get(user_id) == 'AWAITING_WORD':
                try:
                    parts = text.replace('，', ',').split(',')
                    if len(parts) == 2:
                        ru, zh = parts[0].strip(), parts[1].strip()
                        self.db.add_word(user_id, ru, zh)
                        self.user_states[user_id] = None
                        if lang == 'en':
                            self.bot.reply_to(message, f"✅ Added to vocabulary:\nRussian: {ru}\nChinese: {zh}")
                        else:
                            self.bot.reply_to(message, f"✅ 成功录入生词本：\n俄语：{ru}\n中文：{zh}")
                    else:
                        if lang == 'en':
                            self.bot.reply_to(message, "⚠️ Wrong format! Use: Russian,Chinese\nSend /cancel to exit.")
                        else:
                            self.bot.reply_to(message, "⚠️ 格式错误！请按「俄语,中文」发送。退出请发 /cancel")
                except Exception:
                    if lang == 'en':
                        self.bot.reply_to(message, "Save error. Check database.")
                    else:
                        self.bot.reply_to(message, "保存出错，请检查数据库配置。")
                return

            if text.startswith('/'):
                return

            has_english = any('a' <= c.lower() <= 'z' for c in text)
            if has_english:
                if lang == 'en':
                    self.bot.reply_to(message, text)
                else:
                    self.bot.reply_to(message, "暂不支持纯英语交流哦。")
            else:
                self.bot.reply_to(message, text)

    def start(self):
        print(">>> 俄语助手已启动，正在监听...")
        self.bot.infinity_polling()


if __name__ == "__main__":
    import time
    max_retries = 3
    for i in range(max_retries):
        try:
            my_bot = RusHelperBot()
            my_bot.bot.remove_webhook()
            my_bot.start()
        except Exception as e:
            print(f"连接失败 ({i+1}/{max_retries}): {e}")
            if i < max_retries - 1:
                print("5秒后重试...")
                time.sleep(5)