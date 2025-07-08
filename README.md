# 雑学動画ジェネレータ
shortsでよく見る雑学動画を生成します。

## 設定
.env.exampleに従ってください

## 起動方法
```shell
git clone https://github.com/makaseloli/zatugaku.git
uv sync
.venv/bin/python main.py
```

## 使用方法
左のタブから順に実行してください

## 推奨スペック
- VRAM32GB以上
- RAM64GB以上
  
メモリさえあればCPUでも動きます

## 使用したもの
### 主要なライブラリ
- Diffusers
- Gradio
- LlamaIndex
- Open JTalk

### 開発に使用
- VSC
- GH Copilot

## 既知の問題
- LLMがPDFを読めてないっぽい

## 注意事項
このプログラムの使用によって発生した問題に対し、私は一切責任を負いません。
