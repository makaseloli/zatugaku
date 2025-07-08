from PIL import Image, ImageDraw, ImageFont
from image_process import generate_image
from voice_process import generate_voice
import json
import pathlib
import os

def wrap_text(text, font, max_width):
    """テキストを指定された幅で折り返す"""

    characters = list(text)
    lines = []
    current_line = ""
    
    print(f"テキスト折り返し開始: max_width={max_width}")
    print(f"元のテキスト: {text}")
    
    for char in characters:
        test_line = current_line + char
        
        bbox = font.getbbox(test_line)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
                current_line = char
            else:
                lines.append(char)
                current_line = ""
    
    if current_line:
        lines.append(current_line)
    
    print(f"折り返し結果: {lines}")
    return lines


def process_json(json_data, toggle_shorts, debug=False):
    """JSONデータを処理して画像と音声を生成する"""

    json_data = json.loads(json_data)

    for key, value in json_data.items():
        if not debug:
            generate_image(value[2], key)

        base = Image.new('RGB', (1920, 1080), (255, 255, 255))
        if toggle_shorts:
            base = Image.new('RGB', (1080, 1920), (255, 255, 255))

        if debug:
            ai_img = Image.new('RGB', (1024, 1024), (255, 0, 0))
        else:
            ai_img = Image.open(f"./temp/ai/{key}.png")

        ai_width, ai_height = ai_img.size

        bairitu = 0.7

        if toggle_shorts:
            bairitu = 0.8

        ai_width = int(ai_width * bairitu)
        ai_height = int(ai_height * bairitu)

        ai_img = ai_img.resize((ai_width, ai_height), Image.Resampling.LANCZOS)
        
        center_x = (1920 - ai_width) // 2
        center_y = (180 + 540 - ai_height) // 2
        if toggle_shorts:
            center_x = (1080 - ai_width) // 2
            center_y = (1050 - ai_height) // 2
        
        base.paste(ai_img, (center_x, center_y))

        page1 = base.copy()
        page2 = base.copy()

        font_path = sorted(os.listdir("./temp/font"))[0]
        font_path = f"./temp/font/{font_path}"

        font = ImageFont.truetype(font_path, 60)

        text1 = value[0]
        text2 = value[1]

        text_area_width = 1850
        text_area_start_y = 540
        text_area_height = 540

        if toggle_shorts:
            text_area_width = 960
            text_area_start_y = 540
            text_area_height = 1080 + 100

        lines1 = wrap_text(text1, font, text_area_width)
        lines2 = wrap_text(text2, font, text_area_width)

        line_height = 50
        text1_height = len(lines1) * line_height
        text2_height = len(lines2) * line_height

        def draw_text(basenoimage, text_height, linesnn):
            """テキストを画像に描画する"""
            
            draw = ImageDraw.Draw(basenoimage)
            start_y = text_area_start_y + (text_area_height - text_height) // 2
            
            current_y = start_y
            for i, line in enumerate(linesnn):
                if line:
                    bbox = font.getbbox(line)
                    text_width = bbox[2] - bbox[0]
                    text_x = (1920 - text_width) // 2
                    if toggle_shorts:
                        text_x = (1080 - text_width) // 2
                    
                    text_color = (0, 0, 0)
                    
                    draw.text((text_x, current_y), line, fill=text_color, font=font)
                
                current_y += line_height
            
        if not pathlib.Path("./temp").exists():
            pathlib.Path("./temp").mkdir(parents=True, exist_ok=True)

        if not pathlib.Path("./tem/key").exists():
            pathlib.Path("./temp/key").mkdir(parents=True, exist_ok=True)

        draw_text(page1, text1_height, lines1)
        draw_text(page2, text2_height, lines2)


        page1.save(f"./temp/key/{key}_page1.png")
        page2.save(f"./temp/key/{key}_page2.png")

        generate_voice(text1, f"{key}_page1")
        generate_voice(text2, f"{key}_page2")

    generated_files = os.listdir("./temp/ai")
    generated_files_path = []

    for file in generated_files:
        generated_files_path.append(f"./temp/ai/{file}")

    print(f"生成されたファイル: {generated_files_path}")

    return sorted(generated_files_path)


if __name__ == "__main__":
    process_json(
    """
    {
        "key1": [
            "これは1ページ目です", 
            "これは2ページ目です",
            "A beautiful landscape with mountains and a river"
        ]
    }
    """,
    toggle_shorts=False, debug=True)