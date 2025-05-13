import streamlit as st
from openai import OpenAI
import os

# Configure Streamlit page
st.set_page_config(page_title="AI Opportunity Analyzer", layout="centered")

# Get OpenAI API key from environment or secret
api_key = os.getenv("OPENAI_API_KEY")
# Replace with your key if not using secrets
client = OpenAI(api_key=api_key)

# Header
st.title("🔍 AI Opportunity Analyzer")
st.markdown("""
This tool helps identify high-impact AI opportunities and builds a 90-day transformation roadmap.

Fill out the brief intake form below to begin.
""")

# Intake form
with st.form("ai_diagnosis_form"):
    department = st.selectbox("Which department are you analyzing?", [
        "Operations", "Finance", "HR", "Customer Support", "Marketing", "IT",
        "Other"
    ])
    pain_point = st.text_area(
        "What is the most repetitive or manual task in this department?",
        height=100)
    data_used = st.text_area(
        "What kind of data do you typically work with? (e.g., spreadsheets, databases, paper forms)",
        height=100)
    volume = st.radio("How frequent is this task?",
                      ["Multiple times a day", "Daily", "Weekly", "Monthly"])
    impact = st.radio("How important is this task to business performance?",
                      ["Low", "Medium", "High"])

    submitted = st.form_submit_button("Analyze AI Opportunities")


# Updated OpenAI generation logic
def generate_ai_recommendation(inputs):
    prompt = f"""
    You are an AI strategy consultant. Based on the following operational context, generate:
    1. Three tailored AI or automation use cases with:
       - A short explanation of each
       - A score for ROI (1–5)
       - A score for implementation feasibility (1–5)
    2. A 90-day AI Transformation Roadmap (Month 1, 2, 3)

    Context:
    - Department: {inputs['department']}
    - Pain Point: {inputs['pain_point']}
    - Data Used: {inputs['data_used']}
    - Task Frequency: {inputs['volume']}
    - Task Importance: {inputs['impact']}

    Present results clearly using bullet points.
    """

    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[{
                                                  "role": "user",
                                                  "content": prompt
                                              }],
                                              temperature=0.7)
    return response.choices[0].message.content


# Display result
if submitted:
    st.session_state.inputs = {
        "department": department,
        "pain_point": pain_point,
        "data_used": data_used,
        "volume": volume,
        "impact": impact
    }

    st.success("Inputs captured! Generating recommendations...")

    with st.spinner("Analyzing with GPT..."):
        try:
            ai_output = generate_ai_recommendation(st.session_state.inputs)
            st.subheader("📊 AI Use Cases & Roadmap")
            st.markdown(ai_output)
        except Exception as e:
            st.error(f"An error occurred: {e}")
# Reset button
if st.button("🔄 Start Over"):
    for key in ["inputs"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
