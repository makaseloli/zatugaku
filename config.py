import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:30b-a3b")

GRADIO_HOST = os.getenv("GRADIO_HOST", "127.0.0.1")
GRADIO_PORT = int(os.getenv("GRADIO_PORT", 7860))

HF_TOKEN = os.getenv("HF_TOKEN", "")
GH_TOKEN = os.getenv("GH_TOKEN", "")

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Klee+One&display=swap');


/* 全体のフォント設定 */
* {
    font-family: "Klee One", cursive !important;
}

"""

SYSTEM_PROMPT = """
あなたは与えられたリポジトリの解説に関する動画の台本を作成してください。
リポジトリの内容を理解し、説明することが求められています。
説明を1つあたり2ページに分けて書いてください。

必ず以下のjsonフォーマットで出力してください。  

【出力例】

{
    "key1": [
        {
            "text": [
                "1ページ目の内容を日本語で入力してください。",
                "2ページ目の内容を日本語で入力してください。"
            ],
            "image_prompt": "上記の説明に必要な画像を生成するためプロンプトを英語で入力してください。文字を含む場合は詳細な説明にしてください。"
        }
    ]
}

2つ以上の場合はkey2, key3のように増やしてください。
"""
