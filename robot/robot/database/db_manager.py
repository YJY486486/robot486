import sqlite3
import os
import json

class DatabaseManager:
    def __init__(self, db_path="data/bot_database.db"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        self.db_path = os.path.join(project_root, db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def get_user_words(self, user_id):
        """获取用户存储的所有单词"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT ru_word, zh_word FROM words WHERE user_id = ? ORDER BY word_id DESC",
                (user_id,)
            )
            return cursor.fetchall()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """初始化所有数据库表"""
        with self._get_connection() as conn:
            # 1. 创建用户表
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    level TEXT DEFAULT '未设置'
                )
            ''')

            # 2. 创建单词表
            conn.execute('''
                CREATE TABLE IF NOT EXISTS words (
                    word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    ru_word TEXT,
                    zh_word TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')

            # 3. 创建单词库表（带英文列）
            conn.execute('''
                CREATE TABLE IF NOT EXISTS word_bank (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    russian TEXT NOT NULL,
                    chinese TEXT NOT NULL,
                    english TEXT DEFAULT '',
                    level TEXT DEFAULT 'A0'
                )
            ''')
            conn.commit()

        # 初始化单词库数据
        self._load_word_bank_if_empty()

    def add_word(self, user_id, ru, zh):
        """保存新单词"""
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO words (user_id, ru_word, zh_word) VALUES (?, ?, ?)",
                (user_id, ru, zh)
            )
            conn.commit()

    def save_user(self, user_id, username, first_name):
        with self._get_connection() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
                (user_id, username, first_name)
            )
            conn.commit()

    def update_user_level(self, user_id, level):
        with self._get_connection() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
                (user_id,)
            )
            conn.execute(
                "UPDATE users SET level = ? WHERE user_id = ?",
                (level, user_id)
            )
            conn.commit()

    def get_user_level(self, user_id):
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT level FROM users WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            return result[0] if result else "未记录"

    def _load_word_bank_if_empty(self):
        """如果单词库为空，则加载数据"""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM word_bank")
            if cursor.fetchone()[0] == 0:
                self._load_words_from_json(conn)

    def _load_words_from_json(self, conn):
        """从 JSON 文件加载单词库"""
        project_root = os.path.dirname(os.path.dirname(self.db_path))
        json_path = os.path.join(project_root, 'word_bank.json')

        if not os.path.exists(json_path):
            print(f"⚠️ 未找到单词库文件: {json_path}")
            self._load_minimal_words(conn)
            return

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                words_data = json.load(f)

            count = 0
            for level, words in words_data.items():
                for word in words:
                    conn.execute('''
                        INSERT INTO word_bank (russian, chinese, english, level)
                        VALUES (?, ?, ?, ?)
                    ''', (word['ru'], word['zh'], word.get('en', ''), level))
                    count += 1

            conn.commit()
            print(f"✅ 从 word_bank.json 加载了 {count} 个单词")
        except Exception as e:
            print(f"❌ 加载 JSON 失败: {e}")
            self._load_minimal_words(conn)

    def _load_minimal_words(self, conn):
        """最小备用单词库"""
        minimal_words = [
            ("Привет", "你好", "Hello", "A0"),
            ("Спасибо", "谢谢", "Thank you", "A0"),
            ("Пока", "再见", "Bye", "A0"),
            ("Как дела?", "你好吗", "How are you?", "A1"),
            ("Любовь", "爱", "Love", "A2"),
        ]
        for ru, zh, en, lvl in minimal_words:
            conn.execute('''
                INSERT INTO word_bank (russian, chinese, english, level)
                VALUES (?, ?, ?, ?)
            ''', (ru, zh, en, lvl))
        conn.commit()
        print("✅ 加载了备用单词库")

    def get_random_words(self, count=50, level=None):
        """从单词库随机获取指定数量的单词（返回 russian, chinese, english）"""
        with self._get_connection() as conn:
            if level and level != '未设置':
                cursor = conn.execute('''
                    SELECT russian, chinese, english FROM word_bank 
                    WHERE level = ?
                    ORDER BY RANDOM() LIMIT ?
                ''', (level, count))
            else:
                cursor = conn.execute('''
                    SELECT russian, chinese, english FROM word_bank 
                    ORDER BY RANDOM() LIMIT ?
                ''', (count,))
            return cursor.fetchall()

    def get_word_count_by_level(self, level):
        """获取某个等级有多少单词"""
        if level == '未设置':
            return 0
        with self._get_connection() as conn:
            cursor = conn.execute('SELECT COUNT(*) FROM word_bank WHERE level = ?', (level,))
            return cursor.fetchone()[0]