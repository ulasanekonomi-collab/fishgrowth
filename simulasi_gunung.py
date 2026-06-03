import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulasi Bioekonomi", layout="wide")

# --- PANEL KONTROL DI KIRI (SIDEBAR) ---
st.sidebar.header("🕹️ Panel Kontrol Ekosistem")

st.sidebar.markdown("### 🗺️ Data Spasial Habitat (Hektar)")
luas_terumbu = st.sidebar.slider("Luasan Terumbu Karang (Ha)", 0, 5000, 2500)
luas_mangrove = st.sidebar.slider("Luasan Hutan Mangrove (Ha)", 0, 5000, 2500)

st.sidebar.markdown("### 🧪 Kondisi Lingkungan")
indeks_pencemaran = st.sidebar.slider("Tingkat Pencemaran (0=Bersih, 10=Sangat Tercemar)", 0.0, 10.0, 2.0)
r = st.sidebar.slider("Laju Pertumbuhan Intrinsik (r)", 0.1, 1.0, 0.5, step=0.1)

st.sidebar.markdown("---")
# K dihitung berdasarkan luasan habitat dan dikurangi dampak pencemaran
K = ((luas_terumbu * 1.5) + (luas_mangrove * 1.2)) * (10 - indeks_pencemaran)
K = max(1000, K) # Pastikan K minimal 1000

populasi_saat_ini = st.sidebar.slider("Jumlah Populasi Ikan Saat Ini", 0, int(K*1.5), int(K*0.5))

# --- AREA UTAMA ---
st.title("🏔️ SIMULASI PERTUMBUHAN SUMBER DAYA IKAN")
st.write(f"**Carrying Capacity (K) saat ini:** {int(K)} unit biomassa.")

# Perhitungan pertumbuhan
pertumbuhan = r * populasi_saat_ini * (1 - (populasi_saat_ini / K))

# Logika Fase
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
x_vals = np.linspace(0, K*1.2, 500)
y_vals = r * x_vals * (1 - (x_vals / K))
# Pastikan tidak negatif di grafik
y_vals = np.maximum(y_vals, 0)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x_vals, y_vals, color='black', lw=2, label='Kurva Pertumbuhan')
ax.scatter([populasi_saat_ini], [pertumbuhan], color=warna, s=200, zorder=5, label='Kondisi Saat Ini')
ax.fill_between(x_vals, y_vals, color='skyblue', alpha=0.3)

ax.set_title('Hubungan Biomassa dan Pertumbuhan Ikan Baru')
ax.set_xlabel('Biomassa Ikan (x)')
ax.set_ylabel('Tambahan Ikan Baru (F(x))')
ax.grid(True, alpha=0.3)
ax.legend()
st.pyplot(fig)

st.write("---")
st.info("""
**Catatan untuk Mahasiswa:**
- Titik **MSY** adalah titik puncak gunung (di mana pertumbuhan paling maksimal).
- Jika **Indeks Pencemaran** naik, lihat bagaimana gunung menyusut dan titik MSY bergeser ke kiri.
- Jika **Luasan Mangrove/Terumbu** bertambah, gunung akan tumbuh melebar, menunjukkan daya dukung (K) yang lebih besar bagi ikan.
""")
