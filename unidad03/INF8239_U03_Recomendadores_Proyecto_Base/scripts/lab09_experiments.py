from __future__ import annotations

import json
from time import perf_counter

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import root_mean_squared_error

from inf8239_u03.config import MOVIELENS_DIR, ROOT
from inf8239_u03.data import load_movielens
from inf8239_u03.metrics import catalog_coverage, hit_rate_at_k
from inf8239_u03.recommenders import MatrixFactorization, hybrid_top_n, popularity_fallback, temporal_leave_one_out

SEEDS = [42, 7, 2026]
FACTORS = [10, 20, 40]
ALPHAS = [0.0, 0.25, 0.5, 0.75, 1.0]
EPOCHS = 12

ratings, movies = load_movielens(MOVIELENS_DIR)
train, test = temporal_leave_one_out(ratings)
titles = movies.set_index("movieId")["title"]
movie_table = movies.reset_index(drop=True).copy()
movie_table["genres_text"] = movie_table["genres"].str.replace("|", " ", regex=False)
genre_matrix = TfidfVectorizer().fit_transform(movie_table["genres_text"])
movie_row = {int(movie_id): index for index, movie_id in enumerate(movie_table["movieId"])}
reports = ROOT / "reports"
reports.mkdir(exist_ok=True)

history_size = train.groupby("userId").size()
profiles = {"amplio": int(history_size.idxmax()), "pequeño": int(history_size.idxmin()), "nuevo": -1}

runs, lists = [], []
for seed in SEEDS:
    for factors in FACTORS:
        start = perf_counter()
        model = MatrixFactorization(factors=factors, seed=seed).fit(train, epochs=EPOCHS)
        train_seconds = perf_counter() - start
        evaluable = test[test["userId"].isin(model.user_index) & test["movieId"].isin(model.item_index)]
        rmse = root_mean_squared_error(evaluable["rating"], [model.predict(r.userId, r.movieId) for r in evaluable.itertuples()])
        for alpha in ALPHAS:
            start = perf_counter()
            recs = {
                int(user): hybrid_top_n(model, train, genre_matrix, movie_row, user, alpha)["movieId"].astype(int).tolist()
                for user in evaluable["userId"].unique()
            }
            runs.append({
                "seed": seed, "factors": factors, "alpha": alpha, "rmse": rmse,
                "hit_rate_at_10": hit_rate_at_k(recs, evaluable, 10),
                "catalog_coverage": catalog_coverage(recs, len(model.items)),
                "train_seconds": train_seconds, "recommend_seconds": perf_counter() - start,
                "model_kb": model.size_bytes() / 1024,
            })
            for profile, user in profiles.items():
                result = hybrid_top_n(model, train, genre_matrix, movie_row, user, alpha)
                for rank, row in enumerate(result.itertuples(), 1):
                    lists.append({
                        "seed": seed, "factors": factors, "alpha": alpha, "profile": profile, "userId": user,
                        "rank": rank, "movieId": int(row.movieId), "title": titles[row.movieId], "source": row.source,
                        "collaborative": getattr(row, "normalized", None), "content": getattr(row, "content_score", None),
                    })
            print(runs[-1])

popular = popularity_fallback(train, 10)["movieId"].astype(int).tolist()
evaluable = test[test["userId"].isin(train["userId"]) & test["movieId"].isin(train["movieId"])]
baseline = {
    "hit_rate_at_10": hit_rate_at_k({int(u): popular for u in evaluable["userId"]}, evaluable, 10),
    "catalog_coverage": catalog_coverage({0: popular}, train["movieId"].nunique()),
    "evaluable_users": int(len(evaluable)),
    "test_users": int(len(test)),
}
pd.DataFrame(runs).to_csv(reports / "lab09_runs.csv", index=False)
pd.DataFrame(lists).to_csv(reports / "lab09_profiles.csv", index=False)
(reports / "lab09_baseline.json").write_text(
    json.dumps({**baseline, "profiles": profiles, "history_size": {k: int(history_size.get(v, 0)) for k, v in profiles.items()}}, indent=2),
    encoding="utf-8",
)
print(baseline, profiles)
