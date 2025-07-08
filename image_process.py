from diffusers import FluxPipeline
import torch
import pathlib

torch.cuda.empty_cache()

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell",
    torch_dtype=torch.bfloat16,
    use_safetensors=True,
)

pipe.enable_attention_slicing(1)

pipe.enable_sequential_cpu_offload()

def generate_image(prompt: str, file_name: str):
    """画像を生成する関数"""

    image = pipe(
        prompt,
        guidance_scale=0.0,
        num_inference_steps=4,
        max_sequence_length=256,
        generator=torch.Generator("cpu").manual_seed(0)
    ).images[0]
    torch.cuda.empty_cache()
    

    pathlib.Path("./temp").mkdir(parents=True, exist_ok=True)
    pathlib.Path("./temp/ai").mkdir(parents=True, exist_ok=True)

    image.save(f"./temp/ai/{file_name}.png")

if __name__ == "__main__":
    generate_image("A beautiful landscape with mountains and a river", "output_image.png")