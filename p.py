from groq import Groq
import streamlit as st
import os
from dotenv import load_dotenv
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
}
</style>
""", unsafe_allow_html=True)
def id_note():
    try:
        with open("n.txt","r")as f:
            count=sum(1 for line in f if line.startswith("NO:"))
            return count + 1
    except FileNotFoundError:
        return 1

if "note_id" not in st.session_state:
    st.session_state.note_id=id_note()
# Remove load_dotenv()
# Use Streamlit Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def save(notes, note_id):
    with open("n.txt", "a") as f:
        f.write(f"NO:{note_id}\n{notes}\n\n")
    st.success("Notes Saved")
def see():
    try:
        with open("n.txt","r")as f:
            return f.read()
    except FileNotFoundError:
        return "File Not Found"
def delete(no):
  
    try:
        with open("n.txt","r")as f:
            lines=f.readlines()
        new_line=[]
        skip = False
        for line in lines:
            if line.startswith(f"NO:{no}"):
                skip=True
                continue
            if skip and line.startswith("NO:"):
                skip=False
            if not skip:
                new_line.append(line)
        with open ("n.txt","w")as f:
            f.writelines(new_line)
        
    except FileNotFoundError:
        st.warning("Note  not find")
st.markdown("""
    <h1 style='text-align:center;
            color:#4CAF50;
            font-size:50px;'>
            AI Notes Assistant
            </h1>
    <p style='text-align:center;
            color:gray;
            font-size:20px;'>
            Save Notes • Ask AI • Manage Knowledge
            </p>  
""",unsafe_allow_html=True)
with st.sidebar:
    st.header("📊 Dashboard")
    st.markdown("""
        <style>
                .stMetric label {color:green !important;}
                .stMetric [data-testid="stMetricValue"] {color:#4CAF50 !important;}
                </style>
""",unsafe_allow_html=True)
    st.metric("Next Notes ID",st.session_state.note_id)
    if os.path.exists("n.txt"):
        st.success("Notes File Found")
    else:
        st.warning("Notes File not Found")
    col1,col2=st.columns(2)
    with col1:
        savee=st.button("Save Notes")
    with col2:
        seee=st.button("See Notes")

def style(contant,height=200):
    st.markdown("""
        <style>
            .card {
                padding: 20px;
                border-radius: 15px;
                background: #1f2937;
                border:2px dashed #6FA8DC;
                margin-bottom: 20px;
            }
                div[data-testid="stTextArea"] textarea {
                background: #2d3748 !important;
                color: white !important;
                border-radius: 8px !important;
                border:2px inset #6FA8DC;
                border:2px dashed #6FA8DC;}

                div[data-testid="stTextInput"] input{
                background: #2d3748 !important;
                color: white !important;
                border-radius: 8px !important;
                border:2px inset #6FA8DC;
                border:2px dashed #6FA8DC;
                }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    result=contant()
    st.markdown("</div>", unsafe_allow_html=True)
    return result
def notess():
    return st.text_area("✍️ Write Notes", height=150)
def question():
    return st.text_input("Enter your question:", value=st.session_state.question)
notes=style(notess)

if savee:
    save(notes,st.session_state.note_id)
    st.session_state.note_id+=1
if seee:
    st.write(see())
st.divider()
st.subheader("🤖 Ask AI About Your Notes")

# Initialize session state for question
if 'question' not in st.session_state:
    st.session_state.question = ""

st.session_state.question =style(question)

# Single button for asking
if st.button("Ask AI"):
    if st.session_state.question.strip():
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Notes:
{see()}

Question:
{st.session_state.question}
"""
                }
            ]
        )
        st.info(response.choices[0].message.content)
    else:
        st.warning("Please enter your question.")

with st.expander("I want delet file"):
    no=st.number_input("Please enter notes no. for delete: ",min_value=1,step=1)
    if st.button("delete all notes"):  
        if no: 
            delete(no)
            st.success(f"Deleted note no.{no}")