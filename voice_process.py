import pyopenjtalk
import scipy.io.wavfile as wavfile
import numpy as np
import pathlib

def generate_voice(prompt, file_name):
    """音声を生成する関数"""

    x, sr = pyopenjtalk.tts(prompt)

    pathlib.Path("./temp").mkdir(parents=True, exist_ok=True)
    pathlib.Path("./temp/cv").mkdir(parents=True, exist_ok=True)

    wavfile.write(f"./temp/cv/{file_name}.wav", sr, x.astype(np.int16))


if __name__ == "__main__":
    generate_voice("こんにちは、これはテストです", "test_voice")
