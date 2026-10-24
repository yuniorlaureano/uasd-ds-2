from __future__ import annotations

import argparse
import json
import os
import random
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from inf8239_u03_gen.data import normalize_images, validate_images
from inf8239_u03_gen.evaluation import mean_pairwise_distance, nearest_neighbors
from inf8239_u03_gen.models import build_autoencoder, build_encoder_decoder

ROOT = Path(__file__).resolve().parents[1]
SEED = 42
PANEL_SIZE = 16
CLASSES = ["Camiseta", "Pantalón", "Suéter", "Vestido", "Abrigo", "Sandalia", "Camisa", "Zapatilla", "Bolso", "Botín"]
os.environ.setdefault("TF_DETERMINISTIC_OPS", "1")
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)


class VAE(tf.keras.Model):
    def __init__(self, encoder, decoder):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.loss_tracker = tf.keras.metrics.Mean(name="loss")
        self.reconstruction_tracker = tf.keras.metrics.Mean(name="reconstruction")
        self.kl_tracker = tf.keras.metrics.Mean(name="kl")

    @property
    def metrics(self):
        return [self.loss_tracker, self.reconstruction_tracker, self.kl_tracker]

    def compute_losses(self, images, training):
        mean, log_variance = self.encoder(images, training=training)
        epsilon = tf.random.normal(tf.shape(mean))
        latent = mean + tf.exp(0.5 * log_variance) * epsilon
        reconstruction = self.decoder(latent, training=training)
        reconstruction_loss = tf.reduce_mean(tf.reduce_sum(tf.keras.losses.binary_crossentropy(images, reconstruction), axis=(1, 2)))
        kl_loss = -0.5 * tf.reduce_mean(tf.reduce_sum(1 + log_variance - tf.square(mean) - tf.exp(log_variance), axis=1))
        return reconstruction_loss + kl_loss, reconstruction_loss, kl_loss

    def update_trackers(self, total_loss, reconstruction_loss, kl_loss):
        self.loss_tracker.update_state(total_loss)
        self.reconstruction_tracker.update_state(reconstruction_loss)
        self.kl_tracker.update_state(kl_loss)
        return {metric.name: metric.result() for metric in self.metrics}

    def train_step(self, data):
        images = data[0] if isinstance(data, tuple) else data
        with tf.GradientTape() as tape:
            losses = self.compute_losses(images, training=True)
        gradients = tape.gradient(losses[0], self.trainable_weights)
        self.optimizer.apply_gradients(zip(gradients, self.trainable_weights))
        return self.update_trackers(*losses)

    def test_step(self, data):
        images = data[0] if isinstance(data, tuple) else data
        return self.update_trackers(*self.compute_losses(images, training=False))


def image_panel(path: Path, rows, row_titles, column_titles):
    figure, axes = plt.subplots(len(rows), PANEL_SIZE, figsize=(PANEL_SIZE, len(rows) * 1.15))
    for row, (collection, title) in enumerate(zip(rows, row_titles)):
        for column in range(PANEL_SIZE):
            axis = axes[row, column]
            axis.imshow(collection[column].squeeze(), cmap="gray", vmin=0, vmax=1)
            axis.set_xticks([])
            axis.set_yticks([])
            if column_titles[row] is not None:
                axis.set_title(column_titles[row][column], fontsize=6)
        axes[row, 0].set_ylabel(title, fontsize=7, rotation=0, ha="right", va="center")
    figure.tight_layout()
    figure.savefig(path, dpi=170)
    plt.close(figure)


