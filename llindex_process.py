from config import OLLAMA_HOST, OLLAMA_MODEL, SYSTEM_PROMPT

from llama_index.core import (
    Settings,
    VectorStoreIndex,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
import pathlib
from llama_index.core.node_parser import CodeSplitter
import re
from llama_index.core import Document
import os

Settings.embed_model = HuggingFaceEmbedding("BAAI/bge-small-en-v1.5")
Settings.llm         = Ollama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_HOST,
    request_timeout=1000
    )

index = None

def strip_think(text: str) -> str:
    """<think>タグを削除する関数"""

    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)    

def create_index():
    """メタデータ付きでコードインデックスを作成"""

    repo_path = os.listdir("./temp/repo")

    if not repo_path:
        return

    repo_path = "./temp/repo/" + repo_path[0]

    print(repo_path)

    global index
    
    documents = []
    repo_path = pathlib.Path(repo_path)
    
    # コードファイルを手動で処理してメタデータを追加
    for file_path in repo_path.rglob("*"):
        if (file_path.is_file() and 
            file_path.suffix in ['.py', '.js', '.md', '.txt'] and
            '.git' not in file_path.parts):
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # メタデータを作成
                metadata = {
                    "file_path": str(file_path),
                    "file_name": file_path.name,
                    "file_type": file_path.suffix,
                    "directory": str(file_path.parent),
                    "file_size": len(content),
                    "is_code": file_path.suffix in ['.py', '.js', '.ts', '.java', '.cpp']
                }

                print(metadata)
                
                # Pythonファイルの場合、関数やクラス情報を抽出
                if file_path.suffix == '.py':
                    import ast
                    try:
                        tree = ast.parse(content)
                        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                        metadata["functions"] = functions
                        metadata["classes"] = classes
                    except:
                        pass
                
                doc = Document(text=content, metadata=metadata)
                documents.append(doc)
                
            except Exception as e:
                print(f"ファイル読み込みエラー {file_path}: {e}")
                continue
    
    if documents:
        # コード専用の分割器を使用
        code_splitter = CodeSplitter(
            language="python",
            chunk_lines=50,
            chunk_lines_overlap=20,
            max_chars=2000
        )
        
        index = VectorStoreIndex.from_documents(
            documents,
            transformations=[code_splitter]
        )
        
        print(f"拡張インデックスを作成: {len(documents)}ファイル")
        return "インデックスが正常に作成されました。"
    
    return "インデックス作成に失敗しました。"
    

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


def generate_zatugaku(num: int):
    """文章を生成する関数"""

    global index
    create_index()

    if index is None:
        return "インデックスが作成されていません。先に資料をアップロードしてください。"
    
    print(get_index_info())

    query = f"""
    {SYSTEM_PROMPT}
    与えられたリポジトリに関する説明を{num}個出力してください。
    """

    response = index.as_query_engine().query(query)
    return strip_think(str(response))

if __name__ == "__main__":
    print(generate_zatugaku(4))