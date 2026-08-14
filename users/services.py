import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name: str) -> str:
    """Создает продукт в Stripe и возвращает его ID."""
    product = stripe.Product.create(name=name)
    return product.id


def create_stripe_price(product_id: str, amount: int, currency: str = "usd") -> str:
    """Создает цену для продукта в Stripe.

    amount передается в основных единицах (например, 100$),
    в Stripe конвертируется в центы/копейки (100 * 100 = 10000).
    """
    price = stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),
        currency=currency,
    )
    return price.id


def create_stripe_session(price_id: str, success_url: str = "http://127.0.0.1:8000/") -> tuple[str, str]:
    """Создает сессию оплаты Checkout в Stripe.

    Возвращает кортеж (session_id, payment_url).
    """
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
    )
    return session.id, session.url


def retrieve_stripe_session(session_id: str):
    """(Опционально) Получение данных о статусе сессии оплаты."""
    return stripe.checkout.Session.retrieve(session_id)
