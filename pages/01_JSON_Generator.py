import streamlit as st
import json

st.title("JSON Generator")

# Create a list to store the RSI values
rsi_values = []

# Create a function to generate the JSON structure
def generate_json():
    rsi_base = st.text_input("RSI Base:", "RSI_{}")
    rsi_upper_thold = st.number_input("RSI Upper Threshold:", 70)
    rsi_upper_side = st.selectbox("RSI Upper Side:", ["PositionSide.SHORT", "PositionSide.LONG"])
    rsi_down_thold = st.number_input("RSI Down Threshold:", 30)
    rsi_down_side = st.selectbox("RSI Down Side:", ["PositionSide.SHORT", "PositionSide.LONG"])
    rsi_length = st.number_input("RSI Length:", 14)
    rsi_config = {'length': rsi_length}
    rsi_dict = {'base': rsi_base, 'upper_thold': rsi_upper_thold, 'upper_side': rsi_upper_side, 'down_thold': rsi_down_thold, 'down_side': rsi_down_side, 'config': rsi_config}
    if st.button('Generate JSON'):
        rsi_values.append(rsi_dict)
        # st.success(json.dumps({'crossover':{'rsi': rsi_values}}, indent=2))

# Run the function
col1, col2 = st.columns(2)
with col1:
    generate_json()
with col2:
    st.json(rsi_values)