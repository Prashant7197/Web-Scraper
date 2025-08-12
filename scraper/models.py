from django.db import models

class ScrapedData(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    scraped_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-scraped_at']
    
    def __str__(self):
        return f"{self.title or 'No Title'} - {self.url}"
