# Save this as app.py

import streamlit as st
import random
import math
import numpy as np
import matplotlib.pyplot as plt

# --- Color Palette ---
def random_palette(k=5, mode='pastel'):
    if mode == 'vivid':
        return [(random.random(), random.random(), random.random()) for _ in range(k)]
    elif mode == 'autumn':
        return [((1 + random.random()) / 2, random.uniform(0.3, 0.8), random.uniform(0, 0.2)) for _ in range(k)]
    elif mode == 'ocean':
        return [(random.uniform(0, 0.2), random.uniform(0.3, 0.7), (1 + random.random()) / 2) for _ in range(k)]
    else:
        return [((1 + random.random()) / 2, (1 + random.random()) / 2, (1 + random.random()) / 2) for _ in range(k)]

# --- Shape Generators ---
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def circle(center=(0.5, 0.5), r=0.3, points=200):
    angles = np.linspace(0, 2 * math.pi, points)
    x = center[0] + r * np.cos(angles)
    y = center[1] + r * np.sin(angles)
    return x, y

def heart(center=(0.5, 0.5), r=0.3, points=300):
    t = np.linspace(0, 2 * np.pi, points)
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    x = center[0] + r * x / 16
    y = center[1] + r * y / 13
    return x, y

def star(center=(0.5, 0.5), r=0.3, points=5):
    angles = np.linspace(0, 2 * np.pi, points * 2 + 1)
    radii = np.array([r if i % 2 == 0 else r / 2 for i in range(len(angles))])
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

def triangle(center=(0.5, 0.5), r=0.3):
    angles = np.linspace(0, 2 * np.pi, 4)
    x = center[0] + r * np.cos(angles + np.pi/2)
    y = center[1] + r * np.sin(angles + np.pi/2)
    return x, y

def generate_shape(shape, center, r, wobble):
    if shape == 'circle':
        return circle(center, r)
    elif shape == 'heart':
        return heart(center, r)
    elif shape == 'star':
        return star(center, r)
    elif shape == 'triangle':
        return triangle(center, r)
    else:
        return blob(center, r, wobble=wobble)

# --- Poster Generation ---
def generate_poster(layers, wobble, seed, palette_mode, shape):
    fig, ax = plt.subplots(figsize=(7, 10))
    ax.axis('off')
    ax.set_facecolor((0.98, 0.98, 0.97))

    random.seed(seed)
    np.random.seed(seed)
    palette = random_palette(6, mode=palette_mode)

    for _ in range(layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        x_coords, y_coords = generate_shape(shape, (cx, cy), rr, wobble)
        color = random.choice(palette)
        alpha = random.uniform(0.25, 0.6)
        ax.fill(x_coords, y_coords, color=color, alpha=alpha, edgecolor=(0,0,0,0))

    title = f"Generative Poster • {palette_mode} • {shape}"
    ax.text(0.05, 0.95, title, fontsize=18, weight='bold', transform=ax.transAxes)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    st.pyplot(fig)

# --- Streamlit UI ---
st.title("🎨 Generative Poster")

layers = st.slider("Layers", 1, 50, 11)
wobble = st.slider("Wobble", 0.0, 0.8, 0.26, 0.01)
seed = st.number_input("Seed", min_value=0, max_value=10000, value=7015)
palette_mode = st.radio("Palette Mode", ['pastel', 'vivid', 'autumn', 'ocean'])
shape = st.selectbox("Shape", ['blob', 'circle', 'heart', 'star', 'triangle'])

if st.button("Generate Poster"):
    generate_poster(layers, wobble, seed, palette_mode, shape)
