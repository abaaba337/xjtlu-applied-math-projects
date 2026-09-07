import unittest
import numpy as np

from music_analysis import annealed_kmeans, pagerank, pca_features


class MusicRegression(unittest.TestCase):
    def test_pagerank_equation_with_dangling_column(self):
        weights = np.array([[0, 1, 0], [1, 0, 0], [1, 0, 0]])
        rank = pagerank(weights)
        transition = np.array([[0, 1, 1 / 3], [0.5, 0, 1 / 3], [0.5, 0, 1 / 3]])
        np.testing.assert_allclose(rank, 0.85 * transition @ rank + 0.15 / 3)
        self.assertAlmostEqual(rank.sum(), 1)
        self.assertTrue((rank > 0).all())
        with self.assertRaises(ValueError):
            pagerank([[0, -1], [1, 0]])

    def test_scaled_pca_and_best_candidate_are_reproducible(self):
        data = np.random.default_rng(2).normal(size=(40, 4)) * [1, 10, 100, 1000]
        scores, scaler, _ = pca_features(data, 3)
        np.testing.assert_allclose(scaler.transform(data).std(axis=0), 1)
        first, history = annealed_kmeans(scores, clusters=3, steps=4)
        second, again = annealed_kmeans(scores, clusters=3, steps=4)
        self.assertEqual(history, again)
        self.assertTrue(all(a >= b for a, b in zip(history, history[1:])))
        np.testing.assert_array_equal(first.labels_, second.labels_)
        actual = ((scores - first.cluster_centers_[first.labels_]) ** 2).sum()
        self.assertAlmostEqual(actual, history[-1])


if __name__ == "__main__":
    unittest.main()
