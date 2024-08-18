from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import logging
from news.models import CrawlHackerNews

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Scrape Hacker News RSS feed and store news items in the database'

    def handle(self, *args, **kwargs):
        url = 'https://news.ycombinator.com/rss'

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request to {url} failed: {e}")
            self.stdout.write(self.style.ERROR(f"Request to {url} failed: {e}"))
            return

        soup = BeautifulSoup(response.content, 'xml')  # Use 'xml' parser for RSS feeds
        items = soup.find_all('item')

        for item in items:
            title = item.title.text
            link = item.link.text
            print(link)
            print(title)
            # Extract additional data if needed
            # For example, you can parse 'pubDate', 'description', etc. from RSS feed

            logger.info(f"Scraped item: title={title}, link={link}")

            # Check if the news item already exists in the database based on title or link
            news_obj, created = CrawlHackerNews.objects.get_or_create(
                title=title,
                defaults={'link': link}
           )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created "{title}"'))
            else:
                # Update the link if the news item already exists
                news_obj.link = link
                news_obj.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully updated "{title}"'))

        count = CrawlHackerNews.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Total items in database: {count}'))
