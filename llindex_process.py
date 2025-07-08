from config import OLLAMA_HOST, OLLAMA_MODEL, SYSTEM_PROMPT

from llama_index.core import (
    Settings,
    VectorStoreIndex,
    SimpleDirectoryReader,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

import re

Settings.embed_model = HuggingFaceEmbedding("BAAI/bge-small-en-v1.5")
Settings.llm         = Ollama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_HOST,
    request_timeout=500
    )

index = None

def strip_think(text: str) -> str:
    """<think>タグを削除する関数"""

    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)


def create_index(file_paths):
    """インデックスを作成する関数"""

    global index

    if not file_paths:
        return "ファイルが指定されていません"
    
    docs = SimpleDirectoryReader(input_files=file_paths).load_data()

    if docs:
        index = VectorStoreIndex.from_documents(docs)
        print(index)
        return "インデックスが正常に作成されました"
    else:
        return "ドキュメントが見つかりませんでした"
    

def get_index_info():
    """インデックスの情報を取得する関数"""

    global index
    if index is None:
        return "インデックスが作成されていません"
    
    try:
        node_count = len(index.docstore.docs)
        return f"インデックスには {node_count} 個のノードが含まれています"
    except Exception as e:
        return f"インデックス情報取得エラー: {str(e)}"
    

def clear_index():
    """インデックスを全消去する関数"""

    global index
    index = None
    return "インデックスが消去されました。"


def generate_zatugaku(query: str, num: int):
    """雑学を生成する関数"""

    global index

    if index is None:
        return "インデックスが作成されていません。先に資料をアップロードしてください。"
    
    print(get_index_info())

    query = f"""
    {SYSTEM_PROMPT}
    {query}に関する雑学を{num}個出力してください。
    """

    response = index.as_query_engine().query(query)
    return strip_think(str(response))

if __name__ == "__main__":
    print(generate_zatugaku("提供された情報", 4))