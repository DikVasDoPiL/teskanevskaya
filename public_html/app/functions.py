from .models import User, Category, Promotion, Product

# Функция для получения N продуктов для каждой категории
def get_products_per_category(n):
    categories = Category.query.filter_by(active=True).all()
    result = dict()
    # print(categories)
    
    for category in categories:
        print(category)
        if products := Product.query.filter_by(category_id=category.id).limit(n).all():
            print(products)
            result[category.name] = [product for product in products]
    
    return result