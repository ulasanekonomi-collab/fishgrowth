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
# Menghitung Carrying Capacity (K)
K = ((luas_terumbu * 1.5) + (luas_mangrove * 1.2)) * (10 - indeks_pencemaran)
K = max(1000, K) 

populasi_saat_ini = st.sidebar.slider("Jumlah Populasi Ikan Saat Ini", 0, int(K*1.5), int(K*0.5))

# --- AREA UTAMA ---
st.title("Memahami Aspek Biologi Sumber Daya Ikan")
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
y_vals = np.maximum(y_vals, 0)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x_vals, y_vals, color='black', lw=2, label='Kurva Pertumbuhan')
ax.scatter([populasi_saat_ini], [pertumbuhan], color=warna, s=200, zorder=5, label='Kondisi Saat Ini')
ax.fill_between(x_vals, y_vals, color='skyblue', alpha=0.3)
ax.set_title('Hubungan Biomassa dan Pertumbuhan Ikan Baru')
ax.set_xlabel('Biomassa Ikan (x)')
ax.set_ylabel('Tambahan Ikan Baru (F(x))')
ax.grid(True, alpha=0.3)
ax.legend()
st.pyplot(fig)

# --- PANEL RUMUS INTERAKTIF ---
st.markdown("### Memahami Persamaan Pertumbuhan")
st.latex(r'''
\frac{dx}{dt} = r \cdot x \cdot \left( 1 - \frac{x}{K} \right)
''')

st.write("Dengan nilai parameter saat ini:")
st.markdown(f"""
- **r (Laju Pertumbuhan):** {r}
- **x (Populasi Ikan):** {populasi_saat_ini}
- **K (Daya Dukung):** {int(K)}
""")

st.write("Maka, laju perubahan populasi saat ini ($dx/dt$) adalah:")
st.markdown(f"**{r} × {populasi_saat_ini} × (1 - {populasi_saat_ini}/{int(K)}) = {pertumbuhan:.2f}**")



st.write("---")
st.info("💡 **Insight untuk Mahasiswa:** Titik MSY (puncak gunung) menunjukkan titik di mana pertumbuhan ikan paling optimal. Perubahan pada luasan habitat atau tingkat pencemaran akan menggeser titik ini secara instan.")

# --- FOOTER ---
st.markdown("---")
st.markdown("##### Dikembangkan Oleh: Yuhka Sundaya | Ekonomi Pembangunan Unisba, 2026")
