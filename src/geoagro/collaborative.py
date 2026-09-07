from __future__ import annotations

from dataclasses import dataclass

from .data import Review, normalize_text


@dataclass(frozen=True)
class ProductRecommendation:
    product: str
    rating: int
    source_user: str
    comment: str


def recommend_from_similar_users(
    user: str,
    reviews: tuple[Review, ...] | list[Review],
    *,
    limit: int = 10,
) -> list[ProductRecommendation]:
    """Suggest unseen products reviewed by users sharing at least one product."""
    user_key = normalize_text(user)
    own = [review for review in reviews if normalize_text(review.user) == user_key]
    if not own:
        return []
    own_products = {normalize_text(review.product) for review in own}
    similar_users = {
        normalize_text(review.user)
        for review in reviews
        if normalize_text(review.user) != user_key
        and normalize_text(review.product) in own_products
    }

    candidates: dict[str, ProductRecommendation] = {}
    for review in reviews:
        product_key = normalize_text(review.product)
        if normalize_text(review.user) not in similar_users or product_key in own_products:
            continue
        candidate = ProductRecommendation(
            review.product, review.rating, review.user, review.comment
        )
        previous = candidates.get(product_key)
        if previous is None or (candidate.rating, candidate.product) > (
            previous.rating,
            previous.product,
        ):
            candidates[product_key] = candidate

    return sorted(
        candidates.values(),
        key=lambda item: (-item.rating, item.product.casefold(), item.source_user.casefold()),
    )[:limit]
