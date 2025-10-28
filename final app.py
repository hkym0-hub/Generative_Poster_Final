# app.py
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# --- Streamlit UI ---
st.set_page_config(page_title="Generative Abstract Poster", layout="centered")
st.title("🎨 Generative Abstract Poster")
st.caption("Week 2 • Arts & Advanced Big Data")

# --- Sidebar Controls ---
st.sidebar.header("🎛️ Controls")

n_layers = st.sidebar.slider("Number of Layers", 1, 50, 11)
wobble = st.sidebar.slider("Wobble", 0.0, 0.8, 0.26, 0.01)
random_seed = st.sidebar.number_input("Random Seed", value=7015, step=1)

palette_mode = st.sidebar.selectbox("Color Palette", ['pastel', 'vivid', 'autumn', 'ocean'])
shape = st.sidebar.selectbox("Shape", ['blob', 'circle', 'heart', 'star', 'triangle'])

generate = st.sidebar.button("🎲 Generate Poster")

# --- Color Palette ---
def random_palette(k=6, mode='pastel'):
    if mode == 'vivid':
        return [(random.random(), random.random(), random.random()) for _ in range(k)]
    elif mode == 'autumn':
        return [((1 + random.random())/2, random.uniform(0.3,0.8), random.uniform(0,0.2)) for _ in range(k)]
    elif mode == 'ocean':
        return [(random.uniform(0,0.2), random.uniform(0.3,0.7), (1+random.random())/2) for _ in range(k)]
    else:  # pastel
        return [((1+random.random())/2, (1+random.random())/2, (1+random.random())/2) for _ in range(k)]

# --- Shapes ---
def blob(center=(0.5,0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2*math.pi, points)
    radii = r*(1 + wobble*(np.random.rand(points)-0.5))
    x = center[0] + radii*np.cos(angles)
    y = center[1] + radii*np.sin(angles)
    return x, y

def circle(center=(0.5,0.5), r=0.3, points=200):
    angles = np.linspace(0, 2*math.pi, points)
    x = center[0] + r*np.cos(angles)
    y = center[1] + r*np.sin(angles)
    return x, y

def heart(center=(0.5,0.5), r=0.3, points=300):
    t = np.linspace(0, 2*np.pi, points)
    x = 16*np.sin(t)**3
    y = 13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t)
    x = center[0] + r*x/16
    y = center[1] + r*y/13
    return x, y

def star(center=(0.5,0.5), r=0.3, points=5):
    angles = np.linspace(0, 2*math.pi, points*2 + 1)
    radii = np.array([r if i%2==0 else r/2 for i in range(len(angles))])
    x = center[0] + radii*np.cos(angles)
    y = center[1] + radii*np.sin(angles)
    return x, y

def triangle(center=(0.5,0.5), r=0.3):
    angles = np.linspace(0, 2*math.pi, 4)
    x = center[0] + r*np.cos(angles + np.pi/2)
    y = center[1] + r*np.sin(angles + np.pi/2)
    return x, y

def generate_shape(shape_name, center, r, wobble):
    if shape_name=='circle':
        return circle(center, r)
    elif shape_name=='heart':
        return heart(center, r)
    elif shape_name=='star':
        return star(center, r)
    elif shape_name=='triangle':
        return triangle(center, r)
    else:
        return blob(center, r, wobble=wobble)

# --- Generate Poster ---
if generate:
    random.seed(random_seed)
    np.random.seed(random_seed)

    plt.figure(figsize=(7,10))
    ax = plt.gca()
    ax.axis('off')
    ax.set_facecolor((0.98,0.98,0.97))

    palette = random_palette(6, mode=palette_mode)

    for _ in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15,0.45)
        x_coords, y_coords = generate_shape(shape, (cx, cy), rr, wobble)
        color = random.choice(palette)
        alpha = random.uniform(0.25,0.6)
        ax.fill(x_coords, y_coords, color=color, alpha=alpha, edgecolor=(0,0,0,0))

    ax.text(0.05,0.95,f"Generative Poster • {palette_mode} • {shape}", fontsize=18, weight='bold', transform=ax.transAxes)
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)

    st.pyplot(plt)
