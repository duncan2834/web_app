from django.shortcuts import get_object_or_404, render
from .models import Category, Product
from .munge import Munger
from .recommender import recommend_products
from django.conf import settings

def product_all(request):
    products = Product.objects.prefetch_related("product_image").filter(is_active=True) # tối ưu hóa truy vấn và giảm số lượng truy vấn cơ sở dữ liệu khi lấy các hình ảnh sản phẩm liên quan.
    return render(request, "store/index.html", {"products": products})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True)  # Truy vấn tất cả các sản phẩm thuộc danh mục và các danh mục con của danh mục được chỉ định bởi slug.
    )
    return render(request, "store/category.html", {"category": category, "products": products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True) # lấy sản phẩm có slug = slug
    mung = Munger()
    similarity_matrix = mung.similarity_matrix
    df = mung.df
    recommended = recommend_products(product.cid, df, similarity_matrix)
    for cid in recommended:
        product_rec = get_object_or_404(Product, cid= cid, is_active=True) # lấy sản phẩm có cid = cid
        existing_value = recommended[cid]
        recommended[cid] = (existing_value, product_rec)
    return render(request, "store/single.html", {"product": product, "recommended": recommended, "MEDIA_URL": settings.MEDIA_URL})  # trả về thêm cả các sản phẩm gợi ý

def search_item(request):  # search sản phẩm theo từ chứa trong sp
    query = request.GET.get('q')
    products = Product.objects.filter(title__icontains = query)
    return render(request, "store/searchItem.html", {'products': products, 'query': query})
