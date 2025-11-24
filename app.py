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
    user_input = st.text_area(
        "Enter a sentence containing a number:",
        "The database has 66723107008 records.",
    )

    if st.button("Convert"):
        if user_input.strip():
            result = converter.process_sentence(user_input)
            st.subheader("Result")
            st.write(f"**Input:** {user_input}")
            st.success(f"**Output:** {result}")
        else:
            st.warning("Please enter text.")

elif input_method == "Upload Text File":
    st.sidebar.info("Upload a .txt file. Each line will be processed.")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type="txt")
    
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        results = []
        for raw_line in stringio:
            line = raw_line.strip()
            if not line:
                continue
            try:
                output = converter.process_sentence(line)
            except Exception as exc:
                output = f"error: {exc}"
            results.append({"Input": line, "Output": output})

        if not results:
            st.warning("No non-empty lines found in the uploaded file.")
        else:
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Results as CSV",
                csv,
                "conversion_results.csv",
                "text/csv",
            )
