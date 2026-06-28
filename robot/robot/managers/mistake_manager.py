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
        with self.db._get_connection() as conn:
            row = conn.execute(
                "SELECT total_wrong, consecutive_correct FROM user_mistake_stats "
                "WHERE user_id=? AND ru_word=? AND zh_word=?",
                (user_id, ru_word, zh_word)
            ).fetchone()

            print(f"DEBUG record: user={user_id}, word={ru_word}, correct={is_correct}, row={row}")

            if row is None:
                total_wrong = 0 if is_correct else 1
                cc = 1 if is_correct else 0
                print(f"DEBUG: 新记录, total_wrong={total_wrong}, cc={cc}")
                conn.execute(
                    "INSERT INTO user_mistake_stats VALUES (?, ?, ?, ?, ?)",
                    (user_id, ru_word, zh_word, total_wrong, cc)
                )
            else:
                total_wrong, cc = row
                if is_correct:
                    cc += 1
                    print(f"DEBUG: 答对, cc={cc}")
                    if cc >= 3:
                        print(f"DEBUG: 连对3次，删除")
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
                    print(f"DEBUG: 答错, total_wrong={total_wrong + 1}")
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