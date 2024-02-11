from django.shortcuts import get_object_or_404, render
from .models import Listing
from .choices import prices_choices , bedroom_choices , state_choices
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings,6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context ={
        'listings': paged_listings
    }
    return render(request,'listings/listings.html',context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }


    return render(request,'listings/listing.html',context)

def search(request):
    querysetlist = Listing.objects.order_by('-list_date')
    #keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            querysetlist = querysetlist.filter(description__icontains=keywords  )

    if 'city' in request.GET:
        keywords = request.GET['city']
        if keywords:
            querysetlist = querysetlist.filter(city__exact=keywords  )

    if 'state' in request.GET:
        keywords = request.GET['state']
        if keywords:
            querysetlist = querysetlist.filter(state__iexact=keywords ) 

    if 'bedrooms' in request.GET:
        keywords = request.GET['bedrooms']
        if keywords:
            querysetlist = querysetlist.filter(bedrooms__lte=keywords ) 

    if 'price' in request.GET:
        keywords = request.GET['price']
        if keywords:
            querysetlist = querysetlist.filter(price__lte=keywords )

    context = {
        
        'state_choices': state_choices,
        'prices_choices': prices_choices,
        'bedroom_choices': bedroom_choices,
        'listings': querysetlist,
        'values': request.GET,
    }


    return render(request,'listings/search.html',context)