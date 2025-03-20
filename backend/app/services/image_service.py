import aiohttp
import os
from typing import List
from ..config import get_settings
from ..models.property import PropertyImage
from sqlalchemy.orm import Session

settings = get_settings()

class ImageService:
    def __init__(self, db: Session):
        self.db = db
        self.session = aiohttp.ClientSession()
        os.makedirs(settings.IMAGES_STORE_PATH, exist_ok=True)

    async def download_images(self, property_id: int, image_urls: List[str]):
        """
        Download and store images for a property
        """
        for url in image_urls:
            try:
                local_path = await self._download_image(url, property_id)
                if local_path:
                    image = PropertyImage(
                        property_id=property_id,
                        url=url,
                        local_path=local_path
                    )
                    self.db.add(image)
            except Exception as e:
                print(f"Error downloading image {url}: {str(e)}")
        
        self.db.commit()

    async def _download_image(self, url: str, property_id: int) -> str:
        """
        Download a single image and return its local path
        """
        async with self.session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                if len(content) > settings.MAX_IMAGE_SIZE:
                    return None
                
                filename = f"{property_id}_{os.path.basename(url)}"
                local_path = os.path.join(settings.IMAGES_STORE_PATH, filename)
                
                with open(local_path, 'wb') as f:
                    f.write(content)
                
                return local_path
        return None
