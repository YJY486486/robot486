import random
import re


class QuizManager:
    PRESET_EXERCISES = [
        # ===== 名词所有格单数 =====
        {"ru_word": "Мама", "zh_word": "妈妈", "level": "A0",
         "prompt": "请写出 \"Мама\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Мама\".",
         "answers": ["мамы"], "display_answer": "мамы",
         "explanation": "规则：-а 结尾的阴性名词，所有格单数变为 -ы。",
         "explanation_en": "Rule: Feminine nouns ending in -а change to -ы in genitive singular."},
        {"ru_word": "Папа", "zh_word": "爸爸", "level": "A0",
         "prompt": "请写出 \"Папа\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Папа\".",
         "answers": ["папы"], "display_answer": "папы",
         "explanation": "规则：-а 结尾名词，所有格单数变为 -ы。",
         "explanation_en": "Rule: Nouns ending in -а change to -ы in genitive singular."},
        {"ru_word": "Книга", "zh_word": "书", "level": "A1",
         "prompt": "请写出 \"Книга\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Книга\".",
         "answers": ["книги"], "display_answer": "книги",
         "explanation": "规则：г 后不用 ы，所有格单数写作 -и。",
         "explanation_en": "Rule: After г use -и instead of -ы."},
        {"ru_word": "Школа", "zh_word": "学校", "level": "A1",
         "prompt": "请写出 \"Школа\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Школа\".",
         "answers": ["школы"], "display_answer": "школы",
         "explanation": "规则：-а 结尾的阴性名词，所有格单数变为 -ы。",
         "explanation_en": "Rule: Feminine nouns ending in -а change to -ы in genitive singular."},
        {"ru_word": "Дом", "zh_word": "家/房子", "level": "A1",
         "prompt": "请写出 \"Дом\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Дом\".",
         "answers": ["дома"], "display_answer": "дома",
         "explanation": "规则：多数阳性硬辅音结尾名词，所有格单数加 -а。",
         "explanation_en": "Rule: Most masculine nouns ending in a hard consonant add -а."},
        {"ru_word": "Город", "zh_word": "城市", "level": "A2",
         "prompt": "请写出 \"Город\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Город\".",
         "answers": ["города"], "display_answer": "города",
         "explanation": "规则：多数阳性硬辅音结尾名词，所有格单数加 -а。",
         "explanation_en": "Rule: Most masculine nouns ending in a hard consonant add -а."},
        {"ru_word": "Стол", "zh_word": "桌子", "level": "A0",
         "prompt": "请写出 \"Стол\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Стол\".",
         "answers": ["стола"], "display_answer": "стола",
         "explanation": "规则：阳性硬辅音结尾名词，所有格单数加 -а。",
         "explanation_en": "Rule: Masculine nouns ending in a hard consonant add -а."},
        {"ru_word": "Брат", "zh_word": "兄弟", "level": "A0",
         "prompt": "请写出 \"Брат\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Брат\".",
         "answers": ["брата"], "display_answer": "брата",
         "explanation": "规则：阳性硬辅音结尾名词，所有格单数加 -а。",
         "explanation_en": "Rule: Masculine nouns ending in a hard consonant add -а."},
        {"ru_word": "Студент", "zh_word": "大学生", "level": "A1",
         "prompt": "请写出 \"Студент\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Студент\".",
         "answers": ["студента"], "display_answer": "студента",
         "explanation": "规则：阳性硬辅音结尾名词，所有格单数加 -а。",
         "explanation_en": "Rule: Masculine nouns ending in a hard consonant add -а."},
        {"ru_word": "Учитель", "zh_word": "老师", "level": "A0",
         "prompt": "请写出 \"Учитель\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Учитель\".",
         "answers": ["учителя"], "display_answer": "учителя",
         "explanation": "规则：-ь 结尾的阳性名词，所有格单数变为 -я。",
         "explanation_en": "Rule: Masculine nouns ending in -ь change to -я in genitive singular."},
        {"ru_word": "Словарь", "zh_word": "词典", "level": "A2",
         "prompt": "请写出 \"Словарь\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Словарь\".",
         "answers": ["словаря"], "display_answer": "словаря",
         "explanation": "规则：-ь 结尾的阳性名词，所有格单数变为 -я。",
         "explanation_en": "Rule: Masculine nouns ending in -ь change to -я in genitive singular."},
        {"ru_word": "Дверь", "zh_word": "门", "level": "A0",
         "prompt": "请写出 \"Дверь\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Дверь\".",
         "answers": ["двери"], "display_answer": "двери",
         "explanation": "规则：-ь 结尾的阴性名词，所有格单数变为 -и。",
         "explanation_en": "Rule: Feminine nouns ending in -ь change to -и in genitive singular."},
        {"ru_word": "Ночь", "zh_word": "夜晚", "level": "A0",
         "prompt": "请写出 \"Ночь\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Ночь\".",
         "answers": ["ночи"], "display_answer": "ночи",
         "explanation": "规则：-ь 结尾的阴性名词，所有格单数变为 -и。",
         "explanation_en": "Rule: Feminine nouns ending in -ь change to -и in genitive singular."},
        {"ru_word": "Окно", "zh_word": "窗户", "level": "A0",
         "prompt": "请写出 \"Окно\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Окно\".",
         "answers": ["окна"], "display_answer": "окна",
         "explanation": "规则：-о 结尾的中性名词，所有格单数变为 -а。",
         "explanation_en": "Rule: Neuter nouns ending in -о change to -а in genitive singular."},
        {"ru_word": "Море", "zh_word": "海", "level": "A1",
         "prompt": "请写出 \"Море\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Море\".",
         "answers": ["моря"], "display_answer": "моря",
         "explanation": "规则：-е 结尾的中性名词，所有格单数变为 -я。",
         "explanation_en": "Rule: Neuter nouns ending in -е change to -я in genitive singular."},
        {"ru_word": "Имя", "zh_word": "名字", "level": "A2",
         "prompt": "请写出 \"Имя\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Имя\".",
         "answers": ["имени"], "display_answer": "имени",
         "explanation": "规则：-мя 结尾的中性名词，所有格单数加 -ени。",
         "explanation_en": "Rule: Neuter nouns ending in -мя add -ени in genitive singular."},
        {"ru_word": "Время", "zh_word": "时间", "level": "A2",
         "prompt": "请写出 \"Время\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Время\".",
         "answers": ["времени"], "display_answer": "времени",
         "explanation": "规则：-мя 结尾的中性名词，所有格单数加 -ени。",
         "explanation_en": "Rule: Neuter nouns ending in -мя add -ени in genitive singular."},
        {"ru_word": "Сестра", "zh_word": "姐妹", "level": "A0",
         "prompt": "请写出 \"Сестра\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Сестра\".",
         "answers": ["сестры"], "display_answer": "сестры",
         "explanation": "规则：-а 结尾的阴性名词，所有格单数变为 -ы。",
         "explanation_en": "Rule: Feminine nouns ending in -а change to -ы in genitive singular."},
        {"ru_word": "Вода", "zh_word": "水", "level": "A0",
         "prompt": "请写出 \"Вода\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Вода\".",
         "answers": ["воды"], "display_answer": "воды",
         "explanation": "规则：-а 结尾的阴性名词，所有格单数变为 -ы。",
         "explanation_en": "Rule: Feminine nouns ending in -а change to -ы in genitive singular."},
        {"ru_word": "Земля", "zh_word": "土地", "level": "A1",
         "prompt": "请写出 \"Земля\" 的所有格单数形式。",
         "prompt_en": "Write the genitive singular form of \"Земля\".",
         "answers": ["земли"], "display_answer": "земли",
         "explanation": "规则：-я 结尾的阴性名词，所有格单数变为 -и。",
         "explanation_en": "Rule: Feminine nouns ending in -я change to -и in genitive singular."},

        # ===== 名词复数所有格 =====
        {"ru_word": "Мама", "zh_word": "妈妈", "level": "A1",
         "prompt": "请写出 \"Мама\" 的复数所有格形式。",
         "prompt_en": "Write the genitive plural form of \"Мама\".",
         "answers": ["мам"], "display_answer": "мам",
         "explanation": "规则：-а 结尾阴性名词，复数所有格去掉 -а。",
         "explanation_en": "Rule: Feminine nouns ending in -а drop the ending in genitive plural."},
        {"ru_word": "Школа", "zh_word": "学校", "level": "A1",
         "prompt": "请写出 \"Школа\" 的复数所有格形式。",
         "prompt_en": "Write the genitive plural form of \"Школа\".",
         "answers": ["школ"], "display_answer": "школ",
         "explanation": "规则：-а 结尾阴性名词，复数所有格去掉 -а。",
         "explanation_en": "Rule: Feminine nouns ending in -а drop the ending in genitive plural."},
        {"ru_word": "Стол", "zh_word": "桌子", "level": "A1",
         "prompt": "请写出 \"Стол\" 的复数所有格形式。",
         "prompt_en": "Write the genitive plural form of \"Стол\".",
         "answers": ["столов"], "display_answer": "столов",
         "explanation": "规则：阳性硬辅音结尾名词，复数所有格加 -ов。",
         "explanation_en": "Rule: Masculine hard-stem nouns add -ов in genitive plural."},
        {"ru_word": "Город", "zh_word": "城市", "level": "A2",
         "prompt": "请写出 \"Город\" 的复数所有格形式。",
         "prompt_en": "Write the genitive plural form of \"Город\".",
         "answers": ["городов"], "display_answer": "городов",
         "explanation": "规则：阳性硬辅音结尾名词，复数所有格加 -ов。",
         "explanation_en": "Rule: Masculine hard-stem nouns add -ов in genitive plural."},
        {"ru_word": "Дом", "zh_word": "房子", "level": "A2",
         "prompt": "请写出 \"Дом\" 的复数所有格形式。",
         "prompt_en": "Write the genitive plural form of \"Дом\".",
         "answers": ["домов"], "display_answer": "домов",
         "explanation": "规则：阳性硬辅音结尾名词，复数所有格加 -ов。",
         "explanation_en": "Rule: Masculine hard-stem nouns add -ов in genitive plural."},
        {"ru_word": "Студент", "zh_word": "大学生", "level": "A2",
         "prompt": "请写出 \"Студент\" 的复数所有格形式。",
         "prompt_en": "Write the genitive plural form of \"Студент\".",
         "answers": ["студентов"], "display_answer": "студентов",
         "explanation": "规则：阳性硬辅音结尾名词，复数所有格加 -ов。",
         "explanation_en": "Rule: Masculine hard-stem nouns add -ов in genitive plural."},
        {"ru_word": "Учитель", "zh_word": "老师", "level": "A1",
         "prompt": "请写出 \"Учитель\" 的复数所有格形式。",
         "prompt_en": "Write the genitive plural form of \"Учитель\".",
         "answers": ["учителей"], "display_answer": "учителей",
         "explanation": "规则：-ь 结尾阳性名词，复数所有格变为 -ей。",
         "explanation_en": "Rule: Masculine nouns ending in -ь change to -ей in genitive plural."},
        {"ru_word": "Словарь", "zh_word": "词典", "level": "A2",
         "prompt": "请写出 \"Словарь\" 的复数所有格形式。",
         "prompt_en": "Write the genitive plural form of \"Словарь\".",
         "answers": ["словарей"], "display_answer": "словарей",
         "explanation": "规则：-ь 结尾阳性名词，复数所有格变为 -ей。",
         "explanation_en": "Rule: Masculine nouns ending in -ь change to -ей in genitive plural."},
        {"ru_word": "Дверь", "zh_word": "门", "level": "A1",
         "prompt": "请写出 \"Дверь\" 的复数所有格形式。",
         "prompt_en": "Write the genitive plural form of \"Дверь\".",
         "answers": ["дверей"], "display_answer": "дверей",
         "explanation": "规则：-ь 结尾阴性名词，复数所有格变为 -ей。",
         "explanation_en": "Rule: Feminine nouns ending in -ь change to -ей in genitive plural."},
        {"ru_word": "Ночь", "zh_word": "夜晚", "level": "A1",
         "prompt": "请写出 \"Ночь\" 的复数所有格形式。",
         "prompt_en": "Write the genitive plural form of \"Ночь\".",
         "answers": ["ночей"], "display_answer": "ночей",
         "explanation": "规则：-ь 结尾阴性名词，复数所有格变为 -ей。",
         "explanation_en": "Rule: Feminine nouns ending in -ь change to -ей in genitive plural."},
        {"ru_word": "Окно", "zh_word": "窗户", "level": "A1",
         "prompt": "请写出 \"Окно\" 的复数所有格形式。",
         "prompt_en": "Write the genitive plural form of \"Окно\".",
         "answers": ["окон"], "display_answer": "окон",
         "explanation": "规则：-о 结尾中性名词，复数所有格去掉 -о，加插入元音 о。",
         "explanation_en": "Rule: Neuter nouns ending in -о drop -о and add a fill vowel in genitive plural."},
        {"ru_word": "Море", "zh_word": "海", "level": "A2",
         "prompt": "请写出 \"Море\" 的复数所有格形式。",
         "prompt_en": "Write the genitive plural form of \"Море\".",
         "answers": ["морей"], "display_answer": "морей",
         "explanation": "规则：-е 结尾中性名词，复数所有格变为 -ей。",
         "explanation_en": "Rule: Neuter nouns ending in -е change to -ей in genitive plural."},
        {"ru_word": "Место", "zh_word": "地方", "level": "A2",
         "prompt": "请写出 \"Место\" 的复数所有格形式。",
         "prompt_en": "Write the genitive plural form of \"Место\".",
         "answers": ["мест"], "display_answer": "мест",
         "explanation": "规则：-о 结尾中性名词，复数所有格去掉 -о。",
         "explanation_en": "Rule: Neuter nouns ending in -о drop the ending in genitive plural."},
        {"ru_word": "Друг", "zh_word": "朋友", "level": "A1",
         "prompt": "请写出 \"Друг\" 的复数所有格形式。",
         "prompt_en": "Write the genitive plural form of \"Друг\".",
         "answers": ["друзей"], "display_answer": "друзей",
         "explanation": "规则：阳性名词，复数所有格加 -ей，г→з 音变。",
         "explanation_en": "Rule: Masculine nouns, add -ей with г→з mutation in genitive plural."},

        # ===== 名词与格单数 =====
        {"ru_word": "Мама", "zh_word": "妈妈", "level": "A1",
         "prompt": "请写出 \"Мама\" 的与格单数形式。",
         "prompt_en": "Write the dative singular form of \"Мама\".",
         "answers": ["маме"], "display_answer": "маме",
         "explanation": "规则：-а 结尾的阴性名词，与格单数变为 -е。",
         "explanation_en": "Rule: Feminine nouns ending in -а change to -е in dative singular."},
        {"ru_word": "Папа", "zh_word": "爸爸", "level": "A1",
         "prompt": "请写出 \"Папа\" 的与格单数形式。",
         "prompt_en": "Write the dative singular form of \"Папа\".",
         "answers": ["папе"], "display_answer": "папе",
         "explanation": "规则：-а 结尾名词，与格单数变为 -е。",
         "explanation_en": "Rule: Nouns ending in -а change to -е in dative singular."},
        {"ru_word": "Книга", "zh_word": "书", "level": "A1",
         "prompt": "请写出 \"Книга\" 的与格单数形式。",
         "prompt_en": "Write the dative singular form of \"Книга\".",
         "answers": ["книге"], "display_answer": "книге",
         "explanation": "规则：г 后写作 -е。",
         "explanation_en": "Rule: After г, write -е in dative singular."},
        {"ru_word": "Брат", "zh_word": "兄弟", "level": "A1",
         "prompt": "请写出 \"Брат\" 的与格单数形式。",
         "prompt_en": "Write the dative singular form of \"Брат\".",
         "answers": ["брату"], "display_answer": "брату",
         "explanation": "规则：阳性硬辅音结尾名词，与格单数加 -у。",
         "explanation_en": "Rule: Masculine hard-stem nouns add -у in dative singular."},
        {"ru_word": "Стол", "zh_word": "桌子", "level": "A1",
         "prompt": "请写出 \"Стол\" 的与格单数形式。",
         "prompt_en": "Write the dative singular form of \"Стол\".",
         "answers": ["столу"], "display_answer": "столу",
         "explanation": "规则：阳性硬辅音结尾名词，与格单数加 -у。",
         "explanation_en": "Rule: Masculine hard-stem nouns add -у in dative singular."},
        {"ru_word": "Учитель", "zh_word": "老师", "level": "A2",
         "prompt": "请写出 \"Учитель\" 的与格单数形式。",
         "prompt_en": "Write the dative singular form of \"Учитель\".",
         "answers": ["учителю"], "display_answer": "учителю",
         "explanation": "规则：-ь 结尾阳性名词，与格单数变为 -ю。",
         "explanation_en": "Rule: Masculine nouns ending in -ь change to -ю in dative singular."},
        {"ru_word": "Сестра", "zh_word": "姐妹", "level": "A1",
         "prompt": "请写出 \"Сестра\" 的与格单数形式。",
         "prompt_en": "Write the dative singular form of \"Сестра\".",
         "answers": ["сестре"], "display_answer": "сестре",
         "explanation": "规则：-а 结尾阴性名词，与格单数变为 -е。",
         "explanation_en": "Rule: Feminine nouns ending in -а change to -е in dative singular."},
        # ===== 名词工具格单数 =====
         {"ru_word": "Брат", "zh_word": "兄弟", "level": "A2",
         "prompt": "请写出 \"Брат\" 的工具格单数形式。",
         "prompt_en": "Write the instrumental singular form of \"Брат\".",
         "answers": ["братом"], "display_answer": "братом",
         "explanation": "规则：阳性硬辅音结尾名词，工具格单数加 -ом。",
         "explanation_en": "Rule: Masculine hard-stem nouns add -ом in instrumental singular."},
        {"ru_word": "Стол", "zh_word": "桌子", "level": "A2",
         "prompt": "请写出 \"Стол\" 的工具格单数形式。",
         "prompt_en": "Write the instrumental singular form of \"Стол\".",
         "answers": ["столом"], "display_answer": "столом",
         "explanation": "规则：阳性硬辅音结尾名词，工具格单数加 -ом。",
         "explanation_en": "Rule: Masculine hard-stem nouns add -ом in instrumental singular."},
        {"ru_word": "Учитель", "zh_word": "老师", "level": "A2",
         "prompt": "请写出 \"Учитель\" 的工具格单数形式。",
         "prompt_en": "Write the instrumental singular form of \"Учитель\".",
         "answers": ["учителем"], "display_answer": "учителем",
         "explanation": "规则：-ь 结尾阳性名词，工具格单数变为 -ем。",
         "explanation_en": "Rule: Masculine nouns ending in -ь change to -ем in instrumental singular."},
        {"ru_word": "Мама", "zh_word": "妈妈", "level": "A2",
         "prompt": "请写出 \"Мама\" 的工具格单数形式。",
         "prompt_en": "Write the instrumental singular form of \"Мама\".",
         "answers": ["мамой"], "display_answer": "мамой",
         "explanation": "规则：-а 结尾阴性名词，工具格单数变为 -ой。",
         "explanation_en": "Rule: Feminine nouns ending in -а change to -ой in instrumental singular."},
        {"ru_word": "Школа", "zh_word": "学校", "level": "A2",
         "prompt": "请写出 \"Школа\" 的工具格单数形式。",
         "prompt_en": "Write the instrumental singular form of \"Школа\".",
         "answers": ["школой"], "display_answer": "школой",
         "explanation": "规则：-а 结尾阴性名词，工具格单数变为 -ой。",
         "explanation_en": "Rule: Feminine nouns ending in -а change to -ой in instrumental singular."},
        {"ru_word": "Дверь", "zh_word": "门", "level": "A2",
         "prompt": "请写出 \"Дверь\" 的工具格单数形式。",
         "prompt_en": "Write the instrumental singular form of \"Дверь\".",
         "answers": ["дверью"], "display_answer": "дверью",
         "explanation": "规则：-ь 结尾阴性名词，工具格单数变为 -ью。",
         "explanation_en": "Rule: Feminine nouns ending in -ь change to -ью in instrumental singular."},

        # ===== 名词前置格单数 =====
        {"ru_word": "Стол", "zh_word": "桌子", "level": "A1",
         "prompt": "请写出 \"Стол\" 的前置格单数形式。",
         "prompt_en": "Write the prepositional singular form of \"Стол\".",
         "answers": ["столе"], "display_answer": "столе",
         "explanation": "规则：阳性硬辅音结尾名词，前置格单数加 -е。",
         "explanation_en": "Rule: Masculine hard-stem nouns add -е in prepositional singular."},
        {"ru_word": "Город", "zh_word": "城市", "level": "A1",
         "prompt": "请写出 \"Город\" 的前置格单数形式。",
         "prompt_en": "Write the prepositional singular form of \"Город\".",
         "answers": ["городе"], "display_answer": "городе",
         "explanation": "规则：阳性硬辅音结尾名词，前置格单数加 -е。",
         "explanation_en": "Rule: Masculine hard-stem nouns add -е in prepositional singular."},
        {"ru_word": "Школа", "zh_word": "学校", "level": "A1",
         "prompt": "请写出 \"Школа\" 的前置格单数形式。",
         "prompt_en": "Write the prepositional singular form of \"Школа\".",
         "answers": ["школе"], "display_answer": "школе",
         "explanation": "规则：-а 结尾阴性名词，前置格单数变为 -е。",
         "explanation_en": "Rule: Feminine nouns ending in -а change to -е in prepositional singular."},
        {"ru_word": "Окно", "zh_word": "窗户", "level": "A1",
         "prompt": "请写出 \"Окно\" 的前置格单数形式。",
         "prompt_en": "Write the prepositional singular form of \"Окно\".",
         "answers": ["окне"], "display_answer": "окне",
         "explanation": "规则：-о 结尾中性名词，前置格单数变为 -е。",
         "explanation_en": "Rule: Neuter nouns ending in -о change to -е in prepositional singular."},
        {"ru_word": "Море", "zh_word": "海", "level": "A2",
         "prompt": "请写出 \"Море\" 的前置格单数形式。",
         "prompt_en": "Write the prepositional singular form of \"Море\".",
         "answers": ["море"], "display_answer": "море",
         "explanation": "规则：-е 结尾中性名词，前置格单数不变。",
         "explanation_en": "Rule: Neuter nouns ending in -е remain unchanged in prepositional singular."},

        # ===== 动词现在时第一人称单数 =====
        {"ru_word": "Читать", "zh_word": "阅读", "level": "A1",
         "prompt": "请写出 \"Читать\" 的第一人称单数现在时（я）。",
         "prompt_en": "Write the 1st person singular present tense of \"Читать\" (я).",
         "answers": ["читаю"], "display_answer": "читаю",
         "explanation": "规则：-ать 结尾动词，я 形式为 -аю。",
         "explanation_en": "Rule: Verbs ending in -ать take -аю in the я form."},
        {"ru_word": "Писать", "zh_word": "写", "level": "A1",
         "prompt": "请写出 \"Писать\" 的第一人称单数现在时（я）。",
         "prompt_en": "Write the 1st person singular present tense of \"Писать\" (я).",
         "answers": ["пишу"], "display_answer": "пишу",
         "explanation": "规则：писать 的 я 形式是 пишу（с→ш 音变）。",
         "explanation_en": "Rule: писать becomes пишу (с→ш mutation)."},
        {"ru_word": "Говорить", "zh_word": "说", "level": "A1",
         "prompt": "请写出 \"Говорить\" 的第一人称单数现在时（я）。",
         "prompt_en": "Write the 1st person singular present tense of \"Говорить\" (я).",
         "answers": ["говорю"], "display_answer": "говорю",
         "explanation": "规则：-ить 结尾动词，я 形式为 -ю。",
         "explanation_en": "Rule: Verbs ending in -ить take -ю in the я form."},
        {"ru_word": "Идти", "zh_word": "走", "level": "A1",
         "prompt": "请写出 \"Идти\" 的第一人称单数现在时（я）。",
         "prompt_en": "Write the 1st person singular present tense of \"Идти\" (я).",
         "answers": ["иду"], "display_answer": "иду",
         "explanation": "规则：идти 的 я 形式是 иду。",
         "explanation_en": "Rule: идти becomes иду in the я form."},
        {"ru_word": "Жить", "zh_word": "生活/住", "level": "A1",
         "prompt": "请写出 \"Жить\" 的第一人称单数现在时（я）。",
         "prompt_en": "Write the 1st person singular present tense of \"Жить\" (я).",
         "answers": ["живу"], "display_answer": "живу",
         "explanation": "规则：жить 的 я 形式是 живу。",
         "explanation_en": "Rule: жить becomes живу in the я form."},
        {"ru_word": "Любить", "zh_word": "爱", "level": "A1",
         "prompt": "请写出 \"Любить\" 的第一人称单数现在时（я）。",
         "prompt_en": "Write the 1st person singular present tense of \"Любить\" (я).",
         "answers": ["люблю"], "display_answer": "люблю",
         "explanation": "规则：-ить 结尾，я 形式为 -лю（б→бл 音变）。",
         "explanation_en": "Rule: любить becomes люблю (б→бл mutation)."},
        {"ru_word": "Смотреть", "zh_word": "看", "level": "A1",
         "prompt": "请写出 \"Смотреть\" 的第一人称单数现在时（я）。",
         "prompt_en": "Write the 1st person singular present tense of \"Смотреть\" (я).",
         "answers": ["смотрю"], "display_answer": "смотрю",
         "explanation": "规则：-еть 结尾动词，я 形式为 -ю。",
         "explanation_en": "Rule: Verbs ending in -еть take -ю in the я form."},
        {"ru_word": "Слышать", "zh_word": "听见", "level": "A2",
         "prompt": "请写出 \"Слышать\" 的第一人称单数现在时（я）。",
         "prompt_en": "Write the 1st person singular present tense of \"Слышать\" (я).",
         "answers": ["слышу"], "display_answer": "слышу",
         "explanation": "规则：-ать 结尾但属第二变位法，я 形式为 -у。",
         "explanation_en": "Rule: Second conjugation verb ending in -ать, takes -у in the я form."},
        {"ru_word": "Ехать", "zh_word": "乘车去", "level": "A2",
         "prompt": "请写出 \"Ехать\" 的第一人称单数现在时（я）。",
         "prompt_en": "Write the 1st person singular present tense of \"Ехать\" (я).",
         "answers": ["еду"], "display_answer": "еду",
         "explanation": "规则：ехать 的 я 形式是 еду（х→д 音变）。",
         "explanation_en": "Rule: ехать becomes еду (х→д mutation)."},
        {"ru_word": "Искать", "zh_word": "寻找", "level": "A2",
         "prompt": "请写出 \"Искать\" 的第一人称单数现在时（я）。",
         "prompt_en": "Write the 1st person singular present tense of \"Искать\" (я).",
         "answers": ["ищу"], "display_answer": "ищу",
         "explanation": "规则：искать 的 я 形式是 ищу（ск→щ 音变）。",
         "explanation_en": "Rule: искать becomes ищу (ск→щ mutation)."},

        # ===== 动词现在时第二人称单数 =====
        {"ru_word": "Читать", "zh_word": "阅读", "level": "A1",
         "prompt": "请写出 \"Читать\" 的第二人称单数现在时（ты）。",
         "prompt_en": "Write the 2nd person singular present tense of \"Читать\" (ты).",
         "answers": ["читаешь"], "display_answer": "читаешь",
         "explanation": "规则：-ать 结尾动词，ты 形式为 -аешь。",
         "explanation_en": "Rule: Verbs ending in -ать take -аешь in the ты form."},
        {"ru_word": "Говорить", "zh_word": "说", "level": "A1",
         "prompt": "请写出 \"Говорить\" 的第二人称单数现在时（ты）。",
         "prompt_en": "Write the 2nd person singular present tense of \"Говорить\" (ты).",
         "answers": ["говоришь"], "display_answer": "говоришь",
         "explanation": "规则：-ить 结尾动词，ты 形式为 -ишь。",
         "explanation_en": "Rule: Verbs ending in -ить take -ишь in the ты form."},
        {"ru_word": "Жить", "zh_word": "生活/住", "level": "A1",
         "prompt": "请写出 \"Жить\" 的第二人称单数现在时（ты）。",
         "prompt_en": "Write the 2nd person singular present tense of \"Жить\" (ты).",
         "answers": ["живёшь"], "display_answer": "живёшь",
         "explanation": "规则：жить 的 ты 形式是 живёшь。",
         "explanation_en": "Rule: жить becomes живёшь in the ты form."},
        {"ru_word": "Идти", "zh_word": "走", "level": "A1",
         "prompt": "请写出 \"Идти\" 的第二人称单数现在时（ты）。",
         "prompt_en": "Write the 2nd person singular present tense of \"Идти\" (ты).",
         "answers": ["идёшь"], "display_answer": "идёшь",
         "explanation": "规则：идти 的 ты 形式是 идёшь。",
         "explanation_en": "Rule: идти becomes идёшь in the ты form."},
        {"ru_word": "Любить", "zh_word": "爱", "level": "A2",
         "prompt": "请写出 \"Любить\" 的第二人称单数现在时（ты）。",
         "prompt_en": "Write the 2nd person singular present tense of \"Любить\" (ты).",
         "answers": ["любишь"], "display_answer": "любишь",
         "explanation": "规则：-ить 结尾，ты 形式为 -ишь。",
         "explanation_en": "Rule: Verbs ending in -ить take -ишь in the ты form."},

        # ===== 动词现在时第三人称单数 =====
        {"ru_word": "Читать", "zh_word": "阅读", "level": "A1",
         "prompt": "请写出 \"Читать\" 的第三人称单数现在时（он/она）。",
         "prompt_en": "Write the 3rd person singular present tense of \"Читать\" (он/она).",
         "answers": ["читает"], "display_answer": "читает",
         "explanation": "规则：-ать 结尾动词，он/она 形式为 -ает。",
         "explanation_en": "Rule: Verbs ending in -ать take -ает in the он/она form."},
        {"ru_word": "Говорить", "zh_word": "说", "level": "A1",
         "prompt": "请写出 \"Говорить\" 的第三人称单数现在时（он/она）。",
         "prompt_en": "Write the 3rd person singular present tense of \"Говорить\" (он/она).",
         "answers": ["говорит"], "display_answer": "говорит",
         "explanation": "规则：-ить 结尾动词，он/она 形式为 -ит。",
         "explanation_en": "Rule: Verbs ending in -ить take -ит in the он/она form."},
        {"ru_word": "Жить", "zh_word": "生活/住", "level": "A1",
         "prompt": "请写出 \"Жить\" 的第三人称单数现在时（он/она）。",
         "prompt_en": "Write the 3rd person singular present tense of \"Жить\" (он/она).",
         "answers": ["живёт"], "display_answer": "живёт",
         "explanation": "规则：жить 的 он/она 形式是 живёт。",
         "explanation_en": "Rule: жить becomes живёт in the он/она form."},
        {"ru_word": "Идти", "zh_word": "走", "level": "A2",
         "prompt": "请写出 \"Идти\" 的第三人称单数现在时（он/она）。",
         "prompt_en": "Write the 3rd person singular present tense of \"Идти\" (он/она).",
         "answers": ["идёт"], "display_answer": "идёт",
         "explanation": "规则：идти 的 он/она 形式是 идёт。",
         "explanation_en": "Rule: идти becomes идёт in the он/она form."},
        {"ru_word": "Писать", "zh_word": "写", "level": "A2",
         "prompt": "请写出 \"Писать\" 的第三人称单数现在时（он/она）。",
         "prompt_en": "Write the 3rd person singular present tense of \"Писать\" (он/она).",
         "answers": ["пишет"], "display_answer": "пишет",
         "explanation": "规则：писать 的 он/она 形式是 пишет（с→ш 音变）。",
         "explanation_en": "Rule: писать becomes пишет (с→ш mutation)."},
        # ===== 动词现在时复数 =====
        {"ru_word": "Читать", "zh_word": "阅读", "level": "A1",
         "prompt": "请写出 \"Читать\" 的第一人称复数现在时（мы）。",
         "prompt_en": "Write the 1st person plural present tense of \"Читать\" (мы).",
         "answers": ["читаем"], "display_answer": "читаем",
         "explanation": "规则：-ать 结尾动词，мы 形式为 -аем。",
         "explanation_en": "Rule: Verbs ending in -ать take -аем in the мы form."},
        {"ru_word": "Говорить", "zh_word": "说", "level": "A1",
         "prompt": "请写出 \"Говорить\" 的第一人称复数现在时（мы）。",
         "prompt_en": "Write the 1st person plural present tense of \"Говорить\" (мы).",
         "answers": ["говорим"], "display_answer": "говорим",
         "explanation": "规则：-ить 结尾动词，мы 形式为 -им。",
         "explanation_en": "Rule: Verbs ending in -ить take -им in the мы form."},
        {"ru_word": "Жить", "zh_word": "生活/住", "level": "A2",
         "prompt": "请写出 \"Жить\" 的第一人称复数现在时（мы）。",
         "prompt_en": "Write the 1st person plural present tense of \"Жить\" (мы).",
         "answers": ["живём"], "display_answer": "живём",
         "explanation": "规则：жить 的 мы 形式是 живём。",
         "explanation_en": "Rule: жить becomes живём in the мы form."},
        {"ru_word": "Читать", "zh_word": "阅读", "level": "A1",
         "prompt": "请写出 \"Читать\" 的第三人称复数现在时（они）。",
         "prompt_en": "Write the 3rd person plural present tense of \"Читать\" (они).",
         "answers": ["читают"], "display_answer": "читают",
         "explanation": "规则：-ать 结尾动词，они 形式为 -ают。",
         "explanation_en": "Rule: Verbs ending in -ать take -ают in the они form."},
        {"ru_word": "Говорить", "zh_word": "说", "level": "A1",
         "prompt": "请写出 \"Говорить\" 的第三人称复数现在时（они）。",
         "prompt_en": "Write the 3rd person plural present tense of \"Говорить\" (они).",
         "answers": ["говорят"], "display_answer": "говорят",
         "explanation": "规则：-ить 结尾动词，они 形式为 -ят。",
         "explanation_en": "Rule: Verbs ending in -ить take -ят in the они form."},
        {"ru_word": "Любить", "zh_word": "爱", "level": "A2",
         "prompt": "请写出 \"Любить\" 的第三人称复数现在时（они）。",
         "prompt_en": "Write the 3rd person plural present tense of \"Любить\" (они).",
         "answers": ["любят"], "display_answer": "любят",
         "explanation": "规则：-ить 结尾，они 形式为 -ят。",
         "explanation_en": "Rule: Verbs ending in -ить take -ят in the они form."},

        # ===== 动词过去时 =====
        {"ru_word": "Читать", "zh_word": "阅读", "level": "A1",
         "prompt": "请写出 \"Читать\" 的过去时阳性形式（он）。",
         "prompt_en": "Write the past tense masculine form of \"Читать\" (он).",
         "answers": ["читал"], "display_answer": "читал",
         "explanation": "规则：-ть 去掉加 -л。",
         "explanation_en": "Rule: Remove -ть and add -л."},
        {"ru_word": "Читать", "zh_word": "阅读", "level": "A1",
         "prompt": "请写出 \"Читать\" 的过去时阴性形式（она）。",
         "prompt_en": "Write the past tense feminine form of \"Читать\" (она).",
         "answers": ["читала"], "display_answer": "читала",
         "explanation": "规则：-ть 去掉加 -ла。",
         "explanation_en": "Rule: Remove -ть and add -ла."},
        {"ru_word": "Читать", "zh_word": "阅读", "level": "A1",
         "prompt": "请写出 \"Читать\" 的过去时中性形式（оно）。",
         "prompt_en": "Write the past tense neuter form of \"Читать\" (оно).",
         "answers": ["читало"], "display_answer": "читало",
         "explanation": "规则：-ть 去掉加 -ло。",
         "explanation_en": "Rule: Remove -ть and add -ло."},
        {"ru_word": "Говорить", "zh_word": "说", "level": "A1",
         "prompt": "请写出 \"Говорить\" 的过去时阳性形式（он）。",
         "prompt_en": "Write the past tense masculine form of \"Говорить\" (он).",
         "answers": ["говорил"], "display_answer": "говорил",
         "explanation": "规则：-ть 去掉加 -л。",
         "explanation_en": "Rule: Remove -ть and add -л."},
        {"ru_word": "Жить", "zh_word": "生活/住", "level": "A2",
         "prompt": "请写出 \"Жить\" 的过去时阳性形式（он）。",
         "prompt_en": "Write the past tense masculine form of \"Жить\" (он).",
         "answers": ["жил"], "display_answer": "жил",
         "explanation": "规则：жить 的过去时阳性是 жил。",
         "explanation_en": "Rule: жить becomes жил in the masculine past tense."},
        {"ru_word": "Идти", "zh_word": "走", "level": "A2",
         "prompt": "请写出 \"Идти\" 的过去时阳性形式（он）。",
         "prompt_en": "Write the past tense masculine form of \"Идти\" (он).",
         "answers": ["шёл"], "display_answer": "шёл",
         "explanation": "规则：идти 的过去时阳性是 шёл。",
         "explanation_en": "Rule: идти becomes шёл in the masculine past tense."},
        {"ru_word": "Мочь", "zh_word": "能够", "level": "A2",
         "prompt": "请写出 \"Мочь\" 的过去时阳性形式（он）。",
         "prompt_en": "Write the past tense masculine form of \"Мочь\" (он).",
         "answers": ["мог"], "display_answer": "мог",
         "explanation": "规则：мочь 的过去时阳性是 мог。",
         "explanation_en": "Rule: мочь becomes мог in the masculine past tense."},

        # ===== 形容词性数格一致 =====
        {"ru_word": "Новый", "zh_word": "新的", "level": "A2",
         "prompt": "请写出 \"Новый\" 的阴性单数形式（与 книга 搭配）。",
         "prompt_en": "Write the feminine singular form of \"Новый\".",
         "answers": ["новая"], "display_answer": "новая",
         "explanation": "规则：-ый 结尾形容词，阴性单数变为 -ая。",
         "explanation_en": "Rule: Adjectives ending in -ый change to -ая in feminine singular."},
        {"ru_word": "Красивый", "zh_word": "漂亮的", "level": "A2",
         "prompt": "请写出 \"Красивый\" 的阴性单数形式。",
         "prompt_en": "Write the feminine singular form of \"Красивый\".",
         "answers": ["красивая"], "display_answer": "красивая",
         "explanation": "规则：-ый 结尾形容词，阴性单数变为 -ая。",
         "explanation_en": "Rule: Adjectives ending in -ый change to -ая in feminine singular."},
        {"ru_word": "Большой", "zh_word": "大的", "level": "A0",
         "prompt": "请写出 \"Большой\" 的阴性单数形式。",
         "prompt_en": "Write the feminine singular form of \"Большой\".",
         "answers": ["большая"], "display_answer": "большая",
         "explanation": "规则：-ой 结尾形容词，阴性单数变为 -ая。",
         "explanation_en": "Rule: Adjectives ending in -ой change to -ая in feminine singular."},
        {"ru_word": "Новый", "zh_word": "新的", "level": "A2",
         "prompt": "请写出 \"Новый\" 的中性单数形式（与 окно 搭配）。",
         "prompt_en": "Write the neuter singular form of \"Новый\".",
         "answers": ["новое"], "display_answer": "новое",
         "explanation": "规则：-ый 结尾形容词，中性单数变为 -ое。",
         "explanation_en": "Rule: Adjectives ending in -ый change to -ое in neuter singular."},
        {"ru_word": "Красивый", "zh_word": "漂亮的", "level": "A2",
         "prompt": "请写出 \"Красивый\" 的复数形式。",
         "prompt_en": "Write the plural form of \"Красивый\".",
         "answers": ["красивые"], "display_answer": "красивые",
         "explanation": "规则：-ый 结尾形容词，复数变为 -ые。",
         "explanation_en": "Rule: Adjectives ending in -ый change to -ые in plural."},
        {"ru_word": "Хороший", "zh_word": "好的", "level": "A1",
         "prompt": "请写出 \"Хороший\" 的阴性单数形式。",
         "prompt_en": "Write the feminine singular form of \"Хороший\".",
         "answers": ["хорошая"], "display_answer": "хорошая",
         "explanation": "规则：-ий 结尾形容词，阴性单数变为 -ая。",
         "explanation_en": "Rule: Adjectives ending in -ий change to -ая in feminine singular."},
        {"ru_word": "Русский", "zh_word": "俄语的/俄罗斯的", "level": "A1",
         "prompt": "请写出 \"Русский\" 的阴性单数形式。",
         "prompt_en": "Write the feminine singular form of \"Русский\".",
         "answers": ["русская"], "display_answer": "русская",
         "explanation": "规则：-ий 结尾形容词，阴性单数变为 -ая。",
         "explanation_en": "Rule: Adjectives ending in -ий change to -ая in feminine singular."},
        {"ru_word": "Синий", "zh_word": "蓝色的", "level": "A2",
         "prompt": "请写出 \"Синий\" 的阴性单数形式。",
         "prompt_en": "Write the feminine singular form of \"Синий\".",
         "answers": ["синяя"], "display_answer": "синяя",
         "explanation": "规则：-ий 结尾软变化形容词，阴性单数变为 -яя。",
         "explanation_en": "Rule: Soft-stem adjectives ending in -ий change to -яя in feminine singular."},

        # ===== 人称代词变格 =====
        {"ru_word": "Я", "zh_word": "我", "level": "A1",
         "prompt": "请写出 \"Я\" 的所有格形式。",
         "prompt_en": "Write the genitive form of \"Я\".",
         "answers": ["меня"], "display_answer": "меня",
         "explanation": "人称代词 я 的所有格是 меня。",
         "explanation_en": "The genitive of я is меня."},
        {"ru_word": "Я", "zh_word": "我", "level": "A2",
         "prompt": "请写出 \"Я\" 的与格形式。",
         "prompt_en": "Write the dative form of \"Я\".",
         "answers": ["мне"], "display_answer": "мне",
         "explanation": "人称代词 я 的与格是 мне。",
         "explanation_en": "The dative of я is мне."},
        {"ru_word": "Ты", "zh_word": "你", "level": "A1",
         "prompt": "请写出 \"Ты\" 的所有格形式。",
         "prompt_en": "Write the genitive form of \"Ты\".",
         "answers": ["тебя"], "display_answer": "тебя",
         "explanation": "人称代词 ты 的所有格是 тебя。",
         "explanation_en": "The genitive of ты is тебя."},
        {"ru_word": "Он", "zh_word": "他", "level": "A1",
         "prompt": "请写出 \"Он\" 的所有格形式。",
         "prompt_en": "Write the genitive form of \"Он\".",
         "answers": ["его"], "display_answer": "его",
         "explanation": "人称代词 он 的所有格是 его。",
         "explanation_en": "The genitive of он is его."},
        {"ru_word": "Она", "zh_word": "她", "level": "A1",
         "prompt": "请写出 \"Она\" 的所有格形式。",
         "prompt_en": "Write the genitive form of \"Она\".",
         "answers": ["её"], "display_answer": "её",
         "explanation": "人称代词 она 的所有格是 её。",
         "explanation_en": "The genitive of она is её."},
        {"ru_word": "Мы", "zh_word": "我们", "level": "A1",
         "prompt": "请写出 \"Мы\" 的所有格形式。",
         "prompt_en": "Write the genitive form of \"Мы\".",
         "answers": ["нас"], "display_answer": "нас",
         "explanation": "人称代词 мы 的所有格是 нас。",
         "explanation_en": "The genitive of мы is нас."},

        # ===== 物主代词 =====
        {"ru_word": "Мой", "zh_word": "我的", "level": "A1",
         "prompt": "请写出 \"Мой\" 的阴性单数形式。",
         "prompt_en": "Write the feminine singular form of \"Мой\".",
         "answers": ["моя"], "display_answer": "моя",
         "explanation": "物主代词 мой 的阴性单数是 моя。",
         "explanation_en": "The feminine singular of мой is моя."},
        {"ru_word": "Твой", "zh_word": "你的", "level": "A1",
         "prompt": "请写出 \"Твой\" 的阴性单数形式。",
         "prompt_en": "Write the feminine singular form of \"Твой\".",
         "answers": ["твоя"], "display_answer": "твоя",
         "explanation": "物主代词 твой 的阴性单数是 твоя。",
         "explanation_en": "The feminine singular of твой is твоя."},
        {"ru_word": "Наш", "zh_word": "我们的", "level": "A2",
         "prompt": "请写出 \"Наш\" 的阴性单数形式。",
         "prompt_en": "Write the feminine singular form of \"Наш\".",
         "answers": ["наша"], "display_answer": "наша",
         "explanation": "物主代词 наш 的阴性单数是 наша。",
         "explanation_en": "The feminine singular of наш is наша."},
        {"ru_word": "Ваш", "zh_word": "您的/你们的", "level": "A2",
         "prompt": "请写出 \"Ваш\" 的阴性单数形式。",
         "prompt_en": "Write the feminine singular form of \"Ваш\".",
         "answers": ["ваша"], "display_answer": "ваша",
         "explanation": "物主代词 ваш 的阴性单数是 ваша。",
         "explanation_en": "The feminine singular of ваш is ваша."},

        # ===== 动词将来时 =====
        {"ru_word": "Читать", "zh_word": "阅读", "level": "A2",
         "prompt": "请写出 \"Читать\" 的将来时第一人称单数（я）。",
         "prompt_en": "Write the future tense 1st person singular of \"Читать\" (я).",
         "answers": ["буду читать"], "display_answer": "буду читать",
         "explanation": "规则：未完成体将来时用 быть + 不定式，я 用 буду。",
         "explanation_en": "Rule: Imperfective future uses быть + infinitive. Я takes буду."},
        {"ru_word": "Говорить", "zh_word": "说", "level": "A2",
         "prompt": "请写出 \"Говорить\" 的将来时第三人称单数（он）。",
         "prompt_en": "Write the future tense 3rd person singular of \"Говорить\" (он).",
         "answers": ["будет говорить"], "display_answer": "будет говорить",
         "explanation": "规则：未完成体将来时，он 用 будет + 不定式。",
         "explanation_en": "Rule: Imperfective future. Он takes будет + infinitive."},
        {"ru_word": "Прочитать", "zh_word": "读完", "level": "A2",
         "prompt": "请写出 \"Прочитать\" 的将来时第一人称单数（я）。",
         "prompt_en": "Write the future tense 1st person singular of \"Прочитать\" (я).",
         "answers": ["прочитаю"], "display_answer": "прочитаю",
         "explanation": "规则：完成体动词变位即表示将来时，прочитать → прочитаю。",
         "explanation_en": "Rule: Perfective verbs use their conjugation for future tense. прочитать → прочитаю."},

        # ===== 动词命令式 =====
        {"ru_word": "Читать", "zh_word": "阅读", "level": "A2",
         "prompt": "请写出 \"Читать\" 的命令式单数形式（ты）。",
         "prompt_en": "Write the imperative singular form of \"Читать\" (ты).",
         "answers": ["читай"], "display_answer": "читай",
         "explanation": "规则：-ать 结尾动词，命令式单数为 -ай。",
         "explanation_en": "Rule: Verbs ending in -ать take -ай in imperative singular."},
        {"ru_word": "Говорить", "zh_word": "说", "level": "A2",
         "prompt": "请写出 \"Говорить\" 的命令式单数形式（ты）。",
         "prompt_en": "Write the imperative singular form of \"Говорить\" (ты).",
         "answers": ["говори"], "display_answer": "говори",
         "explanation": "规则：-ить 结尾动词，命令式单数为 -и。",
         "explanation_en": "Rule: Verbs ending in -ить take -и in imperative singular."},
        {"ru_word": "Сказать", "zh_word": "说（完成体）", "level": "A2",
         "prompt": "请写出 \"Сказать\" 的命令式单数形式（ты）。",
         "prompt_en": "Write the imperative singular form of \"Сказать\" (ты).",
         "answers": ["скажи"], "display_answer": "скажи",
         "explanation": "规则：сказать 的命令式是 скажи（з→ж 音变）。",
         "explanation_en": "Rule: сказать becomes скажи in imperative (з→ж mutation)."},
    ]

    def __init__(self, db_manager, word_provider=None, mistake_manager=None):
        self.db = db_manager
        self.word_provider = word_provider
        self.mistake_manager = mistake_manager
        self._init_quiz_history()

    def _init_quiz_history(self):
        with self.db._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS quiz_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    mode TEXT NOT NULL,
                    ru_word TEXT,
                    zh_word TEXT,
                    user_answer TEXT,
                    correct_answer TEXT,
                    is_correct INTEGER NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def _get_words(self, count=1, level=None):
        words = None
        if self.word_provider and hasattr(self.word_provider, "get_random_words"):
            try:
                words = self.word_provider.get_random_words(count=count, level=level)
            except TypeError:
                words = self.word_provider.get_random_words(count, level)
        elif self.word_provider and hasattr(self.word_provider, "get_all"):
            words = self.word_provider.get_all()
            random.shuffle(words)
            words = words[:count]

        if words is None:
            words = self.db.get_random_words(count=count, level=level)

        return [self._normalize_word_item(word) for word in words]

    def _normalize_word_item(self, word):
        if isinstance(word, dict):
            return {
                "ru_word": word.get("ru_word") or word.get("russian") or word.get("ru"),
                "zh_word": word.get("zh_word") or word.get("chinese") or word.get("zh"),
                "en_word": word.get("en_word") or word.get("english") or word.get("en", ""),
                "level": word.get("level"),
            }

        ru_word = word[0]
        zh_word = word[1]
        en_word = ""
        level = None

        if len(word) >= 4:
            en_word = word[2] if word[2] else ""
            level = word[3]
        elif len(word) == 3:
            if word[2] in ('A0', 'A1', 'A2'):
                level = word[2]
            else:
                en_word = word[2] if word[2] else ""

        return {"ru_word": ru_word, "zh_word": zh_word, "en_word": en_word, "level": level}

    def get_random_word(self, level=None):
        words = self._get_words(count=1, level=level)
        if not words and level:
            words = self._get_words(count=1)
        return words[0] if words else None

    def build_quiz_question(self, mode="ru_to_zh", level=None, user_id=None, options_count=4, lang='zh'):
        correct_word = self._pick_word(user_id, level=level)
        if not correct_word:
            return None

        if mode == "ru_to_zh":
            answer_key = "en_word" if lang == "en" else "zh_word"
            prompt_key = "ru_word"
            prompt_text = "Select the correct translation for"
        else:
            answer_key = "ru_word"
            prompt_key = "en_word" if lang == "en" else "zh_word"
            prompt_text = "Select the Russian word for"

        candidates = self._get_words(count=30, level=level)
        if len(candidates) < options_count and level:
            candidates = self._get_words(count=30)

        options = [correct_word[answer_key]]
        for word in candidates:
            option = word[answer_key]
            if option and self._normalize(option) not in {self._normalize(item) for item in options}:
                options.append(option)
            if len(options) == options_count:
                break

        if len(options) < options_count:
            return None

        random.shuffle(options)
        correct_index = next(
            index for index, option in enumerate(options)
            if self.check_answer(correct_word[answer_key], option)
        )

        return {
            "mode": mode,
            "prompt": f"{prompt_text} \"{correct_word[prompt_key]}\":",
            "ru_word": correct_word["ru_word"],
            "zh_word": correct_word["zh_word"],
            "correct_answer": correct_word[answer_key],
            "correct_index": correct_index,
            "options": options,
        }

    def build_exercise(self, level=None, user_id=None, lang='zh'):
        exercises = self.PRESET_EXERCISES
        if self.mistake_manager and user_id:
            mistakes = self.mistake_manager.get_mistake_words(user_id)
            if mistakes:
                mistake_ru = [m["ru_word"] for m in mistakes]
                for ex in exercises:
                    if ex["ru_word"] in mistake_ru:
                        return self._localize_exercise(ex, lang)
        if level and level not in ("未设置", "未记录"):
            level_matches = [item for item in exercises if item["level"] == level]
            if level_matches:
                exercises = level_matches
        ex = random.choice(exercises) if exercises else None
        return self._localize_exercise(ex, lang) if ex else None

    def _localize_exercise(self, ex, lang):
        if lang == 'en':
            return {
                "ru_word": ex["ru_word"],
                "zh_word": ex["zh_word"],
                "level": ex["level"],
                "prompt": ex.get("prompt_en", ex["prompt"]),
                "answers": ex["answers"],
                "display_answer": ex["display_answer"],
                "explanation": ex.get("explanation_en", ex["explanation"]),
            }
        return ex

    def check_answer(self, expected, actual):
        actual_normalized = self._normalize(actual)
        for candidate in self._answer_candidates(expected):
            if self._normalize(candidate) == actual_normalized:
                return True
        return False

    def save_result(self, user_id, mode, ru_word, zh_word, user_answer, correct_answer, is_correct):
        with self.db._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO quiz_history (
                    user_id, mode, ru_word, zh_word,
                    user_answer, correct_answer, is_correct
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, mode, ru_word, zh_word, user_answer, correct_answer, 1 if is_correct else 0),
            )
            conn.commit()

        if self.mistake_manager and ru_word and zh_word:
            self.mistake_manager.record(user_id, ru_word, zh_word, is_correct)

    def _pick_word(self, user_id, level=None):
        if self.mistake_manager and user_id:
            mistakes = self.mistake_manager.get_mistake_words(user_id)
            if mistakes and random.random() < 0.8:
                word = random.choice(mistakes)
                # 错题库只有 ru_word 和 zh_word，需要补 en_word
                if "en_word" not in word:
                    with self.db._get_connection() as conn:
                        row = conn.execute(
                            "SELECT english FROM word_bank WHERE russian=? AND chinese=?",
                            (word["ru_word"], word["zh_word"])
                        ).fetchone()
                    word["en_word"] = row[0] if row else ""
                return word
        return self.get_random_word(level=level)

    def _answer_candidates(self, expected):
        if isinstance(expected, (list, tuple, set)):
            candidates = []
            for item in expected:
                candidates.extend(self._answer_candidates(item))
            return candidates

        parts = re.split(r"[/,，;；、]", str(expected))
        return [expected, *parts]

    def _normalize(self, value):
        value = str(value or "").strip().lower().replace("ё", "е")
        return re.sub(r"\s+", " ", value)