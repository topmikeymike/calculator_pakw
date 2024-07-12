import streamlit as st
import pandas as pd
import uuid  # For generating unique IDs

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

def collect_household_data(data, generate_household_id):
    st.markdown("<h2 style='font-size:20px;' >Langkah 1 : Jumlah isi rumah</h2>", unsafe_allow_html=True)
    num_households = st.number_input('Masukkan jumlah isi rumah', min_value=1, value=1, step=1)
    selected_options_list = []
    total_pakw_hh = 0

    # Select Negeri
    st.markdown("<h2 style='font-size:20px;' >Langkah 2 : Masukkan negeri</h2>", unsafe_allow_html=True)
    selected_negeri = st.selectbox('NEGERI', ["Pilih"] + list(data['NEGERI'].unique()), key=f'NEGERI_{1}')

    # Filter Daerah options based on selected Negeri
    st.markdown("<h2 style='font-size:20px;' >Langkah 3 : Masukkan daerah</h2>", unsafe_allow_html=True)
    if selected_negeri != "Pilih":
        daerah_options = list(data[data['NEGERI'] == selected_negeri]['DAERAH'].unique())
        selected_daerah = st.selectbox('DAERAH', ["Pilih"] + daerah_options, key=f'DAERAH_{1}')
    else:
        selected_daerah = st.selectbox('DAERAH', ["Pilih"], key=f'DAERAH_{1}')

    # Filter Strata options based on selected Daerah
    st.markdown("<h2 style='font-size:20px;' >Langkah 4 : Masukkan strata</h2>", unsafe_allow_html=True)
    if selected_daerah != "Pilih":
        strata_options = list(data[data['DAERAH'] == selected_daerah]['STRATA'].unique())
        selected_strata = st.radio('STRATA', strata_options, key=f'STRATA_{1}')
    else:
        selected_strata = st.radio('STRATA', ["Pilih"], key=f'STRATA_{1}')

    for household_id in range(num_households):
        household_uuid = generate_household_id()  # Generate unique household ID for the session
    
        with st.expander(f'Isi Rumah {household_id + 1}'):
            # Create dropdown lists for categorical columns for individual member
            umur_ksh = st.selectbox('UMUR_KSH', ["Pilih"] + list(data['UMUR_KSH'].unique()), key=f'UMUR_KSH_{household_id}')
            jantina = st.radio('JANTINA', list(data['JANTINA'].unique()), key=f'JANTINA_{household_id}')

            # Calculate total expenditure for the household
            
            if (umur_ksh != "Pilih" and jantina != "Pilih" and selected_negeri != "Pilih" and 
                selected_daerah != "Pilih" and selected_strata != "Pilih"):
                
                filtered_data = data[
                    (data['UMUR_KSH'] == umur_ksh) & 
                    (data['JANTINA'] == jantina) &
                    (data['NEGERI'] == selected_negeri) &
                    (data['DAERAH'] == selected_daerah) &
                    (data['STRATA'] == selected_strata)
                ]

                if not filtered_data.empty:
                    total_mean_p_rent = filtered_data['Mean(p_rent)'].sum()
                    mean_p_rent = total_mean_p_rent / num_households
                    adjusted_mean_p_rent = mean_p_rent * (num_households ** 0.4745)

                    total_pakw = (
                        filtered_data['Mean(TOTAL_PAKW_MAKANAN)'].values[0] +
                        adjusted_mean_p_rent +
                        filtered_data['Mean(p_lain2)'].values[0]
                    )

                    selected_options = {
                        'HOUSEHOLD_ID': household_uuid,
                        'UMUR_KSH': umur_ksh,
                        'JANTINA': jantina,
                        'NEGERI': selected_negeri,
                        'DAERAH': selected_daerah,
                        'STRATA': selected_strata,
                        'TOTAL PAKW': total_pakw,
                        'TOTAL_HH': num_households  # Add total number of households
                    }

                    selected_options_list.append(selected_options)
                    total_pakw_hh += total_pakw  # Accumulate total PAKW HH

    # Set TOTAL PAKW HH for each entry if there are multiple households
    if num_households > 1:
        for option in selected_options_list:
            option['TOTAL PAKW HH'] = total_pakw_hh

    return selected_options_list
