import torch

from diffusers import AutoPipelineForText2Image
from PIL import Image


class SdxlTurbo:

    def __init__(self) -> None:
        self.pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
        self.pipe.to("cuda")

    def generate(self, prompt: str) -> Image:
        return self.pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]