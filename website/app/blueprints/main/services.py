# Бизнес-логика (опционально)
from app.models import Category
from app.models import Product

# Функция для получения N продуктов для каждой категории
def get_products_per_category(n):
    categories = Category.query.join(Category.products).distinct().all()
    result = dict()
    
    for category in categories:
        cat_fields = {field.id: field.name for field in category.fields}

        if products := Product.query.filter_by(category_id=category.id).limit(n).all():

            result[category.name] = {
                'products' : [product for product in products],
                'image_path': category.image_path if category.image_path else None
            }

    return result


def get_product_by_name(name):
    if product := Product.query.filter_by(name=name).first():
        return product
    return None


def get_products_by_category(category, limit=16):
    if products := Product.query.filter_by(category_id=category.id).limit(limit).all():
        return products
    return None
