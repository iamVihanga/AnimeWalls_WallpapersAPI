from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import Scraper

app = FastAPI()
wallpapers_scraper = Scraper()

# Handelling CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def get_all():
    return wallpapers_scraper.scrape_items()

@app.get('/categories')
def get_categories():
    return wallpapers_scraper.all_categories()

@app.get('/categories/{category_name}')
def get_categories(category_name):
    return wallpapers_scraper.single_category(category_name)

@app.get('/wallpapers/{slug}')
def get_wallpapers(slug):
    return wallpapers_scraper.get_wallpapers(slug)