from requests_html import HTMLSession

class Scraper():
    def __init__(self):
        self.url = 'https://wallpapercave.com/categories/anime'
        self.baseURL = 'https://wallpapercave.com/'

        # Session
        self.s = HTMLSession()

        # Category Lists
        self.popular_list = []
        self.characters_list = []
        self.manga_anime_list = []


    def all_categories(self):
        all_items_list = self.scrape_items()

        category_list = [
            {'name' : 'popular', 'sub_categories': len(all_items_list[0]['popular'])},
            {'name' : 'characters', 'sub_categories': len(all_items_list[0]['characters'])},
            {'name' : 'manga_anime', 'sub_categories': len(all_items_list[0]['manga_anime'])}
        ]
        return category_list


    def single_category(self, single_category):
        all_items_list = self.scrape_items()
        try:
            return all_items_list[0][single_category]
        except:
            return { 'message': 'Error, invalid category name' }


    def scrape_items(self):
        r = self.s.get(self.url)

        all_items = r.html.find('a.albumthumbnail')
        # Organize category lists with items
        popular_items = all_items[0:12]
        characters_items = all_items[12:73]
        manga_anime_items = all_items[73:]

        # Create Popular List
        for item in popular_items:
            thumbnail = item.find('img.thumbnail', first=True).attrs['src']
            title = item.find('p.title', first=True).text.strip()
            wallpaper_count = item.find('p.number', first=True).text.strip()
            slug = item.find('div.albumphoto', first=True).attrs['href'][1:]
            
            self.popular_list.append({
                'thumbnail': thumbnail,
                'title': title,
                'wallpaper_count': wallpaper_count,
                'slug': slug,
                'category': 'popular'
            })

        # Create characters list
        for item in characters_items:
            thumbnail = item.find('img.thumbnail', first=True).attrs['src']
            title = item.find('p.title', first=True).text.strip()
            wallpaper_count = item.find('p.number', first=True).text.strip()
            slug = item.find('div.albumphoto', first=True).attrs['href'][1:]
            
            self.characters_list.append({
                'thumbnail': thumbnail,
                'title': title,
                'wallpaper_count': wallpaper_count,
                'slug': slug,
                'category': 'characters'
            })

        # Create manga_anime list
        for item in manga_anime_items:
            thumbnail = item.find('img.thumbnail', first=True).attrs['src']
            title = item.find('p.title', first=True).text.strip()
            wallpaper_count = item.find('p.number', first=True).text.strip()
            slug = item.find('div.albumphoto', first=True).attrs['href'][1:]
            
            self.manga_anime_list.append({
                'thumbnail': thumbnail,
                'title': title,
                'wallpaper_count': wallpaper_count,
                'slug': slug,
                'category': 'manga_anime'
            })

        return [{
            'popular': self.popular_list,
            'characters' : self.characters_list,
            'manga_anime': self.manga_anime_list
        }]
        

    def get_wallpapers(self, slug):
        r = self.s.get(f'{self.baseURL}{slug}')

        # Scrape wallpapers
        wallpapers_list = []
        all_elems = r.html.find('img.wimg')
        for wallpaper in all_elems:
            link = self.baseURL + wallpaper.attrs['src'][1:]
            wallpapers_list.append(link)
        
        return wallpapers_list
        
