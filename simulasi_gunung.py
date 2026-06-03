import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fase Pertumbuhan Ikan", layout="wide")
st.title("🏔️ Anatomi 'Gunung' Pertumbuhan Ikan")
st.markdown("Mengapa fungsi pertumbuhan ikan melengkung seperti gunung? Geser *slider* di bawah untuk melihat fase-fasenya.")

# --- PARAMETER DASAR ---
r = 0.5   # Laju pertumbuhan intrinsik
K = 10000 # Daya dukung lingkungan (Carrying Capacity)
msy_x = K / 2 # Titik MSY (Puncak Gunung)

# --- SLIDER INTERAKTIF ---
st.subheader("Simulasi Populasi Saat Ini")
populasi_saat_ini = st.slider(
    "Geser untuk mengubah jumlah populasi ikan di laut (Biomassa):", 
    min_value=0, 
    max_value=K, 
    value=1500, 
    step=100
)

# Menghitung pertumbuhan pada titik slider
pertumbuhan_saat_ini = r * populasi_saat_ini * (1 - (populasi_saat_ini / K))

# --- LOGIKA PENENTUAN FASE (4 FASE) ---
if populasi_saat_ini < (0.2 * K):
    fase = "1. Fase Kritis (Pemijahan Sulit)"
    warna = "red"
    penjelasan = "Populasi sangat sedikit. Ikan kesulitan mencari pasangan untuk kawin (pemijahan). Tambahan ikan baru sangat lambat."
elif populasi_saat_ini < (0.45 * K):
    fase = "2. Fase Pertumbuhan Eksponensial"
    warna = "blue"
    penjelasan = "Populasi cukup untuk berkembang biak dengan cepat. Daya dukung lingkungan (terumbu karang, pakan) masih sangat melimpah. Pertumbuhan melesat naik."
elif populasi_saat_ini <= (0.55 * K):
    fase = "3. Fase MSY (Maximum Sustainable Yield)"
    warna = "green"
    penjelasan = "Ini adalah PUNCAK GUNUNG. Populasi berada pada level paling optimal di mana reproduksi menghasilkan tambahan ikan terbanyak secara berkelanjutan."
else:
    fase = "4. Fase Kejenuhan (Mendekati Carrying Capacity)"
    warna = "orange"
    penjelasan = "Populasi ikan sudah terlalu padat dan mulai melebihi daya dukung laut. Persaingan makanan ketat, ruang gerak sempit, sehingga laju pertumbuhan ikan baru malah menurun."

# --- TAMPILAN STATUS FASE ---
st.markdown(f"### Status: <span style='color:{warna}'>{fase}</span>", unsafe_allow_html=True)
st.info(penjelasan)

# --- VISUALISASI GRAFIK ---
# Membuat data untuk kurva gunung (Parabola)
x_vals = np.linspace(0, K, 500)
y_vals = r * x_vals * (1 - (x_vals / K))

fig, ax = plt.subplots(figsize=(10, 5))

# Plot kurva utama
ax.plot(x_vals, y_vals, color='gray', linestyle='--', label='Kurva Pertumbuhan Logistik')

# Beri warna area di bawah kurva berdasarkan fase
ax.fill_between(x_vals, y_vals, where=(x_vals < 0.2*K), color='red', alpha=0.2, label='Fase 1')
ax.fill_between(x_vals, y_vals, where=((x_vals >= 0.2*K) & (x_vals < 0.45*K)), color='blue', alpha=0.2, label='Fase 2')
ax.fill_between(x_vals, y_vals, where=((x_vals >= 0.45*K) & (x_vals <= 0.55*K)), color='green', alpha=0.4, label='Fase 3 (MSY)')
ax.fill_between(x_vals, y_vals, where=(x_vals > 0.55*K), color='orange', alpha=0.2, label='Fase 4')

# Titik dinamis dari slider
ax.scatter([populasi_saat_ini], [pertumbuhan_saat_ini], color='black', s=150, zorder=5)
ax.annotate('  Posisi Saat Ini', (populasi_saat_ini, pertumbuhan_saat_ini), fontsize=12, fontweight='bold')

# Garis MSY
ax.axvline(x=msy_x, color='black', linestyle=':', label=f'Titik MSY (Populasi={msy_x})')

ax.set_title('Kurva Pertumbuhan Ikan (Biomassa vs Tambahan Baru)', fontsize=14)
ax.set_xlabel('Biomassa / Populasi Ikan ($x$)', fontsize=12)
ax.set_ylabel('Pertumbuhan Ikan / Tambahan Baru ($F(x)$)', fontsize=12)
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

st.pyplot(fig)
