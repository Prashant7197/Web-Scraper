from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging

logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self, headless=True):
        self.driver = None
        self.headless = headless
        
    def setup_driver(self):
        """Set up Chrome WebDriver with options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
            
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        return self.driver
    
    def scrape_page(self, url, title_selector=None, content_selector=None):
        """
        Scrape a webpage and return title and content
        
        Args:
            url (str): URL to scrape
            title_selector (str): CSS selector for title (default: 'title')
            content_selector (str): CSS selector for content (default: 'body')
            
        Returns:
            dict: Dictionary containing 'url', 'title', and 'content'
        """
        if not self.driver:
            self.setup_driver()
            
        try:
            self.driver.get(url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extract title
            title = ""
            try:
                if title_selector:
                    title_element = self.driver.find_element(By.CSS_SELECTOR, title_selector)
                    title = title_element.text.strip()
                else:
                    title = self.driver.title
            except Exception as e:
                logger.warning(f"Could not extract title: {e}")
                title = self.driver.title
            
            # Extract content
            content = ""
            try:
                if content_selector:
                    content_element = self.driver.find_element(By.CSS_SELECTOR, content_selector)
                    content = content_element.text.strip()
                else:
                    content = self.driver.find_element(By.TAG_NAME, "body").text.strip()
            except Exception as e:
                logger.warning(f"Could not extract content: {e}")
                content = ""
            
            return {
                'url': url,
                'title': title,
                'content': content
            }
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return {
                'url': url,
                'title': "",
                'content': f"Error: {str(e)}"
            }
    
    def scrape_multiple_pages(self, urls, title_selector=None, content_selector=None, delay=1):
        """
        Scrape multiple pages
        
        Args:
            urls (list): List of URLs to scrape
            title_selector (str): CSS selector for title
            content_selector (str): CSS selector for content
            delay (int): Delay between requests in seconds
            
        Returns:
            list: List of scraped data dictionaries
        """
        results = []
        
        for url in urls:
            result = self.scrape_page(url, title_selector, content_selector)
            results.append(result)
            
            # Add delay between requests to be respectful
            if delay > 0:
                time.sleep(delay)
                
        return results
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def __enter__(self):
        """Context manager entry"""
        self.setup_driver()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
