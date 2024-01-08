# Install library yang diperlukan jika belum terpasang
# pip install streamlit pandas numpy

import streamlit as st
import numpy as np
import pandas as pd

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

L = np.array(['benefit', 'benefit', 'benefit', 'cost', 'cost'])

W = np.array([0.3, 0.2, 0.2, 0.15, 0.15])

def click_button():
    st.session_state.clicked = True

def mora(values, weights, labels):
    norm_values = sample_norm(values, labels)
    mora_values = calculate_mora(norm_values, weights)
    ranking_result = ranking(np.asarray(mora_values))
    return norm_values, mora_values, ranking_result

def sample_norm(values, label):
    if not values.shape[0] == label.shape[0]:
        st.write('Jumlah kriteria dan label tidak sama')
        return

    norm_value = []
    norm_all = []

    for i in range(values.shape[0]):
        if label[i] == 'benefit':
            for j in range(values[i].shape[0]):
                norm_c = values[i][j] / np.max(values[i])
                norm_value.append(norm_c)
        elif label[i] == 'cost':
            for j in range(values[i].shape[0]):
                norm_c = np.min(values[i]) / values[i][j]
                norm_value.append(norm_c)

        norm_all.append(norm_value)
        norm_value = []

    return np.array(norm_all)

def calculate_mora(values, weight):
    if not values.shape[0] == weight.shape[0]:
        print('Jumlah kriteria dan bobot tidak sama')
        return

    alt_crit_value = []
    all_value = []
    all_mora = []

    values = np.transpose(values)

    for i in range(values.shape[0]):
        for j in range(values[i].shape[0]):
            val = values[i][j] * weight[j]
            alt_crit_value.append(val)

        all_value.append(alt_crit_value)
        alt_crit_value = []

        mora = np.max(all_value)
        all_mora.append(mora)
        all_value = []

    return all_mora

def ranking(vector):
    temp = vector.argsort()
    ranks = np.empty_like(temp)
    ranks[temp] = np.arange(len(vector))

    return len(vector) - ranks

def run():
    st.set_page_config(
        page_title="Implementasi MORA",
        page_icon="👋",
    )

    st.write("# Implementasi Metode MORA")
    st.write("Muhammad akbar rohandi")

    st.markdown(
        """
        MORA (Multi-Objective Ratio Analysis) merupakan metode pengambilan keputusan multi-kriteria yang digunakan untuk memilih alternatif terbaik dari sejumlah alternatif berdasarkan sejumlah kriteria. Metode ini dirancang untuk memberikan solusi yang paling optimal dengan mempertimbangkan rasio antara kriteria dan bobot yang telah ditentukan.
        
        Contoh kasus yang akan diimplementasikan pada aplikasi ini adalah sebagai berikut:

        Sebuah Club bola akan melakukan rekrutmen Pemain terhadap **5 calon pemain** untuk posisi straiker. Posisi yang dibutuhkan hanya **2 orang**. Kriteria seleksi yang digunakan adalah sebagai berikut:

        - Kemampuan teknis (C1), Evaluasi ketrampilan teknis pemain, seperti dribbling, umpan, Ketrampilan menggiring bola.
        - Kekuatan fisik (C2), Kekuatan fisik pemain, termasuk kecepatan dan daya tahan tubuh.
        - Pengalaman (C3), Pengalaman pemain di berbagai turnamen dan pertandingan level tinggi
        - Statistik pertandingan (C4), kinerja pemain berdasarkan statistik seperti jumlah gol, assist, rating pertandingan.
        - Mentalitas (C5), Karakteristik mental pemain, seperti determinasi, konsistensi performa, dan kemampuan untuk beradaptasi dengan situasi pertandingan.

    """
    )

    st.divider()

    st.write("## Input Nilai Kriteria")

    c1 = st.slider("Nilai Kemampuan teknis", 1, 5, 1)
    c2 = st.slider("Nilai Kekuatan fisik", 1, 5, 1)
    c3 = st.slider("Nilai Pengalaman", 1, 5, 1)
    c4 = st.slider("Nilai Statistik pertandingan", 1, 5, 1)
    c5 = st.slider("Nilai mentalits", 1, 5, 1)

    if st.button("Simpan", type='primary', on_click=click_button):
        simpanData(c1, c2, c3, c4, c5)
    
    if st.session_state.clicked:
        data = st.session_state.nilai_kriteria
        df = pd.DataFrame(data, columns=('C1', 'C2', 'C3', 'C4', 'C5'))
        st.dataframe(df)

        if st.button("Proses"):
            prosesData()


def simpanData(c1, c2, c3, c4, c5):
    if 'nilai_kriteria' not in st.session_state:
        st.session_state.nilai_kriteria = np.array([[c1, c2, c3, c4, c5]])
    else:
        dataLama = st.session_state.nilai_kriteria
        dataBaru = np.append(dataLama, [[c1, c2, c3, c4, c5]], axis=0)
        st.session_state.nilai_kriteria = dataBaru

def prosesData():
    A = st.session_state.nilai_kriteria

    norm_a, mora_values, rank = mora(A, W, L)

    st.write("Nilai alternatif:")
    st.text(A)

    st.write("Normalisasi nilai alternatif:")
    st.text(norm_a)

    st.write("Perhitungan nilai MORA:")
    st.text(mora_values)

    st.write("Perankingan:")
    st.text(rank)


if __name__ == "__main__":
    run()