def training_curves(path: Path, ae_history, vae_history):
    figure, axes = plt.subplots(1, 3, figsize=(13, 3.4))
    panels = [(axes[0], ae_history, "loss", "AE · BCE por píxel"),
              (axes[1], vae_history, "reconstruction", "VAE · reconstrucción (BCE suma)"),
              (axes[2], vae_history, "kl", "VAE · KL")]
    for axis, history, key, title in panels:
        epochs = range(1, len(history[key]) + 1)
        axis.plot(epochs, history[key], marker="o", label="entrenamiento")
        axis.plot(epochs, history[f"val_{key}"], marker="o", label="validación")
        axis.set_title(title)
        axis.set_xlabel("época")
        axis.legend()
    figure.tight_layout()
    figure.savefig(path, dpi=150)
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs-ae", type=int, default=6)
    parser.add_argument("--epochs-vae", type=int, default=8)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    reports = ROOT / "reports"
    models = ROOT / "models"
    reports.mkdir(exist_ok=True)
    models.mkdir(exist_ok=True)
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
    x_train = normalize_images(x_train)
    x_test = normalize_images(x_test)
    if args.limit:
        x_train, y_train = x_train[: args.limit], y_train[: args.limit]
        x_test, y_test = x_test[: max(100, args.limit // 5)], y_test[: max(100, args.limit // 5)]
    validate_images(x_train)
    # Misma partición que validation_split=0.1 de Keras: el último 10 % de entrenamiento.
    split = int(len(x_train) * 0.9)
    x_fit, x_val = x_train[:split], x_train[split:]

    start = perf_counter()
    autoencoder = build_autoencoder(tf)
    autoencoder.compile(optimizer="adam", loss="binary_crossentropy", metrics=["mse"])
    ae_history = autoencoder.fit(x_fit, x_fit, validation_data=(x_val, x_val), epochs=args.epochs_ae, batch_size=256,
                                 callbacks=[tf.keras.callbacks.EarlyStopping(patience=2, restore_best_weights=True)], verbose=2)
    ae_seconds = perf_counter() - start
    encoder, decoder = build_encoder_decoder(tf, latent_dim=2)
    vae = VAE(encoder, decoder)
    vae.compile(optimizer="adam")
    start = perf_counter()
    vae_history = vae.fit(x_fit, validation_data=(x_val,), epochs=args.epochs_vae, batch_size=256, verbose=2)
    vae_seconds = perf_counter() - start
    training_curves(reports / "training_curves.png", ae_history.history, vae_history.history)

    # Panel no seleccionado: 16 índices de prueba elegidos con semilla fija, no a mano.
    rng = np.random.default_rng(SEED)
    panel_index = rng.choice(len(x_test), size=PANEL_SIZE, replace=False)
    originals = x_test[panel_index]
    ae_reconstructed = autoencoder.predict(originals, verbose=0)
    mean, _ = encoder.predict(originals, verbose=0)
    vae_reconstructed = decoder.predict(mean, verbose=0)
    generated = decoder.predict(rng.normal(size=(PANEL_SIZE, 2)), verbose=0)
    neighbor_index, neighbor_distance = nearest_neighbors(generated, x_train)
    neighbors = x_train[neighbor_index]
    image_panel(reports / "ae_vae_panel.png",
                [originals, ae_reconstructed, vae_reconstructed, generated, neighbors],
                ["Original", "AE", "VAE", "Muestra VAE", "Vecino train"],
                [[CLASSES[label] for label in y_test[panel_index]], None, None, None,
                 [f"{CLASSES[y_train[i]]}\n{d:.3f}" for i, d in zip(neighbor_index, neighbor_distance)]])

    grid = np.array([(1 - value) * np.array([-2.0, -1.0]) + value * np.array([2.0, 1.0]) for value in np.linspace(0, 1, 12)])
    interpolation = decoder.predict(grid, verbose=0)
    figure, axes = plt.subplots(1, 12, figsize=(12, 1.3))
    for axis, image in zip(axes, interpolation):
        axis.imshow(image.squeeze(), cmap="gray")
        axis.axis("off")
    figure.savefig(reports / "interpolation.png", dpi=170, bbox_inches="tight")
    plt.close(figure)

    ae_test_bce, ae_test_mse = autoencoder.evaluate(x_test, x_test, batch_size=256, verbose=0)
    vae_test = vae.evaluate(x_test, batch_size=256, verbose=0, return_dict=True)
    vae_test_mse = float(np.mean((decoder.predict(encoder.predict(x_test, verbose=0)[0], verbose=0) - x_test) ** 2))
    # Referencia: distancia de imágenes reales de prueba a su vecino de entrenamiento.
    _, real_distance = nearest_neighbors(originals, x_train)
    autoencoder.save(models / "autoencoder.keras")
    decoder.save(models / "decoder.keras")
    metrics = {
        "seed": SEED,
        "train_size": len(x_fit), "validation_size": len(x_val), "test_size": len(x_test),
        "ae_epochs_run": len(ae_history.history["loss"]), "vae_epochs_run": len(vae_history.history["loss"]),
        "ae_train_seconds": ae_seconds, "vae_train_seconds": vae_seconds,
        "ae_parameters": autoencoder.count_params(), "decoder_parameters": decoder.count_params(),
        "ae_test_bce": ae_test_bce, "ae_test_mse": ae_test_mse,
        "vae_test_loss": float(vae_test["loss"]), "vae_test_reconstruction": float(vae_test["reconstruction"]),
        "vae_test_kl": float(vae_test["kl"]), "vae_test_mse": vae_test_mse,
        "history": {"ae": ae_history.history, "vae": vae_history.history},
        "panel_test_indices": panel_index.tolist(),
        "generated_nn_distance_mean": float(neighbor_distance.mean()),
        "generated_nn_distance_min": float(neighbor_distance.min()),
        "real_test_nn_distance_mean": float(real_distance.mean()),
        "generated_diversity": mean_pairwise_distance(generated),
        "real_test_diversity": mean_pairwise_distance(originals),
        "generated_nn_classes": [CLASSES[y_train[i]] for i in neighbor_index],
    }
    (reports / "training_metrics.json").write_text(json.dumps(metrics, indent=2, default=float), encoding="utf-8")
    print(json.dumps({key: value for key, value in metrics.items() if key != "history"}, indent=2, default=float))


if __name__ == "__main__":
    main()
