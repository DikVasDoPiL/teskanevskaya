# Бизнес-логика (опционально)
from app.models import Category
from app.models import Product

# Функция для получения N продуктов для каждой категории
def get_products_per_category(n):
    categories = Category.query.filter_by(active=True).all()
    result = dict()
    # print(categories)
    
    for category in categories:
        print(category)
        if products := Product.query.filter_by(category_id=category.id).limit(n).all():
            print(products)
            result[category.name] = {
                'products' : [product for product in products],
                'image_path': category.image_path if category.image_path else None
            }

    
    return result