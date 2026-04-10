import stripe

def getStripePrice(price_id):
    return stripe.Price.retrieve(price_id).unit_amount/100

def getProductPrice(product):
    price = None
    if product.stripe_price_id:
        try:
            price = getStripePrice(product.stripe_price_id)
        except stripe.error.StripeError:
            price = product.price
    else:
        price = product.price
    return price


def setServicePrices(service):
    service.prices = ', '.join(f'{product.size.capitalize()}: ${getProductPrice(product)}' for product in service.products.all())