# 俄语助手机器人

这是一个基于 Telegram 的俄语学习机器人项目，支持用户注册、等级设置、生词本、单词学习、变格/变位练习和随机测验。

## 主要功能

- `/start`：启动机器人并保存用户信息
- `/help`：打开功能菜单
- `/level`：查看当前俄语水平
- `/view_words`：查看个人生词本
- `/cancel`：退出当前输入状态
- `/exercise`：随机变格/变位练习
- `/quiz`：随机选择题测验，支持俄语到中文、中文到俄语

## 项目结构

```text
robot/
├── main.py
├── word_bank.json
├── requirements.txt
├── database/
│   └── db_manager.py
├── handlers/
│   ├── grammar.py
│   └── quiz.py
├── managers/
│   └── quiz_manager.py
├── utils/
│   └── message_helper.py
└── data/
    └── 运行时自动生成 SQLite 数据库
```

## 安装与启动

建议使用项目内虚拟环境，不依赖本机全局 Python 包。

```powershell
cd robot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\main.py
```

也可以不激活虚拟环境，直接使用虚拟环境里的 Python 启动：

```powershell
cd robot
.\.venv\Scripts\python.exe .\main.py
```

## Token 配置说明

当前项目的 Telegram Bot Token 写在 `main.py` 的 `TOKEN` 变量中。提交或分享项目之前，建议改为从环境变量读取，避免 Token 泄露。

## C 模块说明

C 同学负责的练习与测验模块已拆分为：

- `managers/quiz_manager.py`：题目生成、答案判断、测验记录入库
- `handlers/grammar.py`：`/exercise` 变格/变位练习
- `handlers/quiz.py`：`/quiz` 随机选择题测验

测验结果会保存到 SQLite 的 `quiz_history` 表中。

## 数据库说明

`data/bot_database.db` 是运行时数据库文件，启动项目时会自动创建表结构。打包或提交项目时可以不包含该文件。

## 后续建议

- 将 Token 改成环境变量读取
- 补充 `config.py`
- 将生词本逻辑继续拆到 `handlers/words.py` 和 `managers/word_manager.py`
- 增加测试用例
- 部署到服务器或使用 ngrok 做本地演示
