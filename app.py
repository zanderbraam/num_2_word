import streamlit as st
import pandas as pd
from io import StringIO
from converter import NumberConverter

# Initialize logic
converter = NumberConverter()

st.set_page_config(page_title="Num2Word Converter", layout="wide")

st.title("🔢 Number to Word Converter")
st.markdown("""
This application converts numbers embedded in text into their English word equivalents.
It handles **large integers**, **validation**, and **file uploads**.
""")

# --- Sidebar for Inputs ---
st.sidebar.header("Input Method")
input_method = st.sidebar.radio("Choose input:", ["Manual Text Entry", "Upload Text File"])

if input_method == "Manual Text Entry":
    user_input = st.text_input("Enter a sentence containing a number:", "The database has 66723107008 records.")
    
    if st.button("Convert"):
        if user_input:
            result = converter.process_sentence(user_input)
            st.subheader("Result")
            st.success(result)
        else:
            st.warning("Please enter text.")

elif input_method == "Upload Text File":
    st.sidebar.info("Upload a .txt file. Each line will be processed.")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type="txt")
    
    if uploaded_file is not None:
        # Read file
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        lines = stringio.readlines()
        
        results = []
        for line in lines:
            line = line.strip()
            if line:
                output = converter.process_sentence(line)
                results.append({"Input": line, "Output": output})
        
        # Display Dataframe
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)
        
        # Option to download results (Enhancement)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download Results as CSV",
            csv,
            "conversion_results.csv",
            "text/csv"
        )
