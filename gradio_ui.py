import gradio as gr
import tomli
from pathlib import Path
from config import CUSTOM_CSS
from llindex_process import create_index, generate_zatugaku, clear_index
import pathlib
from generate_imagevoice import process_json
from generate_video import finally_create_video
import shutil


def get_version():
    """pyproject.tomlを直接読み取ってバージョンを取得"""
    try:
        pyproject_path = Path(__file__).parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            data = tomli.load(f)
        return data["project"]["version"]
    except (FileNotFoundError, KeyError):
        return "unknown"

    
def clear_index_handler():
    """インデックスを消去するハンドラー"""
    clear_index()
    return "インデックスが消去されました。"


def image_gen_handler(json_str, toggle_shorts):
    """画像生成のハンドラー"""
    return process_json(json_str, toggle_shorts)


def clean_temp_directory():
    """final_video_with_bgm.mp4以外のtempディレクトリ内のファイルを削除"""

    temp_dir = Path("./temp")
    keep_file = temp_dir / "final_video_with_bgm.mp4"
    
    if not temp_dir.exists():
        return "tempディレクトリが存在しません"
    
    deleted_count = 0
    
    for item in temp_dir.rglob("*"):
        if item.is_file() and item != keep_file:
            item.unlink()
            deleted_count += 1
            print(f"削除: {item}")
    
    for item in temp_dir.rglob("*"):
        if item.is_dir() and not any(item.iterdir()):
            item.rmdir()
            print(f"空のディレクトリを削除: {item}")
        

def video_gen_handler():
    """動画生成のハンドラー"""

    finally_create_video()
    clean_temp_directory()    

    return "./temp/final_video_with_bgm.mp4"

def process_upload(files, bgm_files, font_files):
    """アップロードされたファイルを処理するハンドラー"""

    if not files:
        return "資料がアップロードされていません"
    
    if not bgm_files:
        return "BGMファイルがアップロードされていません"
    
    if not font_files:
        return "フォントファイルがアップロードされていません"

    pathlib.Path("./temp/bgm").mkdir(parents=True, exist_ok=True)
    pathlib.Path("./temp/font").mkdir(parents=True, exist_ok=True)


    print(f"アップロードされたファイル: {[file.name for file in files]}")

    shutil.copy2(font_files.name, "./temp/font")
    shutil.copy2(bgm_files.name, "./temp/bgm")
    
    try:
        file_paths = [file.name for file in files]
        result = create_index(file_paths)
        return result
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"


def define_gradio_interface():
    """Gradioのインターフェースを定義"""

    with gr.Blocks(css=CUSTOM_CSS, theme=gr.themes.Base()) as gui:

        gr.Markdown(f"""# 雑学動画ジェネレータ""")

        with gr.Row():
            with gr.Tab("資料のアップロード"):

                with gr.Column():
                    gr.Markdown("""
                    ## 資料のアップロード
                    """)
                    upload_input = gr.File(
                        label="資料ファイルをアップロード",
                        file_types=[".pdf", ".txt", ".md", ".html", ".docx", ".csv", ".png", ".jpg", ".jpeg", ".webp", ".mp4", ".mp3", ".wav"],
                        file_count="multiple",
                    )
                    bgm_input = gr.File(
                        label="BGMファイルをアップロード",
                        file_types=[".mp3", ".wav"]
                    )
                    font_inuput = gr.File(
                        label="フォントファイルをアップロード",
                        file_types=[".ttf", ".otf"],
                    )

                    upload_input.clear(
                        fn=clear_index_handler,
                    )

                    upload_button = gr.Button("資料をアップロード")
                    upload_process = gr.Textbox(interactive=False, label="アップロード結果")

                    upload_button.click(
                        fn=process_upload,
                        inputs=[upload_input, bgm_input, font_inuput],
                        outputs=[upload_process]
                    )

            with gr.Tab("雑学の出力"):
                with gr.Column():
                    query_input = gr.Textbox(
                        label="雑学を生成したい質問を入力",
                        placeholder="例: 提供された情報",
                        interactive=True,
                        value="提供された情報"
                    )
                    num_input = gr.Number(
                        label="生成する雑学の数",
                        value=5,
                    )
                    generate_button = gr.Button("雑学を生成")
                    output_text = gr.Textbox(interactive=False, label="生成された雑学")

                    generate_button.click(
                        fn=generate_zatugaku,
                        inputs=[query_input, num_input],
                        outputs=[output_text]
                    )

            with gr.Tab("画像の作成"):
                with gr.Column():
                    toggle_shorts = gr.Checkbox(
                        label="ショート動画用の画像を生成",
                        value=False,
                        interactive=True
                    )
                    start_genimage = gr.Button("画像を生成")
                    genimage_output = gr.Gallery(
                        interactive=False,
                        type="filepath",
                    )


                    start_genimage.click(   
                        fn=image_gen_handler,
                        inputs=[output_text, toggle_shorts],
                        outputs=[genimage_output]
                    )

            with gr.Tab("動画の作成"):
                with gr.Column():
                    start_genvideo = gr.Button("動画を生成")
                    genvideo_output = gr.Video(interactive=False)

                    start_genvideo.click(
                        fn=video_gen_handler,
                        inputs=[],
                        outputs=[genvideo_output]
                    )

            with gr.Tab("設定"):

                gr.Markdown("## バージョン情報")
                version_info = f"バージョン: {get_version()}"
                gr.Markdown(version_info)

    return gui