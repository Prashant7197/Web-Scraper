from django.contrib import admin
from .models import ScrapedData

@admin.register(ScrapedData)
class ScrapedDataAdmin(admin.ModelAdmin):
    list_display = ['url', 'title', 'scraped_at']
    list_filter = ['scraped_at']
    search_fields = ['url', 'title', 'content']
    readonly_fields = ['scraped_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-scraped_at')
