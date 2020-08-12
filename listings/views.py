from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from .choices import bedroom_choices, price_choices, state_choices
from .models import Listing


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context = {
        'listings': paged_listings,

    }
    return render(request, 'listings/listings.html', context=context)


def listing(request, listing_id):
    listing_ = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing_
    }
    return render(request, 'listings/listing.html', context=context)


def search(request):
    queryset = Listing.objects.order_by('-list_date')
    if 'keywords' in request.GET:
        keywords = request.GET.get('keywords')
        if keywords:
            queryset = queryset.filter(description__icontains=keywords)

    if 'city' in request.GET:
        city = request.GET.get('city')
        if city:
            queryset = queryset.filter(city__iexact=city)
    if 'price' in request.GET:
        price = request.GET.get('price')
        if price:
            queryset = queryset.filter(price__lte=price)
    if 'bedrooms' in request.GET:
        bedrooms = request.GET.get('bedrooms')
        if bedrooms:
            queryset = queryset.filter(bedrooms__lte=bedrooms)

    if 'state' in request.GET:
        state = request.GET.get('state')
        if state:
            queryset = queryset.filter(state__iexact=state)

    context = {
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'state_choices': state_choices,
        'listings': queryset,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context=context)
