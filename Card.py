import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO
from streamlit_extras.metric_cards import style_metric_cards

# Mengatur background
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-image: linear-gradient(to bottom, #030637 0%, #720455 100%);
background-size: cover;
}
[data-testid="stSidebar"] > div:first-child {
background-image: url("https://wallpapers-clan.com/wp-content/uploads/2023/11/cute-pokemon-pikachu-rain-desktop-wallpaper-preview.jpg");
background-position: center;
backdrop-filter: blur(10px);
}
[data-testid="stHeader"] {
background: rgba(0,0,0,30);
}
[data-testid="stToolbar"] {
right: 2rem;
}

</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Load data
df = pd.read_csv("Data_pokemon.csv")

# Side Bar
st.sidebar.header("Filter by Type, Generation, and Legendary 🦕️")
select_all_option = "Select All"

division_name = st.sidebar.selectbox(
    "Pokemon Type 1",
    options=np.append(select_all_option, df["Type 1"].unique())
)

department_name = st.sidebar.selectbox(
    "Pokemon Type 2",
    options=np.append(select_all_option,df["Type 2"].unique())
)

class_name = st.sidebar.selectbox(
    "Select Generation",
    (select_all_option,1,2,3,4,5,6)
)

rating = st.sidebar.selectbox(
    "Select Legendary",
    (select_all_option,True,False)
)

# Add "Select All" option
pokemon_list = sorted(df['Name'].unique())
selectvalue = st.selectbox("Select your Pokemon, and you can also Select All", [select_all_option] + pokemon_list)

# Filter data berdasarkan pilihan di sidebar
filtered_df = df.copy()

if division_name != select_all_option:
    filtered_df = filtered_df[filtered_df["Type 1"] == division_name]

if department_name != select_all_option:
    filtered_df = filtered_df[filtered_df["Type 2"] == department_name]

if class_name != select_all_option:
    filtered_df = filtered_df[filtered_df["Generation"] == class_name]

if rating != select_all_option:
    filtered_df = filtered_df[filtered_df["Legendary"] == rating]

# KPIs (Key Performance Indicators)
if selectvalue != select_all_option:
    selected_pokemons = filtered_df[filtered_df['Name'] == selectvalue]
else:
    selected_pokemons = filtered_df.head(20)


st.markdown(f"<div style='font-size: 40px; font-weight: bold; text-align: center;'>Pokemon 🐉️</div>", unsafe_allow_html=True)

style_metric_cards(background_color="#FEF3E2", border_left_color="#FF4B4B", border_color="#1f66bd", box_shadow="#F71938")

# Fungsi untuk menampilkan informasi Pokemon
def display_pokemon_info(selected_pokemon):
    # Hitung jumlah Pokemon yang dipilih
    num_pokemons = len(selected_pokemon)
    
    # Tentukan lebar kolom berdasarkan jumlah Pokemon yang ditampilkan
    column_widths = [1.2, 2, 2]  # Misalnya, kolom pertama lebih lebar

    st.markdown("<hr style='size:30px;margin-top:0px'>", unsafe_allow_html=True)

    # Bagi layar menjadi kolom-kolom sesuai lebar yang ditentukan
    col1, col2, col3 = st.columns(column_widths)

    # Tampilkan nama Pokemon, gambar, dan total stats di kolom pertama
    with col1:
        st.markdown(f"<div style='font-size:30px;margin-bottom:-30px'>{selected_pokemon['Name']}</div>", unsafe_allow_html=True)
        
        # Mengambil URL gambar
        url = selected_pokemon['link']
        try:
            # Mengirimkan permintaan GET untuk mengunduh gambar
            response = requests.get(url)
            response.raise_for_status()  # Memastikan permintaan berhasil
            image_data = response.content
            # Membaca data gambar dari bytes ke objek gambar menggunakan PIL
            img = Image.open(BytesIO(image_data))
            st.image(img, width=150)
        except requests.exceptions.RequestException as e:
            st.error(f"Error loading image: {e}")
        
        st.markdown(f"<div style='font-size:15px;margin-bottom:5px;margin-top:-20px;text-align: center;border-radius: 50px;color:black; background:linear-gradient(to bottom, #FF6500 30%, #FFC100 100%)'>Total {selected_pokemon['Total']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:15px;margin-bottom:5px;text-align: center;border-radius: 50px;color:black; background:linear-gradient(to bottom, #ECB159 30%, #FEFBF6 100%)'>Type 1 {selected_pokemon['Type 1']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:15px;margin-bottom:5px;text-align: center;border-radius: 50px;color:black; background:linear-gradient(to bottom, #06D001 30%, #F3FF90 100%)'>Type 2 {selected_pokemon['Type 2']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:15px;margin-bottom:5px;text-align: center;border-radius: 50px;color:black;background:linear-gradient(to bottom, #37B7C3 30%, #EBF4F6 100%)'>Generation {selected_pokemon['Generation']}</div>", unsafe_allow_html=True)

    # Tampilkan deskripsi Pokemon menggunakan expander di kolom kedua
    with col2:
        st.markdown(f"<div style='font-size:30px;margin-bottom:10px;text-align: center'>Description</div>", unsafe_allow_html=True)
        with st.expander(f"Click to expand description of {selected_pokemon['Name']}"):
            st.markdown(f"<div style='font-size:15px;color:white; text-align: justify;padding:10px;overflow-y: scroll'>{selected_pokemon['desc']}</div>", unsafe_allow_html=True)

    # Tampilkan statistik Pokemon dalam radar chart di kolom ketiga
    with col3:
        st.markdown(f"<div style='font-size:30px;margin-bottom:23px;text-align: center'>Statistic</div>", unsafe_allow_html=True)
        stats = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
        values = [selected_pokemon[stat] for stat in stats]

        # Siapkan data radar chart
        N = len(values)
        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, values, color='red', alpha=0.25)
        ax.plot(angles, values, color='red', linewidth=2)
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(stats)
        ax.set_xticklabels(stats, fontsize=20)
        st.pyplot(fig)

# Tampilkan informasi Pokemon yang dipilih
for i in range(len(selected_pokemons)):
    display_pokemon_info(selected_pokemons.iloc[i])

