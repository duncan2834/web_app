from django.test import TestCase
from django.contrib.auth.models import User
from store.models import Category, Product

class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name='duncan', slug='duncan')
        
    def test_category_model_entry(self):
        """
        kiểm tra liệu dữ liệu được thêm vào mô hình Category có đúng kiểu và các thuộc tính của nó có chính xác hay không
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))
        
    def test_category_model_entry(self):
        """
        test tên default của model Category 
        """
        data = self.data1
        self.assertEqual(str(data), 'duncan')
        
class TestProductModel(TestCase):
    def setUp(self):
        Category.objects.create(name='duncan', slug='duncan')
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=1, title='duncan-first',created_by_id=1,
                                            slug='duncan-first', price='20.00', image='duncan', color='red', size='22')
    
    def test_product_model_entry(self):
        """
        kiểm tra liệu dữ liệu được thêm vào mô hình Product có đúng kiểu và các thuộc tính của nó có chính xác hay không
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'duncan-first')   # so sánh với title vì models.py default là trả về self.title
        
        
        