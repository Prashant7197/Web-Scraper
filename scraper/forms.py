from django import forms

class ScrapeForm(forms.Form):
    url = forms.URLField(
        label='URL to Scrape',
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com',
            'required': True
        })
    )
    
    title_selector = forms.CharField(
        label='Title CSS Selector (Optional)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'h1, .title, #main-title',
            'help_text': 'Leave empty to use page title'
        })
    )
    
    content_selector = forms.CharField(
        label='Content CSS Selector (Optional)',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '.content, #main-content, article',
            'help_text': 'Leave empty to scrape entire body'
        })
    )
