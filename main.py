from tokopedia_scraper import TokopediaScraper

if __name__ == "__main__":
    keywords = input('Masukan kata kunci: ')
    pages = int(input('Berapa page yang ingin discrap: '))
    scraper = TokopediaScraper()
    scraper.run(keywords, pages)