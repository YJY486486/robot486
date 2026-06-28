class MistakeManager:
    def __init__(self, db):
        self.db = db
        self._create_table()        # 保证表存在

    def _create_table(self):
        with self.db._get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_mistake_stats (
                    user_id INTEGER,
                    ru_word TEXT,
                    zh_word TEXT,
                    total_wrong INTEGER DEFAULT 1,
                    consecutive_correct INTEGER DEFAULT 0,
                    PRIMARY KEY (user_id, ru_word, zh_word)
                )
            ''')
            conn.commit()

    def record(self, user_id, ru_word, zh_word, is_correct):
        """记录一次答题结果"""
        with self.db._get_connection() as conn:
            # 查找是否已有该用户的这个单词
            row = conn.execute(
                "SELECT total_wrong, consecutive_correct FROM user_mistake_stats "
                "WHERE user_id=? AND ru_word=? AND zh_word=?",
                (user_id, ru_word, zh_word)
            ).fetchone()

            if row is None:
                # 第一次遇到这个单词
                total_wrong = 1
                cc = 1 if is_correct else 0
                conn.execute(
                    "INSERT INTO user_mistake_stats VALUES (?, ?, ?, ?, ?)",
                    (user_id, ru_word, zh_word, total_wrong, cc)
                )
            else:
                total_wrong, cc = row
                if is_correct:
                    cc += 1
                    if cc >= 3:      # 连对3次，删除记录
                        conn.execute(
                            "DELETE FROM user_mistake_stats WHERE user_id=? AND ru_word=? AND zh_word=?",
                            (user_id, ru_word, zh_word)
                        )
                        conn.commit()
                        return
                    else:
                        conn.execute(
                            "UPDATE user_mistake_stats SET consecutive_correct=? WHERE user_id=? AND ru_word=? AND zh_word=?",
                            (cc, user_id, ru_word, zh_word)
                        )
                else:
                    # 答错：错误次数+1，连续正确归零
                    conn.execute(
                        "UPDATE user_mistake_stats SET total_wrong=?, consecutive_correct=0 WHERE user_id=? AND ru_word=? AND zh_word=?",
                        (total_wrong + 1, user_id, ru_word, zh_word)
                    )
            conn.commit()

    def get_mistake_words(self, user_id):
        """获取用户的所有错题，按错误次数从高到低排序"""
        with self.db._get_connection() as conn:
            rows = conn.execute(
                "SELECT ru_word, zh_word FROM user_mistake_stats "
                "WHERE user_id=? AND consecutive_correct < 3 "
                "ORDER BY total_wrong DESC",
                (user_id,)
            ).fetchall()
            return [{"ru_word": r[0], "zh_word": r[1]} for r in rows]

    def has_mistakes(self, user_id):
        return len(self.get_mistake_words(user_id)) > 0