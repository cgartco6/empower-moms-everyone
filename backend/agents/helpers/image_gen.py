import aiohttp
from backend.config.settings import settings

class ImageGeneratorHelper:
    """Helper agent that creates engaging, memorable illustrations for course materials."""
    
    async def generate(self, prompt: str, style: str = "watercolor") -> str:
        """Returns a URL of the generated image (DALL·E, Stable Diffusion, etc.)"""
        # Simplified – in reality call an image API
        if settings.IMAGE_PROVIDER == "dalle":
            async with aiohttp.ClientSession() as session:
                payload = {
                    "prompt": f"{prompt}, {style}, fun, educational",
                    "n": 1,
                    "size": "1024x1024"
                }
                headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
                async with session.post(
                    "https://api.openai.com/v1/images/generations",
                    json=payload,
                    headers=headers
                ) as resp:
                    data = await resp.json()
                    return data['data'][0]['url']
        return "https://placehold.co/1024x1024?text=Fun+Course+Image"
