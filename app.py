import streamlit as st
import csv
import re
from difflib import SequenceMatcher


# ======================================
# PAGE CONFIGURATION
# ======================================

st.set_page_config(
    page_title="College FAQ Chatbot",
    page_icon="🎓",
    layout="centered"
)


# ======================================
# CUSTOM CSS
# ======================================

st.markdown("""
<style>

.stApp {
    background-color: #eef3fa;
}

.title {
    text-align: center;
    color: #183b70;
    font-size: 35px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #555;
    font-size: 17px;
}

</style>
""", unsafe_allow_html=True)


# ======================================
# LOAD CSV FILE
# ======================================

@st.cache_data
def load_faq():

    faqs = []

    with open(
        "faq_data.csv",
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            faqs.append(row)

    return faqs


faqs = load_faq()


# ======================================
# CLEAN TEXT
# ======================================

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r'[^a-z0-9\s]',
        '',
        text
    )

    return text


# ======================================
# FIND BEST ANSWER
# ======================================

def find_answer(user_question):

    user_question = clean_text(user_question)

    best_match = None

    highest_score = 0

    user_words = set(user_question.split())

    for faq in faqs:

        question = clean_text(faq["Question"])

        keywords = clean_text(faq["Keywords"])

        combined = question + " " + keywords

        faq_words = set(combined.split())

        common = user_words.intersection(faq_words)

        union = user_words.union(faq_words)

        word_score = (
            len(common) / len(union)
            if union else 0
        )

        similarity = SequenceMatcher(
            None,
            user_question,
            question
        ).ratio()

        score = (
            word_score * 0.6
            +
            similarity * 0.4
        )

        if score > highest_score:

            highest_score = score

            best_match = faq

    if highest_score >= 0.20 and best_match:

        return (
            best_match["Answer"],
            best_match["Category"]
        )

    else:

        return (
            "Sorry, I couldn't understand your question. "
            "Please try asking differently or contact "
            "the college administration.",
            "General"
        )


# ======================================
# WEBSITE HEADER
# ======================================

st.markdown(
    '<div class="title">🎓 College FAQ Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your smart assistant for college-related queries!'
    '</div>',
    unsafe_allow_html=True
)

st.write("")

st.info(
    "Ask me anything about Admission, Academics, "
    "Fees, Examinations, Attendance, Hostel, "
    "Library, Placements and Campus Facilities."
)


# ======================================
# SIDEBAR
# ======================================

st.sidebar.title("📚 FAQ Categories")

categories = sorted(
    set(faq["Category"] for faq in faqs)
)

for category in categories:

    count = sum(
        1 for faq in faqs
        if faq["Category"] == category
    )

    st.sidebar.write(
        f"📌 {category} ({count} questions)"
    )

st.sidebar.markdown("---")

st.sidebar.success(
    f"Total FAQs Available: {len(faqs)}"
)


# ======================================
# CHAT HISTORY
# ======================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! Welcome to the College FAQ Chatbot. How can I help you today?"
        }
    ]


# ======================================
# DISPLAY PREVIOUS MESSAGES
# ======================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ======================================
# USER INPUT
# ======================================

user_question = st.chat_input(
    "Type your college-related question here..."
)


# ======================================
# GENERATE RESPONSE
# ======================================

if user_question:

    # Display user question

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):

        st.markdown(user_question)

    # Find chatbot response

    answer, category = find_answer(user_question)

    response = (
        f"{answer}\n\n"
        f"**Category:** {category}"
    )

    # Display chatbot answer

    with st.chat_message("assistant"):

        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )




   
            

    



    
