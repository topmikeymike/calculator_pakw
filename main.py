import streamlit as st
import pandas as pd
import uuid
from household_calculator import collect_household_data, load_data
import base64

st.set_page_config(
    page_title="Aplikasi Kalkulator PAKW",
    page_icon="🧊",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
    html {
        font-size: 14px;
    }
    .reportview-container .main .block-container {
        max-width: 90%;
        padding: 3rem;
    }
    .footer-text {
        font-size: 12px;
        color: transparent;
    }
    .footer-text:hover {
        color: grey;
    }
    .big-button .stButton > button {
        font-size: 24px !important;
        padding: 20px 40px !important;
        color: #fff !important;
        background-color: #ff8c02 !important;
        border: none !important;
        border-radius: 8px !important;
    }
    .button-space {
        margin-top: 20px;
    }
    .info-icon {
        display: inline-block;
        margin-left: 5px;
        cursor: pointer;
        color: blue;
        font-size: 14px;
    }
    .info-icon:hover .tooltip {
        visibility: visible;
        opacity: 1;
    }
    .tooltip {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%; 
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #555 transparent transparent transparent;
    }
    .container {
        display: flex;
        justify-content: space-between;
         /* Adjust the gap between containers */
    }
    .left-container, .right-container {
        flex: 1;
        padding: 20px;
        border: 2px solid #ddd; /* Border around containers */
        border-radius: 8px; /* Rounded corners */
    }
    .left-container {
        max-width: 90%;
    }
    .right-container {
        max-width: 45%;
    }
    .spacing {
        margin-left: 20px;
    }

    .st-emotion-cache-13ln4jf {
        width: 100% !important;  /* Ensure it takes full width */
        padding: 6rem 1rem 10rem !important;  /* Custom padding */
        max-width: 100rem !important;  /* Adjust the max-width */
    }
    .header {
        display: flex;
        align-items: flex-start;
        flex-direction: row;
        flex-wrap: nowrap;
        align-content: flex-start;
        justify-content: flex-start;
    }
    .header img {
        margin-right: 20px;
    }
     .contact-info {
        display: flex;
        justify-content: space-evenly;
        align-items: flex-start;
        width: 14%;
        margin-top: 27px;
        flex-direction: row;
        flex-wrap: wrap;
        align-content: stretch;
    }
    .contact-text {
        font-size: 16px;
        font-weight: bold;
    }
    .icons-container {
        display: flex;
        gap: 10px;
    }
    .icons-container a {
        color: #000;
        text-decoration: none;
    }
    .icons-container a:hover {
        color: #007bff;
    }
    .logos {
        display: flex;
        justify-content: flex-start;
        width: 100%;
        flex-wrap: nowrap;
        flex-direction: row;
        align-content: center;
        align-items: center;
    }
    .logos img {
        margin-right: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to get image base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load images and convert to base64
logo1_base64 = get_image_base64("images/dosm.png")
logo2_base64 = get_image_base64("images/MM.png")
logo3_base64 = get_image_base64("images/padu.png")

# Header with logos
st.markdown("""
    <div class="header">
        <div class="logos">
            <img src="data:image/png;base64,{}" width="100">
            <img src="data:image/png;base64,{}" width="100">
            <img src="data:image/png;base64,{}" width="100">
        </div>
        <div class="contact-info">
            <p class="contact-text">HUBUNGI KAMI:</p>
            <div class="icons-container">
                <a href="#"><i class="fas fa-globe"></i></a> 
                <a href="https://web.facebook.com/StatsMalaysia"><i class="fab fa-facebook-f"></i></a>
                <a href="#"><i class="fa-brands fa-x-twitter"></i></a> 
                <a href="#"><i class="fa-brands fa-x-twitter"></i></a> 
                <a href="#"><i class="fab fa-instagram"></i></a> 
                <a href="#"><i class="fab fa-youtube"></i></a> 
            </div>
        </div>
    </div>
""".format(
    logo1_base64, logo2_base64, logo3_base64
), unsafe_allow_html=True)

# Function to reset session state
def reset_session_state():
    for key in st.session_state.keys():
        del st.session_state[key]

# Function to generate a unique household ID for the session
def generate_household_id():
    if 'household_id' not in st.session_state:
        st.session_state.household_id = uuid.uuid4().hex[:8]  # Generate a random 8-character hex string
    return st.session_state.household_id

# Main title
st.title("Kalkulator Perbelanjaan Isi Rumah 🧮")

st.markdown("<h1 style='font-size:24px; font-weight:bold;'>Perbelanjaan Asas Kehidupan Wajar | (PAKW)</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='font-size:22px;'>Kalkulator ini mengira jumlah perbelanjaan PAKW berdasarkan input pengguna.</h2>", unsafe_allow_html=True)

# Container for the description and the calculator
col1, col2 = st.columns([1, 1])  # Two equal-width columns

with col1:
    st.markdown("""
    <section class="left-container">
        <h2 style='font-size:22px;'>KALKULATOR KOS SARA HIDUP</h2>
        <ol>
            <li>Kalkulator KSH merupakan inisiatif Kerajaan untuk memaparkan kos perbelanjaan asas kehidupan wajar yang diperlukan oleh isi rumah mengikut negeri, daerah dan strata.</li>
            <li>Data yang dipaparkan adalah kajian yang dilakukan berdasarkan data Laporan Perbelanjaan Isi Rumah 2022.</li>
            <li>Data yang dipaparkan adalah merupakan nilai kos sara hidup semasa dan akan dikemaskini setiap tahun.</li>
            <li>Nilai KSH ini merangkumi 14 buah negeri dan 162 daerah pentadbiran beserta strata bandar dan luar bandar.</li>
            <li>Laporan penuh boleh di muat turun di: <a href="https://www.dosm.gov.my/portal-main/online-services?data=6">https://www.dosm.gov.my/portal-main/online-services?data=6</a></li>
        </ol>
    </section>
    """, unsafe_allow_html=True)

with col2:
    # Load the data
    data = load_data('pakw_calculator_referal.csv')

    # Collect household data
    selected_options_list = collect_household_data(data, generate_household_id)

    # Display total household expenditure
    if 'calculate_clicked' not in st.session_state:
        st.session_state.calculate_clicked = False

    # Add space above the button
    st.markdown('<div class="button-space"></div>', unsafe_allow_html=True)

    if st.button('Kira Jumlah Perbelanjaan Isi Rumah', key='calculate', help='Tekan untuk mengira jumlah perbelanjaan'):
        st.session_state.calculate_clicked = True

    if st.session_state.calculate_clicked:
        if selected_options_list:
            st.write("<p style='font-size:20px; font-weight:bold;'>Jumlah Perbelanjaan Isi Rumah</p>", unsafe_allow_html=True)
            total_household_expenditure = sum(option['TOTAL PAKW'] for option in selected_options_list)
            st.write(
                f"""
                <p style='font-size:16px; font-weight:bold;'>
                    TOTAL PAKW untuk semua isi rumah: RM {total_household_expenditure:.2f}
                    <span class='info-icon'>𝒾
                        <span class='tooltip'>This is the total expenditure for all households calculated based on the input data.</span>
                    </span>
                </p>
                """,
                unsafe_allow_html=True
            )

            # Display TOTAL PAKW HH for all households if applicable
            if selected_options_list[0]['TOTAL_HH'] > 1:
                st.write(
                    f"""
                    <p style='font-size:16px; font-weight:bold;'>
                        TOTAL PAKW HH untuk semua isi rumah: RM {selected_options_list[0]["TOTAL PAKW HH"]:.2f}
                        <span class='info-icon'>𝒾
                            <span class='tooltip'>This is the total PAKW for all households.</span>
                        </span>
                    </p>
                    """,
                    unsafe_allow_html=True
                )

            # Save selected options to CSV
            selected_options_df = pd.DataFrame(selected_options_list)

            # Conditionally add TOTAL PAKW HH column if there are multiple households
            if selected_options_list[0]['TOTAL_HH'] > 1:
                selected_options_df['TOTAL PAKW HH'] = selected_options_list[0]['TOTAL PAKW HH']

            # Save to CSV
            try:
                history = pd.read_csv('user_input_history.csv')
                history = pd.concat([history, selected_options_df], ignore_index=True)
                history.to_csv('user_input_history.csv', index=False)
            except FileNotFoundError:
                selected_options_df.to_csv('user_input_history.csv', index=False)

            # Display selected options in a minimalist table
            st.write("<p style='font-size:20px; font-weight:bold;'>Pilihan yang Dipilih:</p>", unsafe_allow_html=True)
            # Only select relevant columns for display
            display_columns = ['HOUSEHOLD_ID', 'UMUR_KSH', 'JANTINA', 'NEGERI', 'DAERAH', 'STRATA', 'TOTAL PAKW']
            if selected_options_list[0]['TOTAL_HH'] > 1:
                display_columns.append('TOTAL PAKW HH')
            display_columns.append('TOTAL_HH')
            st.dataframe(selected_options_df[display_columns], width=1000)  # Set width to accommodate all columns

        if st.button('Kira Semula'):
            reset_session_state()
            st.experimental_rerun()

# Footer
language_dict = {
    'footer': '© 2024 Kalkulator Perbelanjaan Isi Rumah',
    'footer2': 'BANK IN DULU MAT'
}

footer_html = f"""
    <div style="text-align:center; padding: 10px;">
        <p style="font-size: 12px; color: grey;">{language_dict['footer']}</p>
        <p class="footer-text">{language_dict['footer2']}</p>
        <p style="font-size: 12px; color: grey;">Ver.1.1</p>
    </div>
"""
st.markdown(footer_html, unsafe_allow_html=True)

