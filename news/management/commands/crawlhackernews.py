from django.core.management.base import BaseCommand
import requests
import logging
from news.models import CrawlHackerNews

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch Hacker News top stories along with their authors, points, and comments and store them in the database'

    def handle(self, *args, **kwargs):
        top_stories_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
        story_detail_url = 'https://hacker-news.firebaseio.com/v0/item/{}.json'

        try:
            response = requests.get(top_stories_url)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Request to {top_stories_url} failed: {e}")
            self.stdout.write(self.style.ERROR(f"Request to {top_stories_url} failed: {e}"))
            return

        story_ids = response.json()
        for story_id in story_ids[:40]:  # limiting to top 10 stories for brevity
            try:
                story_response = requests.get(story_detail_url.format(story_id))
                story_response.raise_for_status()
            except requests.RequestException as e:
                logger.error(f"Request to {story_detail_url.format(story_id)} failed: {e}")
                continue

            story_data = story_response.json()
            title = story_data.get('title')
            link = f"https://news.ycombinator.com/item?id={story_id}"
            author = story_data.get('by')
            points = story_data.get('score', 0)
            comments = story_data.get('descendants', 0)

            logger.info(f"Fetched story: title={title}, link={link}, author={author}, points={points}, comments={comments}")

            # Check if the news item already exists in the database based on title or link
            news_obj, created = CrawlHackerNews.objects.get_or_create(
                title=title,
                defaults={'link': link, 'author': author, 'points': points, 'comments': comments}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created "{title}"'))
            else:
                # Update the link, author, points, and comments if the news item already exists
                news_obj.link = link
                news_obj.author = author
                news_obj.points = points
                news_obj.comments = comments
                news_obj.save()
                print(news_obj)
                self.stdout.write(self.style.SUCCESS(f'Successfully updated "{title}"'))

        count = CrawlHackerNews.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Total items in database: {count}'))
