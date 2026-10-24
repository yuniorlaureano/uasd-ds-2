from __future__ import annotations

import argparse
import json
from time import perf_counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import root_mean_squared_error

from inf8239_u03.config import MOVIELENS_DIR, RANDOM_STATE, ROOT
from inf8239_u03.data import load_movielens
from inf8239_u03.metrics import catalog_coverage, hit_rate_at_k
from inf8239_u03.recommenders import MatrixFactorization, hybrid_top_n, popularity_fallback, temporal_leave_one_out

parser = argparse.ArgumentParser()
parser.add_argument("--factors", type=int, default=20)
parser.add_argument("--epochs", type=int, default=12)
parser.add_argument("--alpha", type=float, default=0.75)
parser.add_argument("--seed", type=int, default=RANDOM_STATE)
args = parser.parse_args()

ratings, movies = load_movielens(MOVIELENS_DIR)
train, test = temporal_leave_one_out(ratings)
start = perf_counter()
model = MatrixFactorization(factors=args.factors, seed=args.seed).fit(train, epochs=args.epochs)
train_seconds = perf_counter() - start
evaluable = test[test["userId"].isin(model.user_index) & test["movieId"].isin(model.item_index)]
predictions = [model.predict(row.userId, row.movieId) for row in evaluable.itertuples()]
rmse = root_mean_squared_error(evaluable["rating"], predictions)
movie_table = movies.reset_index(drop=True).copy()
movie_table["genres_text"] = movie_table["genres"].str.replace("|", " ", regex=False)
genre_matrix = TfidfVectorizer().fit_transform(movie_table["genres_text"])
movie_row = {int(movie_id): index for index, movie_id in enumerate(movie_table["movieId"])}
recommendations = {
    int(user_id): hybrid_top_n(model, train, genre_matrix, movie_row, user_id, args.alpha)["movieId"].astype(int).tolist()
    for user_id in evaluable["userId"].unique()
}
metrics = {
    "rmse": float(rmse),
    "hit_rate_at_10": hit_rate_at_k(recommendations, evaluable, 10),
    "catalog_coverage": catalog_coverage(recommendations, len(model.items)),
    "train_seconds": train_seconds,
    "model_kb": model.size_bytes() / 1024,
    "factors": args.factors,
    "epochs": args.epochs,
    "alpha": args.alpha,
    "seed": args.seed,
    "cold_start_policy": "popularidad por cantidad y media; no personalizada",
}
(ROOT / "reports").mkdir(exist_ok=True)
(ROOT / "reports/hybrid_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
cold_start_items = popularity_fallback(train, 10)["movieId"].tolist()
movies[movies["movieId"].isin(cold_start_items)].set_index("movieId").loc[cold_start_items].reset_index().to_csv(
    ROOT / "reports/cold_start_fallback.csv", index=False
)
print(json.dumps(metrics, indent=2))
