import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Anatomi Pertumbuhan Ikan", layout="wide")

# --- PANEL KONTROL DI KIRI (SIDEBAR) ---
st.sidebar.header("🕹️ Panel Kontrol Ekosistem")

# Parameter yang mempengaruhi Carrying Capacity (K)
st.sidebar.markdown("### Pengaruh Lingkungan")
kesehatan_terumbu = st.sidebar.slider("Kesehatan Terumbu Karang (%)", 10, 100, 80)
suhu_normal = st.sidebar.slider("Stabilitas Suhu (Kesesuaian %)", 10, 100, 90)

# Menghitung Carrying Capacity dinamis berdasarkan kesehatan ekosistem
# K dasar adalah 10.000, jika terumbu dan suhu optimal maka K maksimal
K = (10000 * (kesehatan_terumbu / 100) * (suhu_normal / 100))

# Parameter Pertumbuhan
r = st.sidebar.slider("Laju Pertumbuhan Intrinsik (r)", 0.1, 1.0, 0.5, step=0.1)

# Populasi saat ini
st.sidebar.markdown("---")
populasi_saat_ini = st.sidebar.slider("Jumlah Populasi Ikan Saat Ini", 0, int(K), int(K*0.2))

# --- AREA UTAMA ---
st.title("🏔️ Anatomi 'Gunung' Pertumbuhan Ikan")
st.write(f"**Carrying Capacity (K) saat ini:** {int(K)} unit biomassa.")

# Logika Fase
pertumbuhan = r * populasi_saat_ini * (1 - (populasi_saat_ini / K))

if populasi_saat_ini < (0.2 * K):
    fase = "1. Fase Kritis (Pemijahan Sulit)"
    warna = "red"
elif populasi_saat_ini < (0.45 * K):
    fase = "2. Fase Pertumbuhan Eksponensial"
    warna = "blue"
elif populasi_saat_ini <= (0.55 * K):
    fase = "3. Fase MSY (Puncak Keberlanjutan)"
    warna = "green"
else:
    fase = "4. Fase Kejenuhan (Over-Capacity)"
    warna = "orange"

st.markdown(f"### Status Fase: <span style='color:{warna}'>{fase}</span>", unsafe_allow_html=True)

# --- VISUALISASI ---
x_vals = np.linspace(0, K, 500)
y_vals = r * x_vals * (1 - (x_vals / K))

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x_vals, y_vals, color='black', lw=2)
ax.scatter([populasi_saat_ini], [pertumbuhan], color=warna, s=200, zorder=5, label='Kondisi Saat Ini')
ax.fill_between(x_vals, y_vals, color='skyblue', alpha=0.3)

ax.set_title('Kurva Pertumbuhan Ikan (Fungsi Logistik)')
ax.set_xlabel('Biomassa Ikan (x)')
ax.set_ylabel('Tambahan Ikan Baru (F(x))')
ax.grid(True, alpha=0.3)
st.pyplot(fig)

st.write("---")
st.info("💡 **Insight untuk Mahasiswa:** Jika Terumbu Karang rusak, geser slider 'Kesehatan' ke kiri. Perhatikan bagaimana puncak 'gunung' (K) menyusut. Inilah mengapa perikanan tidak bisa dipisahkan dari konservasi habitat.")
