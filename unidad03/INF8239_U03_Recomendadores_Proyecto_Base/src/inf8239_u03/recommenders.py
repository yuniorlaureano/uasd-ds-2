from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def weighted_popularity(ratings: pd.DataFrame, movies: pd.DataFrame, quantile: float = 0.80) -> pd.DataFrame:
    stats = ratings.groupby("movieId")["rating"].agg(["mean", "count"])
    global_mean = float(ratings["rating"].mean())
    minimum = float(stats["count"].quantile(quantile))
    stats["weighted_score"] = (
        stats["count"] / (stats["count"] + minimum) * stats["mean"]
        + minimum / (stats["count"] + minimum) * global_mean
    )
    return stats.query("count >= @minimum").join(movies.set_index("movieId")).sort_values("weighted_score", ascending=False)


class ContentRecommender:
    def fit(self, movies: pd.DataFrame) -> "ContentRecommender":
        self.movies = movies.reset_index(drop=True).copy()
        self.movies["genres_text"] = self.movies["genres"].str.replace("|", " ", regex=False)
        self.vectorizer = TfidfVectorizer()
        self.matrix = self.vectorizer.fit_transform(self.movies["genres_text"])
        return self

    def recommend(self, title: str, k: int = 10) -> pd.DataFrame:
        matches = self.movies.index[self.movies["title"].eq(title)]
        if len(matches) == 0:
            raise KeyError(f"Título no encontrado: {title}")
        index = int(matches[0])
        scores = cosine_similarity(self.matrix[index], self.matrix).ravel()
        order = [value for value in scores.argsort()[::-1] if value != index][:k]
        result = self.movies.loc[order, ["movieId", "title", "genres"]].copy()
        result["content_score"] = scores[order]
        return result.reset_index(drop=True)


class MatrixFactorization:
    def __init__(self, factors: int = 20, learning_rate: float = 0.01, regularization: float = 0.05, seed: int = 42):
        self.factors = factors
        self.learning_rate = learning_rate
        self.regularization = regularization
        self.seed = seed

    def fit(self, ratings: pd.DataFrame, epochs: int = 12) -> "MatrixFactorization":
        self.users = sorted(ratings["userId"].unique())
        self.items = sorted(ratings["movieId"].unique())
        self.user_index = {value: index for index, value in enumerate(self.users)}
        self.item_index = {value: index for index, value in enumerate(self.items)}
        rng = np.random.default_rng(self.seed)
        self.user_factors = rng.normal(0, 0.1, (len(self.users), self.factors))
        self.item_factors = rng.normal(0, 0.1, (len(self.items), self.factors))
        self.global_mean = float(ratings["rating"].mean())
        observations = [(self.user_index[r.userId], self.item_index[r.movieId], float(r.rating)) for r in ratings.itertuples()]
        for _ in range(epochs):
            rng.shuffle(observations)
            for user, item, rating in observations:
                error = rating - self.predict_indices(user, item)
                previous_user = self.user_factors[user].copy()
                self.user_factors[user] += self.learning_rate * (error * self.item_factors[item] - self.regularization * self.user_factors[user])
                self.item_factors[item] += self.learning_rate * (error * previous_user - self.regularization * self.item_factors[item])
        return self

    def predict_indices(self, user_index: int, item_index: int) -> float:
        return float(self.global_mean + self.user_factors[user_index] @ self.item_factors[item_index])

    def predict(self, user_id: int, movie_id: int) -> float:
        return self.predict_indices(self.user_index[user_id], self.item_index[movie_id])

    def top_n(self, user_id: int, seen: set[int], k: int = 10) -> pd.DataFrame:
        if user_id not in self.user_index:
            return pd.DataFrame(columns=["movieId", "collaborative_score"])
        candidates = [item for item in self.items if item not in seen]
        rows = [self.item_index[item] for item in candidates]
        scores = self.global_mean + self.item_factors[rows] @ self.user_factors[self.user_index[user_id]]
        order = scores.argsort()[::-1][:k]
        return pd.DataFrame({"movieId": np.asarray(candidates)[order], "collaborative_score": scores[order]})

    def size_bytes(self) -> int:
        return int(self.user_factors.nbytes + self.item_factors.nbytes)


def popularity_fallback(train: pd.DataFrame, k: int = 10) -> pd.DataFrame:
    popular = train.groupby("movieId")["rating"].agg(["mean", "count"]).sort_values(["count", "mean"], ascending=False)
    result = popular.head(k).reset_index()[["movieId"]]
    result["source"] = "popularidad (no personalizada)"
    return result


def _min_max(values: np.ndarray) -> np.ndarray:
    return (values - values.min()) / max(values.max() - values.min(), 1e-9)


def hybrid_top_n(
    model: MatrixFactorization,
    train: pd.DataFrame,
    genre_matrix,
    movie_row: dict[int, int],
    user_id: int,
    alpha: float = 0.75,
    k: int = 10,
    pool: int = 100,
) -> pd.DataFrame:
    if user_id not in model.user_index:
        return popularity_fallback(train, k)
    history = train.loc[train["userId"].eq(user_id) & train["movieId"].isin(movie_row), ["movieId", "rating"]]
    collaborative = model.top_n(user_id, set(history["movieId"]), pool)
    collaborative["normalized"] = _min_max(collaborative["collaborative_score"].to_numpy())
    history_rows = [movie_row[int(item)] for item in history["movieId"]]
    weights = np.clip(history["rating"].to_numpy() - 2.5, 0.1, None)
    profile = np.asarray(genre_matrix[history_rows].multiply(weights[:, None]).sum(axis=0) / weights.sum())
    candidate_rows = [movie_row[int(item)] for item in collaborative["movieId"]]
    collaborative["content_score"] = _min_max(cosine_similarity(profile, genre_matrix[candidate_rows]).ravel())
    collaborative["hybrid_score"] = alpha * collaborative["normalized"] + (1 - alpha) * collaborative["content_score"]
    result = collaborative.nlargest(k, "hybrid_score").reset_index(drop=True)
    result["source"] = "híbrido"
    return result


def temporal_leave_one_out(ratings: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    ordered = ratings.sort_values(["userId", "timestamp"])
    test = ordered.groupby("userId", sort=False).tail(1)
    train = ordered.drop(test.index)
    return train.reset_index(drop=True), test.reset_index(drop=True)
