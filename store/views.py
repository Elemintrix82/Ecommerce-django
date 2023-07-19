from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from django.db.models import Q
from orders.models import OrderProduct
from store.forms import ReviewForm

from store.models import Boutique, Product, ProductGallery, ReviewRating
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib import messages

from django.utils.translation import gettext_lazy as _ 

from django.utils.translation import activate
# from googletrans import Translator

# Create your views here.

def store(request, category_slug=None):
    categories = None
    products = None
    
    if  category_slug is not None :
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        slug=category_slug
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    
    return render(request, 'store/store.html', context)

"""
def store(request, category_slug=None):
    categories = None
    products = None
    
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
    
    # Traduire les noms des produits en fonction de la langue courante
    current_language = request.LANGUAGE_CODE
    translator = Translator()
    translated_products = []
    for product in products:
        if translator.detect(product.product_name).lang != current_language:
            translated_name = translator.translate(product.product_name, dest=current_language).text
            translated_products.append((product, translated_name))
        else:
            translated_products.append((product, product.product_name))
    
    paginator = Paginator(translated_products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()
    
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    
    return render(request, 'store/store.html', context)

"""

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    except Exception as e:
        raise e
    
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
        
    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    
    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    
   # Récupérer la boutique liée au produit
    boutique = single_product.boutiques.first()  # Récupère la première boutique liée au produit
    
    if single_product.variation_set.colors().exists():
        print(single_product.variation_set.colors())
    else:
        print(single_product.variation_set.colors())

    current_language = request.LANGUAGE_CODE
    activate(current_language)
    
    # translator = Translator()
    
    # if translator and translator.detect(single_product.description).lang != current_language:
    #     translated_description = translator.translate(single_product.description, dest=current_language).text
    # else:
    #     translated_description = single_product.description
        
    # if translator and translator.detect(single_product.product_name).lang != current_language:
    #     translated_name = translator.translate(single_product.product_name, dest=current_language).text
    # else:
    #     translated_name = single_product.product_name
    
    translated_description = single_product.description
    translated_name = single_product.product_name
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
        'boutique': boutique,
        'translated_description':translated_description,
        'translated_name': translated_name,
    }
    
    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
        else:
            products = ""
            product_count = 0

    context = {
        'products' : products,
        'product_count' : product_count,
    }
    
    return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, _('Thank you! Your review has been updates.'))
            return redirect(url)
        
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, _('Thank you! Your review has been submitted.'))
                return redirect(url)
                