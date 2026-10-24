import pytest
from sklearn.feature_extraction.text import TfidfVectorizer

from inf8239_u03.recommenders import MatrixFactorization, hybrid_top_n


@pytest.fixture
def setup(sample_ratings, sample_movies):
    model = MatrixFactorization(factors=3, seed=42).fit(sample_ratings, epochs=5)
    matrix = TfidfVectorizer().fit_transform(sample_movies["genres"].str.replace("|", " ", regex=False))
    movie_row = {int(movie_id): index for index, movie_id in enumerate(sample_movies["movieId"])}
    return model, sample_ratings, matrix, movie_row


def test_hybrid_excludes_seen_items(setup):
    model, ratings, matrix, movie_row = setup
    result = hybrid_top_n(model, ratings, matrix, movie_row, user_id=1, k=5)
    assert not set(result["movieId"]) & set(ratings.loc[ratings["userId"].eq(1), "movieId"])
    assert result["movieId"].is_unique


def test_alpha_one_follows_collaborative_order(setup):
    model, ratings, matrix, movie_row = setup
    result = hybrid_top_n(model, ratings, matrix, movie_row, user_id=1, alpha=1.0, k=5)
    assert result["collaborative_score"].is_monotonic_decreasing


def test_cold_user_gets_declared_fallback(setup):
    model, ratings, matrix, movie_row = setup
    result = hybrid_top_n(model, ratings, matrix, movie_row, user_id=999, k=3)
    assert len(result) == 3
    assert (result["source"] == "popularidad (no personalizada)").all()
