import torch

from diffusers import AutoPipelineForText2Image
from PIL import Image
from io import BytesIO


class SdxlTurbo:

    def __init__(self) -> None:
        self.pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
        self.pipe.to("cuda")

    def generate(self, prompt: str) -> BytesIO:
        image = self.pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]

        image_bytes_stream = BytesIO()
        image_bytes_stream.name = 'tmp.jpeg'
        image.save(image_bytes_stream, 'JPEG')
        image_bytes_stream.seek(0)

        return image_bytes_stream
       