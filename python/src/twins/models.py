import numpy as np
import tensorflow as tf
import sklearn.decomposition as decomp
import matplotlib.pyplot as plt


class BagOfPCA:
    """PCA-Bag of Words"""

    def __init__(self, vocab_size: int = 500, rank: int = 32):
        self.rank = rank
        self.vocab_size = vocab_size
        self._fit = False

    def _tokenize(self, X: np.array) -> np.array:
        return self._tokenizer.sequences_to_matrix(self._tokenizer.texts_to_sequences(X), mode="tfidf")

    def _fit_tokenizer(self, X: np.array) -> np.array:
        self._tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=self.vocab_size)
        self._tokenizer.fit_on_texts(X)

    def fit_transform(self, X: np.array) -> np.array:
        self._fit_tokenizer(X)
        feats = self._tokenize(X)

        self._pca = decomp.PCA(n_components=self.rank)
        feats = self._pca.fit_transform(feats)
        self._fit = True
        return feats

    def transform(self, X: np.array) -> np.array:
        feats = self._tokenize(X)
        return self._pca.transform(feats)

    def explained_variance(self, n_components: int = 32) -> np.array:
        if not self._fit:
            print("`fit_transform` not called yet")
            return
        cum_var = np.cumsum(self._pca.explained_variance_ratio_)
        print(f"{n_components} features captures {cum_var[n_components] * 100:0.0f}% of the variance")
        return cum_var

    # TODO - move plot methods out of class to remove mpl dep from model
    def plot_explained_variance(self, n_components: int = 32) -> None:
        cum_var = self.explained_variance(n_components)
        fig = plt.figure("variance explanation")
        ax = fig.add_subplot(111)
        ax.plot(cum_var)
        ax.set_xlabel("N PCs")
        ax.set_ylabel("Fraction of Captured Variance")

    def plot_pcs(self, X: np.array, x: int = 0, y: int = 1) -> None:
        pcs = self.transform(X)

        fig, ax = plt.subplots()
        scat = ax.scatter(pcs[:, x], pcs[:, y], linewidths=1)
        ax.set_xlabel(f"Data Project onto PC {x + 1}")
        ax.set_ylabel(f"Data Project onto PC {y + 1}")
