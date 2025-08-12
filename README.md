# Django Web Scraper with Selenium

This Django project includes a web scraping application using Selenium WebDriver. You can scrape websites through a web interface or command line.

## Features

- **Web Interface**: User-friendly interface to scrape URLs with custom CSS selectors
- **Data Management**: View, search, and delete scraped data
- **Admin Interface**: Django admin panel for managing scraped data
- **Command Line**: Management command for programmatic scraping
- **Responsive Design**: Bootstrap-based responsive UI

## Installation

The project is already set up with all dependencies installed:

- Django 5.2.5
- Selenium 4.34.2
- WebDriver Manager 4.0.2

## Usage

### 1. Start the Development Server

```bash
D:/downloadmy/scrapy/.venv/Scripts/python.exe manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the web scraper interface.

### 2. Web Interface

- Enter a URL to scrape
- Optionally specify CSS selectors for title and content
- View all scraped data in a paginated table
- Delete unwanted entries
- View full content in a modal

### 3. Command Line Usage

Scrape a URL from the command line:

```bash
D:/downloadmy/scrapy/.venv/Scripts/python.exe manage.py scrape_url https://example.com
```

With custom selectors:

```bash
D:/downloadmy/scrapy/.venv/Scripts/python.exe manage.py scrape_url https://example.com --title-selector "h1" --content-selector ".content"
```

### 4. Admin Interface

Create a superuser to access the admin panel:

```bash
D:/downloadmy/scrapy/.venv/Scripts/python.exe manage.py createsuperuser
```

Then visit `http://127.0.0.1:8000/admin/` to manage scraped data.

## Project Structure

```
scrapy/
├── manage.py
├── mysite/                    # Django project settings
├── scraper/                   # Web scraper app
│   ├── models.py             # ScrapedData model
│   ├── views.py              # Web interface views
│   ├── forms.py              # Web forms
│   ├── scraper.py            # Selenium scraper class
│   ├── admin.py              # Admin interface
│   ├── urls.py               # URL routing
│   ├── templates/            # HTML templates
│   └── management/           # Management commands
└── .venv/                    # Virtual environment
```

## WebScraper Class

The `WebScraper` class provides:

- Headless Chrome browser automation
- Custom CSS selector support
- Error handling and logging
- Context manager support
- Respectful scraping with delays

## Example Usage in Code

```python
from scraper.scraper import WebScraper

# Scrape a single page
with WebScraper() as scraper:
    result = scraper.scrape_page('https://example.com')
    print(result['title'])
    print(result['content'][:100])

# Scrape multiple pages
urls = ['https://example.com', 'https://another-site.com']
with WebScraper() as scraper:
    results = scraper.scrape_multiple_pages(urls, delay=2)
```

## Notes

- Chrome WebDriver is automatically managed by webdriver-manager
- The scraper runs in headless mode by default for better performance
- Always be respectful when scraping websites and follow robots.txt
- Consider adding user-agent rotation and rate limiting for production use
