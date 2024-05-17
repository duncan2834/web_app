from .models import Category


def categories(request):
    return {
        'categories': Category.objects.filter(level=0)  # trả về dữ liệu của categories filter level=0
    }