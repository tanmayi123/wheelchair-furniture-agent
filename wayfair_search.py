from fastapi import FastAPI
from pydantic import BaseModel
import httpx
from bs4 import BeautifulSoup
import json

app = FastAPI()

class SearchRequest(BaseModel):
    category: str        # e.g. "beds", "floor lamps", "dressers"
    max_width_inches: float
    max_height_inches: float
    style: str           # e.g. "scandinavian minimalist"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_mock_products(category: str):
    """Mock data — replace with real crawl at hackathon"""
    mocks = {
        "beds": [
            {"name": "Nordic Platform Bed", "width_inches": 60, "height_inches": 14, "depth_inches": 80, "price": 499, "base_type": "panel base", "style_tags": ["scandinavian", "minimalist"], "image_url": "https://via.placeholder.com/300", "product_url": "https://wayfair.com"},
            {"name": "Modern Low Profile Bed", "width_inches": 62, "height_inches": 12, "depth_inches": 82, "price": 399, "base_type": "panel base", "style_tags": ["modern", "minimalist"], "image_url": "https://via.placeholder.com/300", "product_url": "https://wayfair.com"},
            {"name": "Classic 4-Post Bed", "width_inches": 64, "height_inches": 60, "depth_inches": 84, "price": 799, "base_type": "4 legs", "style_tags": ["traditional", "classic"], "image_url": "https://via.placeholder.com/300", "product_url": "https://wayfair.com"},
        ],
        "floor lamps": [
            {"name": "Slim Arc Floor Lamp", "width_inches": 10, "height_inches": 72, "depth_inches": 10, "price": 89, "base_type": "weighted base", "style_tags": ["scandinavian", "minimalist"], "image_url": "https://via.placeholder.com/300", "product_url": "https://wayfair.com"},
            {"name": "Tripod Floor Lamp", "width_inches": 18, "height_inches": 60, "depth_inches": 18, "price": 129, "base_type": "tripod", "style_tags": ["modern", "industrial"], "image_url": "https://via.placeholder.com/300", "product_url": "https://wayfair.com"},
        ],
        "dressers": [
            {"name": "6-Drawer Scandinavian Dresser", "width_inches": 36, "height_inches": 44, "depth_inches": 18, "price": 349, "base_type": "panel base", "style_tags": ["scandinavian", "minimalist"], "image_url": "https://via.placeholder.com/300", "product_url": "https://wayfair.com"},
            {"name": "Tall 8-Drawer Chest", "width_inches": 30, "height_inches": 58, "depth_inches": 16, "price": 299, "base_type": "4 legs", "style_tags": ["modern"], "image_url": "https://via.placeholder.com/300", "product_url": "https://wayfair.com"},
        ]
    }
    return mocks.get(category.lower(), [])

async def crawl_wayfair(category: str, max_width: float):
    """Real crawl — wire this up at the hackathon"""
    try:
        url = f"https://www.wayfair.com/keyword.php?keyword={category.replace(' ', '+')}"
        async with httpx.AsyncClient(headers=HEADERS, timeout=10) as client:
            response = await client.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            # Parse product cards here at the hackathon
            # For now fall through to mock
            return None
    except Exception:
        return None

@app.post("/tools/wayfair-search")
async def wayfair_search(request: SearchRequest):
    # Try real crawl first, fall back to mock
    real_results = await crawl_wayfair(request.category, request.max_width_inches)
    
    if real_results:
        products = real_results
    else:
        products = get_mock_products(request.category)

    # Filter by dimensions
    filtered = [
        p for p in products
        if p["width_inches"] <= request.max_width_inches
    ]

    return {
        "category": request.category,
        "products": filtered,
        "source": "live" if real_results else "mock"
    }