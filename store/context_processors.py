from .models import Category, ProductType


def categories(request):
    return {
        'categories': Category.objects.filter(level=0)  # trả về dữ liệu của categories filter level=0
    }

def types(request):
    return {
        'types': ProductType.objects.all()  # trả về dữ liệu của categories filter level=0
    }