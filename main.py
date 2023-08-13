import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from transformers import pipeline
import time
from datetime import datetime, timedelta


class SearchEngine:
    def __init__(self):
        self.url = "https://www.google.com/search?q="

    def send_query(self, query):
        search_results = []
        search_url = self.url + query

        response = requests.get(search_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a'):
                url = link.get('href')
                search_results.append(url)

        return search_results


class WebScraper:
    def __init__(self):
        self.translator = Translator()
        self.summarizer = pipeline("summarization")

    def scrape_content(self, url):
        try:
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string
                paragraphs = [p.get_text() for p in soup.find_all('p')]
                images = [img['src'] for img in soup.find_all('img')]
                metadata = soup.find('meta')

                summaries = self.summarizer(paragraphs, max_length=50, min_length=10, num_beams=4, do_sample=False)
                summaries = [summary['summary_text'] for summary in summaries]

                return {
                    'title': title,
                    'paragraphs': paragraphs,
                    'images': images,
                    'metadata': metadata,
                    'summaries': summaries
                }
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Failed to scrape content from {url}: {str(e)}")
            return None

    def translate_content(self, content, target_lang):
        translations = {}
        if target_lang != 'en':
            for key, value in content.items():
                if isinstance(value, str):
                    translations[key] = self.translator.translate(value, dest=target_lang).text
                elif isinstance(value, list):
                    translations[key] = [self.translator.translate(text, dest=target_lang).text for text in value]
                else:
                    translations[key] = value
        else:
            translations = content

        return translations


class ContentAggregator:
    def __init__(self):
        self.content = []

    def aggregate_content(self, scraped_content):
        self.content.append(scraped_content)

    def generate_summary(self):
        summary = ''
        for c in self.content:
            for p in c['paragraphs']:
                summary += p + '\n'

        return summary


class AutonomyPlatform:
    def __init__(self):
        self.search_engine = SearchEngine()
        self.web_scraper = WebScraper()
        self.content_aggregator = ContentAggregator()
        self.languages = ['en', 'es', 'de', 'fr']

    def process_search_query(self, query):
        search_results = self.search_engine.send_query(query)

        for result in search_results:
            if result.startswith('http'):
                scraped_content = self.web_scraper.scrape_content(result)

                if scraped_content:
                    self.content_aggregator.aggregate_content(scraped_content)

        summary = self.content_aggregator.generate_summary()
        return summary

    def translate_content(self, content, target_lang):
        if target_lang in self.languages:
            translated_content = self.web_scraper.translate_content(content, target_lang)
            return translated_content
        else:
            return content

    def execute_program(self):
        while True:
            query = input("Enter your search query: ")
            target_lang = input("Enter target language (en, es, de, fr): ")

            summary = self.process_search_query(query)

            translated_summary = self.translate_content(summary, target_lang)

            print(translated_summary)

            time.sleep(2)
            print("Profit generated!")

            schedule_option = input("Do you want to schedule regular content updates? (y/n): ")

            if schedule_option.lower() == 'y':
                update_frequency = input("Enter update frequency (daily, weekly, etc.): ")
                self.schedule_content_updates(query, target_lang, update_frequency)

    def schedule_content_updates(self, query, target_lang, update_frequency):
        while True:
            current_time = datetime.now()
            next_update_time = current_time + timedelta(days=1) if update_frequency.lower() == 'daily' else current_time + timedelta(weeks=1)

            if next_update_time.hour == 0 and next_update_time.minute == 0:
                summary = self.process_search_query(query)
                translated_summary = self.translate_content(summary, target_lang)
                print(translated_summary)
                time.sleep(2)
                print("Profit generated!")

            time.sleep((next_update_time - datetime.now()).total_seconds())


if __name__ == "__main__":
    platform = AutonomyPlatform()
    platform.execute_program()