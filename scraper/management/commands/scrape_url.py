"""
Simple Django Web Scraper Management Commands

This module provides Django management commands for web scraping operations.
"""

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from scraper.models import ScrapedData
from scraper.scraper import WebScraper
import sys


class Command(BaseCommand):
    help = 'Scrape a URL and save to database'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL to scrape')
        parser.add_argument(
            '--title-selector',
            type=str,
            help='CSS selector for title (optional)'
        )
        parser.add_argument(
            '--content-selector',
            type=str,
            help='CSS selector for content (optional)'
        )
        parser.add_argument(
            '--headless',
            action='store_true',
            default=True,
            help='Run browser in headless mode (default: True)'
        )

    def handle(self, *args, **options):
        url = options['url']
        title_selector = options.get('title_selector')
        content_selector = options.get('content_selector')
        headless = options.get('headless', True)

        self.stdout.write(f'Scraping URL: {url}')
        
        try:
            with WebScraper(headless=headless) as scraper:
                result = scraper.scrape_page(
                    url=url,
                    title_selector=title_selector,
                    content_selector=content_selector
                )
                
                # Save to database
                scraped_data = ScrapedData.objects.create(
                    url=result['url'],
                    title=result['title'],
                    content=result['content']
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully scraped and saved: {scraped_data.title or "No Title"}'
                    )
                )
                
        except Exception as e:
            raise CommandError(f'Error scraping {url}: {str(e)}')
