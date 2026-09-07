"""Runnable PageRank, PCA and annealed clustering reconstruction; see README.md."""
import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def pagerank(weights, damping=0.85):
    """weights[target, source]; distribute empty source columns uniformly."""
    weights = np.asarray(weights, dtype=float)
    if weights.ndim != 2 or weights.shape[0] != weights.shape[1] or not len(weights):
        raise ValueError("Require a nonempty square influence matrix.")
    if not np.isfinite(weights).all() or (weights < 0).any() or not 0 <= damping < 1:
        raise ValueError("Require finite nonnegative weights and 0 <= damping < 1.")
    n = len(weights)
    sums = weights.sum(axis=0)
    transition = np.divide(weights, sums, out=np.full_like(weights, 1 / n), where=sums != 0)
    return np.linalg.solve(np.eye(n) - damping * transition, np.full(n, (1 - damping) / n))


def pca_features(features, components=7):
    """Standardize numeric audio features before fitting PCA; exclude IDs/year."""
    scaler = StandardScaler()
    standardized = scaler.fit_transform(features)
    pca = PCA(n_components=components)
    return pca.fit_transform(standardized), scaler, pca


def annealed_kmeans(features, clusters=5, steps=20, temperature=1.0, cooling=0.7, seed=0):
    """Perturb centers, refit KMeans, and retain the best evaluated candidate."""
    if steps < 0 or not np.isfinite(temperature) or temperature <= 0 or not 0 < cooling < 1:
        raise ValueError("Require steps >= 0, positive finite temperature and 0 < cooling < 1.")
    features = np.asarray(features, dtype=float)
    rng = np.random.default_rng(seed)
    current = KMeans(n_clusters=clusters, n_init=10, random_state=seed).fit(features)
    best = current
    history = [float(best.inertia_)]
    scale = features.std(axis=0)
    for _ in range(steps):
        centers = current.cluster_centers_ + rng.normal(size=current.cluster_centers_.shape) * scale * 0.1
        candidate = KMeans(n_clusters=clusters, init=centers, n_init=1, random_state=seed).fit(features)
        delta = candidate.inertia_ - current.inertia_
        if delta <= 0 or (temperature > 0 and rng.random() < np.exp(-delta / temperature)):
            current = candidate
        if candidate.inertia_ < best.inertia_:
            best = candidate
        history.append(float(best.inertia_))
        temperature *= cooling
    return best, history


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--demo", action="store_true", help="Use synthetic data; no historical results.")
    source.add_argument("--features", type=Path, help="Numeric CSV with one header row; audio features only.")
    parser.add_argument("--components", type=int, default=7)
    parser.add_argument("--clusters", type=int, default=5)
    parser.add_argument("--steps", type=int, default=20)
    args = parser.parse_args()
    features = (np.random.default_rng(0).normal(size=(100, 14)) if args.demo else
                np.loadtxt(args.features, delimiter=",", skiprows=1, ndmin=2))
    scores, _, pca = pca_features(features, args.components)
    model, history = annealed_kmeans(scores, args.clusters, args.steps)
    result = {"synthetic": args.demo, "observations": len(features),
              "explained_variance": pca.explained_variance_ratio_.tolist(),
              "best_inertia": history, "cluster_sizes": np.bincount(model.labels_).tolist()}
    if args.demo:
        result["synthetic_pagerank"] = pagerank([[0, 1, 0], [1, 0, 0], [1, 0, 0]]).tolist()
    print(json.dumps(result, indent=2))
