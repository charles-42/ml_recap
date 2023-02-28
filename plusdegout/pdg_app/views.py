import json

import requests
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .forms import SearchForm

from .utils import get_spotify_token, get_prediction

# This variable maps a search type to the name of the key containing search
# results. It's immutable because it should change - the Spotify API _should_
# be stable.
RESULT_KEY_MAP = (
    ('artist', 'artists',),
    ('album', 'albums',),
    ('playlist', 'playlists',),
    ('track', 'tracks',),
)


def search_index(request):
    results = None
    result_count = None

    # We will lose the POST data every time we use pagination
    # One way of keeping this data is to add it to a session
    # Make sure we only add this data when we're actually using pagination
    # ('page' in request.GET)

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            search_type = form.cleaned_data['search_type']
            search_string = form.cleaned_data['search_string']
        token = get_spotify_token()
        results = get_prediction(token)
            
    else:
        form = SearchForm()

    print(results)

    context = {
        'results': results,
        'form': form,
    }
    return render(request, 'search.html', context)