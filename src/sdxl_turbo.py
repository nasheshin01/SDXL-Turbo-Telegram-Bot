import torch

from diffusers import AutoPipelineForText2Image
from io import BytesIO
from random import randint


class SdxlQuery:
    """Класс запроса для модели SDXL"""

    def __init__(self, main_prompt: str) -> None:
        self.main_prompt = main_prompt
        self.seed = randint(0, 100000)
        self.tags = ['vectorized image', '2d', 'high resolution', 'powerpoint style']

    def get_full_prompt(self) -> str:
        return ', '.join([self.main_prompt, *self.tags])
    
    def query_info(self):
        main_prompt_info = f"Main prompt: {self.main_prompt}"
        tags_info = 'Tags: ' + ', '.join(self.tags)
        seed_info = f'Random seed: {self.seed}'

        return '\n'.join([main_prompt_info, tags_info, seed_info])

    def add_tag(self, tag: str):
        self.tags.append(tag)

    def try_remove_tag(self, tag: str) -> bool:
        if tag in self.tags:
            self.tags.remove(tag)
            return True
        
        return False
    
    def try_remove_last_tag(self) -> bool:
        if len(self.tags) == 0:
            return False
        
        self.tags = self.tags[:-1]
        return True
    
    def clear_tags(self):
        self.tags = []
        
    def new_seed(self):
        self.seed = randint(0, 100000)

        

class SdxlTurbo:
    """Класс модели SDXL-Turbo. Для генерации используется функция generate"""

    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
        self.pipe.to(self.device)

    def generate(self, query: SdxlQuery) -> BytesIO:
        generator = [torch.Generator(device=self.device).manual_seed(query.seed)]
        prompt = query.get_full_prompt()
        image = self.pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0, generator=generator).images[0]

        image_bytes_stream = BytesIO()
        image_bytes_stream.name = 'tmp.jpeg'
        image.save(image_bytes_stream, 'JPEG')
        image_bytes_stream.seek(0)

        return image_bytes_stream
       