import streamlit as st
import pandas as pd
import uuid  # For generating unique IDs

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

def collect_household_data(data, generate_household_id):
    st.markdown("<h2 style='font-size:20px;' >Langkah 1 : Jumlah ahli isi rumah</h2>", unsafe_allow_html=True)
    num_households = st.number_input('Masukkan jumlah ahli isi rumah', min_value=1, value=1, step=1)
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
        
    st.markdown("<h2 style='font-size:20px;' >Langkah 5 : Masukkan maklumat ahli isi rumah</h2>", unsafe_allow_html=True)
    for household_id in range(num_households):
        household_uuid = generate_household_id()  # Generate unique household ID for the session


        # Create a header row to mimic the table in the image
        cols = st.columns([2, 1, 1])  # Define the width of each column (UMUR/JANTINA, LELAKI, PEREMPUAN)
        cols[0].markdown("**UMUR/JANTINA**")
        cols[1].markdown("**LELAKI**")
        cols[2].markdown("**PEREMPUAN**")
        
        # Extract unique age ranges from the data
        unique_age_ranges = data['UMUR_KSH'].unique()
        
        # Loop through the unique age ranges and generate input fields for each
        for umur_ksh in unique_age_ranges:
            # Create a row for each age range
            row_cols = st.columns([2, 1, 1])
            row_cols[0].markdown(f"**{umur_ksh}**")
            
            # Number inputs for LELAKI and PEREMPUAN for each age range
            num_lelaki = row_cols[1].number_input(f'Lelaki {age_range}', min_value=0, key=f'lelaki_{age_range}_{household_id}', label_visibility="collapsed")
            num_perempuan = row_cols[2].number_input(f'Perempuan {age_range}', min_value=0, key=f'perempuan_{age_range}_{household_id}', label_visibility="collapsed")
            
            # You can save or process these values as necessary
            total_members = num_lelaki + num_perempuan
                
        # with st.expander(f'Isi Rumah {household_id + 1}'):
        #     # Define the mapping for sorting
        #     mapping = {
        #         "0-5 BULAN": 0.1,
        #         "6-8 BULAN": 0.2,
        #         "9-11 BULAN": 0.3,
        #         "1-3 TAHUN": 1.5,
        #         "4-6 TAHUN": 5,
        #         "7-9 TAHUN": 8,
        #         "10-12 TAHUN": 11,
        #         "13-15 TAHUN": 14,
        #         "16<18 TAHUN": 17,
        #         "18-29 TAHUN": 24,
        #         "30-59 TAHUN": 44,
        #         ">60 TAHUN": 60
        #     }
            
        #     # Extract unique age ranges from the data
        #     unique_age_ranges = data['UMUR_KSH'].unique()
            
        #     # Sort age ranges based on the mapping
        #     sorted_age_ranges = sorted(unique_age_ranges, key=lambda x: mapping.get(x, float('inf')))
            
        #     # Create the selectbox with sorted options
        #     umur_ksh = st.selectbox(
        #         'UMUR AHLI ISI RUMAH',
        #         ["Pilih"] + sorted_age_ranges,
        #         key=f'UMUR_KSH_{household_id}'
        #     )
        #     jantina = st.radio('JANTINA', list(data['JANTINA'].unique()), key=f'JANTINA_{household_id}')

            # Calculate total expenditure for the household
            # if (umur_ksh != "Pilih" and jantina != "Pilih" and selected_negeri != "Pilih" and 
            #     selected_daerah != "Pilih" and selected_strata != "Pilih"):
                
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

                total_pakw_mknn = (
                    filtered_data['Mean(TOTAL_PAKW_MAKANAN)'].values[0]
                )

                total_pakw_xmknn = (
                    total_pakw - total_pakw_mknn
                )
                    
                selected_options = {
                    'HOUSEHOLD_ID': household_uuid,
                    'UMUR_KSH': umur_ksh,
                    'JANTINA': jantina,
                    'NEGERI': selected_negeri,
                    'DAERAH': selected_daerah,
                    'STRATA': selected_strata,
                    'TOTAL PAKW': total_pakw,
                    'TOTAL MAKANAN': total_pakw_mknn,
                    'TOTAL X MAKANAN': total_pakw_xmknn,
                    'TOTAL_HH': num_households  # Add total number of households
                }

                    # # Prompt for additional income details if specific age ranges are selected
                    # if umur_ksh in ["18-29 TAHUN", "30-59 TAHUN", ">60 TAHUN"]:
                    #     st.markdown("<h2 style='font-size:20px;' >Langkah 6 : Masukkan pendapatan</h2>", unsafe_allow_html=True)
                    #     pendapatan_bergaji = st.number_input('PENDAPATAN BERGAJI', min_value=0, value=0, step=1, key=f'PENDAPATAN_BERGAJI_{household_id}')
                    #     pendapatan_bekerja_sendiri = st.number_input('PENDAPATAN BEKERJA SENDIRI', min_value=0, value=0, step=1, key=f'PENDAPATAN_BEKERJA_SENDIRI_{household_id}')
                    #     pendapatan_dari_harta_pelaburan = st.number_input('PENDAPATAN DARI HARTA PELABURAN', min_value=0, value=0, step=1, key=f'PENDAPATAN_DARI_HARTA_PELABURAN_{household_id}')
                    #     pindahan_semasa = st.number_input('PINDAHAN SEMASA', min_value=0, value=0, step=1, key=f'PINDAHAN_SEMASA_{household_id}')

                    #     total_income = (pendapatan_bergaji + pendapatan_bekerja_sendiri + 
                    #                     pendapatan_dari_harta_pelaburan + pindahan_semasa)
                        
                    #     total_pakw -= total_income

                        # selected_options.update({
                        #     'PENDAPATAN BERGAJI': pendapatan_bergaji,
                        #     'PENDAPATAN BEKERJA SENDIRI': pendapatan_bekerja_sendiri,
                        #     'PENDAPATAN DARI HARTA PELABURAN': pendapatan_dari_harta_pelaburan,
                        #     'PINDAHAN SEMASA': pindahan_semasa,
                        #     'TOTAL INCOME': total_income
                        # })

                selected_options_list.append(selected_options)
                total_pakw_hh += total_pakw  # Accumulate total PAKW HH
                total_pakw_hh += total_pakw_mknn 
                total_pakw_hh += total_pakw_xmknn 

    # Set TOTAL PAKW HH for each entry if there are multiple households
    if num_households > 1:
        for option in selected_options_list:
            option['TOTAL PAKW HH'] = total_pakw_hh

    return selected_options_list

# Example usage
# data = load_data('path_to_your_csv_file.csv')
# selected_options = collect_household_data(data, lambda: str(uuid.uuid4()))
# st.write(selected_options)
