from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from .models import ScrapedData
from .scraper import WebScraper
from .forms import ScrapeForm
import logging

logger = logging.getLogger(__name__)

def index(request):
    """Display scraped data and scraping form"""
    scraped_data = ScrapedData.objects.all()
    paginator = Paginator(scraped_data, 10)  # Show 10 items per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    form = ScrapeForm()
    
    context = {
        'page_obj': page_obj,
        'form': form,
    }
    
    return render(request, 'scraper/index.html', context)

def scrape_url(request):
    """Handle URL scraping requests"""
    if request.method == 'POST':
        form = ScrapeForm(request.POST)
        
        if form.is_valid():
            url = form.cleaned_data['url']
            title_selector = form.cleaned_data.get('title_selector')
            content_selector = form.cleaned_data.get('content_selector')
            
            try:
                with WebScraper(headless=True) as scraper:
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
                    
                    messages.success(request, f'Successfully scraped: {url}')
                    
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': True,
                            'message': f'Successfully scraped: {url}',
                            'data': {
                                'id': scraped_data.id,
                                'url': scraped_data.url,
                                'title': scraped_data.title,
                                'content': scraped_data.content[:200] + '...' if len(scraped_data.content) > 200 else scraped_data.content,
                                'scraped_at': scraped_data.scraped_at.strftime('%Y-%m-%d %H:%M:%S')
                            }
                        })
                    
            except Exception as e:
                error_msg = f'Error scraping {url}: {str(e)}'
                logger.error(error_msg)
                messages.error(request, error_msg)
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': error_msg
                    })
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid form data'
                })
    
    return redirect('scraper:index')

def delete_scraped_data(request, pk):
    """Delete scraped data"""
    if request.method == 'POST':
        try:
            scraped_data = ScrapedData.objects.get(pk=pk)
            scraped_data.delete()
            messages.success(request, 'Data deleted successfully')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
                
        except ScrapedData.DoesNotExist:
            messages.error(request, 'Data not found')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Data not found'})
    
    return redirect('scraper:index')
