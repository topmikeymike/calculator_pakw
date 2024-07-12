import streamlit as st
import pandas as pd
import uuid

st.set_page_config(
    page_title="Aplikasi Kalkulator PAKW",
    page_icon="🧊",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
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
    </style>
    """,
    unsafe_allow_html=True,
)

from household_calculator import collect_household_data, load_data

# Function to reset session state
def reset_session_state():
    for key in st.session_state.keys():
        del st.session_state[key]

# Function to generate a unique household ID for the session
def generate_household_id():
    if 'household_id' not in st.session_state:
        st.session_state.household_id = uuid.uuid4().hex[:8]  # Generate a random 8-character hex string
    return st.session_state.household_id

# Header
st.title("Kalkulator Perbelanjaan Isi Rumah 🧮")

st.markdown("<h1 style='font-size:24px; font-weight:bold;'>Perbelanjaan Asas Kehidupan Wajar | (PAKW)</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='font-size:22px;'>Kalkulator ini mengira jumlah perbelanjaan PAKW berdasarkan input pengguna.</h2>", unsafe_allow_html=True)

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
