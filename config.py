import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:30b-a3b")

GRADIO_HOST = os.getenv("GRADIO_HOST", "127.0.0.1")
GRADIO_PORT = int(os.getenv("GRADIO_PORT", 7860))

HF_TOKEN = os.getenv("HF_TOKEN", "")

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Klee+One&display=swap');


/* 全体のフォント設定 */
* {
    font-family: "Klee One", cursive !important;
}

"""

SYSTEM_PROMPT = """
あなたは雑学に関する動画の台本を作成してください。
指定されたジャンルにまつわる雑学を１つあたり２ページに分けて簡潔に短く書いてください。だ、である口調でお願いします。

以下のjsonフォーマットに従ってください。
{
    "key1" : [
        "1ページ目の内容を日本語で入力してください。",
        "2ページ目の内容を日本語で入力してください。",
        "上記の説明に必要な画像を生成するためプロンプトを英語で入力してください。"
    ]
}
数の指定がありますので、2つ以上の場合はkey2, key3のように増やしてください。
"""
