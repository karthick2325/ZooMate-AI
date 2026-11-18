import base64
from pathlib import Path

import streamlit as st
from utils.chat_handler import chat_with_zoo_mate

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ZooMate AI",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

BANNER_PATH = ASSETS_DIR / "wildlife_banner.png"
SIDEBAR_IMAGE_PATH = ASSETS_DIR / "sidebar_image.png"

# Optional photos for the four suggested-question cards.
SUGGESTION_IMAGES = {
    "lion": ASSETS_DIR / "lion.png",
    "elephant": ASSETS_DIR / "elephant.png",
    "tiger": ASSETS_DIR / "tiger.png",
    "parrot": ASSETS_DIR / "parrot.png",
}


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "language" not in st.session_state:
    st.session_state.language = "English"

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "display_question" not in st.session_state:
    st.session_state.display_question = None


# ============================================================
# DATA
# ============================================================

animal_categories = {
    "🦁 Big Cats": ["Lion", "Tiger", "Leopard"],
    "🐘 Mammals": ["Elephant", "Giraffe", "Deer"],
    "🦜 Birds": ["Parrot", "Eagle", "Peacock"],
    "🐍 Reptiles": ["Snake", "Crocodile", "Turtle"],
    "🐬 Aquatic Animals": ["Dolphin", "Whale", "Shark"],
    "🦋 Insects": ["Butterfly", "Bee", "Ant"]
}

comparison_animals = [
    "Lion", "Tiger", "Elephant", "Giraffe", "Leopard", "Deer",
    "Crocodile", "Snake", "Dolphin", "Whale", "Eagle", "Parrot"
]

feeding_animals = [
    "Lion", "Tiger", "Elephant", "Giraffe", "Deer", "Parrot",
    "Eagle", "Peacock", "Snake", "Crocodile", "Turtle",
    "Dolphin", "Whale", "Shark", "Butterfly", "Bee", "Ant"
]

conservation_animals = [
    "Tiger", "Elephant", "Lion", "Leopard", "Giraffe", "Deer",
    "Parrot", "Eagle", "Peacock", "Crocodile", "Turtle",
    "Dolphin", "Whale", "Shark"
]


# ============================================================
# IMAGE HELPER
# ============================================================

def image_as_data_uri(path):
    """Read a local image and return an embeddable data URI."""
    if not path.exists():
        return None

    suffix = path.suffix.lower()
    mime = "image/jpeg" if suffix in (".jpg", ".jpeg") else "image/png"

    try:
        encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
        return f"data:{mime};base64,{encoded}"
    except OSError:
        return None


def submit_question(prompt, display_text=None):
    st.session_state.pending_question = prompt
    st.session_state.display_question = display_text or prompt
    st.rerun()


# ============================================================
# CUSTOM CSS
# The document itself is fixed to the viewport.
# The conversation transcript is the only scrollable main area.
# ============================================================

st.markdown("""
<style>
:root {
    --forest: #123f2c;
    --forest-dark: #0c3323;
    --forest-light: #246442;
    --sage: #eaf4e9;
    --sage-light: #f5faf3;
    --line: #d9e8d7;
    --ink: #183c2b;
    --muted: #718477;
}

/* Stop the browser page from becoming a scrolling document */
html, body {
    height: 100%;
    overflow: hidden !important;
}

.stApp {
    height: 100vh;
    overflow: hidden !important;
    background: #fbfdf9;
    color: var(--ink);
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    height: 100vh;
    max-height: 100vh;
    overflow: hidden !important;
}

[data-testid="stHeader"] {
    height: 0;
    background: transparent;
}

[data-testid="stToolbar"] {
    right: 0.5rem;
}

/* Main content sizing */
.main .block-container {
    box-sizing: border-box;
    width: 100%;
    max-width: 1700px;
    height: 100vh;
    max-height: 100vh;
    overflow: hidden !important;
    padding: 0.45rem 1.2rem 0.35rem 1.2rem;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
}

/* Keep Streamlit's main vertical layout compact */
.main .block-container > div {
    min-height: 0;
}

/* ---------------- SIDEBAR ---------------- */

[data-testid="stSidebar"] {
    width: 265px !important;
    min-width: 265px !important;
    background: linear-gradient(180deg, #eaf4e9 0%, #f8fbf6 100%);
    border-right: 1px solid #d6e6d5;
}

[data-testid="stSidebar"] > div:first-child {
    height: 100vh;
    max-height: 100vh;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    padding: 0.65rem 0.8rem 0.65rem 0.8rem;
    scrollbar-width: thin;
    scrollbar-color: #b6cdb5 transparent;
}

/* Reserved sidebar image area */
.sidebar-image-frame {
    width: 100%;
    height: 112px;
    border-radius: 16px;
    overflow: hidden;
    margin: 2px 0 9px 0;
    background: linear-gradient(135deg, #dcebd9, #f5faf2);
    border: 1px dashed #a9c8aa;
}

.sidebar-image-frame img {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: cover;
}

/* Compact horizontal brand */
.sidebar-brand {
    background: linear-gradient(120deg, #103e2b, #246442);
    border-radius: 13px;
    padding: 10px 12px;
    color: white;
    margin-bottom: 8px;
}

.sidebar-brand-title {
    color: white;
    font-size: 21px;
    font-weight: 800;
    line-height: 1.15;
    margin: 0;
}

.sidebar-brand-subtitle {
    color: #e1efe1;
    font-size: 11px;
    margin: 4px 0 0 0;
}

[data-testid="stSidebar"] h3 {
    color: #174d32;
    font-size: 16px;
    margin: 0.4rem 0 0.25rem 0;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #718477;
    font-size: 11px;
}

[data-testid="stSidebar"] [data-testid="stExpander"] {
    border: 1px solid #d2e3d1;
    border-radius: 10px;
    background: rgba(255,255,255,0.68);
    margin: 4px 0;
}

[data-testid="stSidebar"] [data-testid="stExpander"] details summary {
    color: #204d34;
    font-weight: 650;
    padding-top: 7px;
    padding-bottom: 7px;
}

[data-testid="stSidebar"] [data-baseweb="select"] > div {
    border-radius: 9px;
    border-color: #c9ddca;
    background: #ffffff;
    min-height: 36px;
}

[data-testid="stSidebar"] div.stButton > button {
    min-height: 35px;
    padding: 0.2rem 0.45rem;
    border-radius: 9px;
    border: 1px solid #cfe1cf;
    background: #ffffff;
    color: #205b38;
    font-size: 12px;
    font-weight: 650;
}

[data-testid="stSidebar"] div.stButton > button:hover {
    background: #e4f1e2;
    border-color: #83ad87;
}

/* ---------------- MAIN BANNER ---------------- */

.wildlife-banner {
    width: 100%;
    height: 142px;
    border-radius: 16px;
    overflow: hidden;
    margin: 0 0 7px 0;
    flex: 0 0 auto;
    background: #dcebd9;
}

.wildlife-banner img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center 47%;
    display: block;
}

/* Fallback if banner file is missing */
.wildlife-banner-fallback {
    width: 100%;
    height: 142px;
    border-radius: 16px;
    margin-bottom: 7px;
    padding: 20px 28px;
    box-sizing: border-box;
    background: linear-gradient(110deg, #103e2b, #4b8054);
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.wildlife-banner-fallback h2 {
    color: white;
    margin: 0 0 5px 0;
    font-size: 27px;
}

.wildlife-banner-fallback p {
    color: #edf6ec;
    margin: 0;
    font-size: 13px;
}

/* ---------------- WELCOME ---------------- */

.welcome-card {
    width: 100%;
    box-sizing: border-box;
    background: linear-gradient(110deg, #eaf5e8, #f8fcf6);
    border: 1px solid #d7e8d5;
    border-radius: 16px;
    padding: 12px 19px;
    margin: 0 0 5px 0;
    flex: 0 0 auto;
}

.welcome-card h3 {
    color: #205d38;
    font-size: 20px;
    margin: 0 0 5px 0;
}

.welcome-card p {
    color: #536b59;
    font-size: 13px;
    margin: 3px 0;
}

/* ---------------- SUGGESTIONS ---------------- */

.section-heading {
    color: #245c3a;
    font-size: 19px;
    font-weight: 800;
    margin: 2px 0 5px 0;
}

.suggestion-card {
    height: 100px;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px;
    background: #ffffff;
    border: 1px solid #dfeade;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(30, 75, 42, 0.06);
    overflow: hidden;
}

.suggestion-card img {
    width: 82px;
    height: 82px;
    flex: 0 0 82px;
    border-radius: 12px;
    object-fit: cover;
}

.suggestion-emoji {
    width: 82px;
    height: 82px;
    flex: 0 0 82px;
    border-radius: 12px;
    background: #edf5eb;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 39px;
}

.suggestion-question {
    color: #183c2b;
    font-size: 13px;
    font-weight: 750;
    line-height: 1.25;
}

.suggestion-action div.stButton > button {
    min-height: 31px;
    margin-top: 3px;
    border-radius: 0 0 10px 10px;
    font-size: 12px;
}

/* ---------------- CHAT TRANSCRIPT ---------------- */

/* st.container(height=...) provides the only scrollable conversation region */
[data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stChatMessage"]) {
    border-radius: 14px;
}

[data-testid="stChatMessage"] {
    background: #ffffff;
    border: 1px solid #e1ebe0;
    border-radius: 15px;
    padding: 8px 11px;
    margin: 5px 0;
    box-shadow: 0 2px 8px rgba(25, 70, 40, 0.035);
}

/* ---------------- CHAT INPUT ---------------- */

[data-testid="stChatInput"] {
    position: fixed;
    bottom: 12px;
    left: max(285px, calc((100vw - 1700px) / 2 + 285px));
    right: max(20px, calc((100vw - 1700px) / 2 + 20px));
    z-index: 999;
    border: 1px solid #8fb495;
    border-radius: 20px;
    background: #ffffff;
    box-shadow: 0 4px 18px rgba(32, 91, 52, 0.12);
}

[data-testid="stChatInput"] textarea {
    color: #183c2b;
}

/* Keep the bottom of the transcript clear of the fixed composer */
.chat-bottom-space {
    height: 8px;
}

/* General buttons */
div.stButton > button {
    border-radius: 10px;
    border: 1px solid #cfe1cf;
    background: #ffffff;
    color: #205b38;
    font-weight: 650;
}

div.stButton > button:hover {
    background: #e7f3e5;
    border-color: #83ad87;
    color: #123f2c;
}

/* Narrow screens */
@media (max-width: 900px) {
    [data-testid="stSidebar"] {
        width: 245px !important;
        min-width: 245px !important;
    }

    .main .block-container {
        padding: 0.35rem 0.6rem;
    }

    .wildlife-banner,
    .wildlife-banner-fallback {
        height: 112px;
    }

    .suggestion-card {
        height: 82px;
        gap: 5px;
        padding: 5px;
    }

    .suggestion-card img,
    .suggestion-emoji {
        width: 52px;
        height: 52px;
        flex-basis: 52px;
        font-size: 27px;
    }

    .suggestion-question {
        font-size: 10px;
    }

    [data-testid="stChatInput"] {
        left: 255px;
        right: 10px;
    }
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # Add your own image later at:
    # E:\ZooMate_AI\assets\sidebar_image.png
    sidebar_image_uri = image_as_data_uri(SIDEBAR_IMAGE_PATH)

    if sidebar_image_uri:
        st.markdown(
            f"""
            <div class="sidebar-image-frame">
                <img src="{sidebar_image_uri}" alt="ZooMate wildlife sidebar">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="sidebar-image-frame"></div>',
            unsafe_allow_html=True
        )

    st.markdown("""
    <div class="sidebar-brand">
        <p class="sidebar-brand-title">🐾 ZooMate AI</p>
        <p class="sidebar-brand-subtitle">Your Wildlife Learning Companion</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💬 Chat with ZooMate")
    st.caption("Ask • Learn • Explore • Conserve")

    st.divider()

    # Animal categories
    with st.expander("🐾 Explore Animal Categories", expanded=False):
        category_names = list(animal_categories.keys())
        selected_category = st.selectbox(
            "Choose category",
            category_names,
            key="animal_category"
        )

        selected_animals = animal_categories[selected_category]
        animal_columns = st.columns(2)

        for index, animal in enumerate(selected_animals):
            with animal_columns[index % 2]:
                if st.button(
                    animal,
                    key=f"animal_{animal}",
                    width="stretch"
                ):
                    submit_question(
                        f"Tell me about {animal}. Explain its habitat, diet, behaviour and interesting facts.",
                        f"Tell me about {animal}."
                    )

    # Compare animals
    with st.expander("⚖️ Compare Animals", expanded=False):
        animal_one = st.selectbox(
            "First Animal",
            comparison_animals,
            key="compare_one"
        )

        animal_two = st.selectbox(
            "Second Animal",
            comparison_animals,
            index=1,
            key="compare_two"
        )

        if st.button("⚖️ Compare Now", width="stretch"):
            if animal_one == animal_two:
                st.warning("Please select two different animals.")
            else:
                submit_question(
                    f"Compare {animal_one} and {animal_two}. Explain habitat, diet, physical features, behaviour, lifespan and conservation status. Present a clear comparison table.",
                    f"Compare {animal_one} and {animal_two}."
                )

    # Feeding guide
    with st.expander("🥬 Animal Feeding Guide", expanded=False):
        selected_feeding_animal = st.selectbox(
            "Choose an animal",
            feeding_animals,
            key="feeding_animal"
        )

        if st.button("🥬 Explore Feeding Guide", width="stretch"):
            submit_question(
                f"Give me a detailed feeding guide for {selected_feeding_animal}. Explain natural diet, food preferences, feeding behaviour, nutritional requirements and safe feeding practices in zoos. Zoo animals must only be fed according to approved diets and trained animal care staff instructions. Do not invent exact food quantities.",
                f"Show me the feeding guide for {selected_feeding_animal}."
            )

    # Wildlife conservation
    with st.expander("🌿 Wildlife Conservation", expanded=False):
        selected_conservation_animal = st.selectbox(
            "Choose an animal",
            conservation_animals,
            key="conservation_animal"
        )

        if st.button("🌿 Explore Conservation", width="stretch"):
            submit_question(
                f"Explain wildlife conservation for {selected_conservation_animal}. Cover conservation status, major threats, habitat protection, anti-poaching efforts, breeding programmes and how people can help. Do not invent statistics.",
                f"Explore conservation of {selected_conservation_animal}."
            )

    st.divider()

    st.markdown("### 🌐 Language / மொழி")

    st.selectbox(
        "Choose language",
        ["English", "தமிழ்"],
        index=0 if st.session_state.language == "English" else 1,
        key="language_selector"
    )
    st.session_state.language = st.session_state.language_selector

    if st.button("🗑️ Clear Chat", width="stretch"):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.session_state.display_question = None
        st.rerun()

    st.caption("🌱 Powered by Gemini AI + LangChain")


# ============================================================
# MAIN HEADER / BANNER
# ============================================================

banner_uri = image_as_data_uri(BANNER_PATH)

if banner_uri:
    st.markdown(
        f"""
        <div class="wildlife-banner">
            <img src="{banner_uri}" alt="ZooMate AI wildlife banner">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown("""
    <div class="wildlife-banner-fallback">
        <h2>🐾 ZooMate AI — Discover the World of Wildlife</h2>
        <p>Ask questions • Learn about animals • Explore nature • Protect wildlife</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# HOME CONTENT
# Welcome and suggestions disappear after the first message
# so the conversation has enough vertical space.
# ============================================================

if not st.session_state.messages:

    st.markdown("""
    <div class="welcome-card">
        <h3>🌱 Welcome to ZooMate AI! 👋</h3>
        <p>Discover fascinating animal facts, habitats, diets, behaviour and wildlife conservation.</p>
        <p><strong>🐾 Your intelligent wildlife assistant is ready to help!</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">⚡ Try asking</div>',
        unsafe_allow_html=True
    )

    suggestions = [
        ("lion", "🦁", "Tell me about lions."),
        ("elephant", "🐘", "How do elephants communicate?"),
        ("tiger", "🐅", "What are endangered animals?"),
        ("parrot", "🦜", "Explain tiger habitat.")
    ]

    suggestion_columns = st.columns(4)

    for index, (image_key, emoji, question_text) in enumerate(suggestions):
        with suggestion_columns[index]:

            animal_image_uri = image_as_data_uri(
                SUGGESTION_IMAGES[image_key]
            )

            if animal_image_uri:
                image_html = (
                    f'<img src="{animal_image_uri}" '
                    f'alt="{image_key}" class="suggestion-photo">'
                )
            else:
                image_html = (
                    f'<div class="suggestion-emoji">{emoji}</div>'
                )

            st.markdown(
                f"""
                <div class="suggestion-card">
                    {image_html}
                    <div class="suggestion-question">{question_text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.container():
                if st.button(
                    "Explore →",
                    key=f"suggestion_{index}",
                    width="stretch"
                ):
                    submit_question(question_text)


# ============================================================
# CHAT TRANSCRIPT
# Only this container scrolls when the conversation grows.
# ============================================================

if st.session_state.messages:
    transcript_height = 405
else:
    transcript_height = 82

with st.container(height=transcript_height, border=False):

    if not st.session_state.messages:
        st.markdown(
            """
            <div style="
                text-align:center;
                color:#829286;
                padding:12px 8px;
                font-size:12px;">
                🐾 Your conversation with ZooMate AI will appear here.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        for message in st.session_state.messages:
            avatar = "🧑" if message["role"] == "user" else "🐾"

            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])


# ============================================================
# CHAT INPUT / GEMINI RESPONSE
# ============================================================

user_input = st.chat_input("Ask anything about animals... 🐾")

pending_question = st.session_state.pending_question
display_question = st.session_state.display_question

question = user_input or pending_question

if question:

    visible_question = (
        user_input
        if user_input
        else display_question or question
    )

    st.session_state.messages.append({
        "role": "user",
        "content": visible_question
    })

    language_instruction = (
        "Reply in Tamil."
        if st.session_state.language == "தமிழ்"
        else "Reply in English."
    )

    with st.spinner("🌿 ZooMate AI is exploring..."):
        response = chat_with_zoo_mate(
            question + "\n\n" + language_instruction,
            chat_history=st.session_state.messages[:-1]
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.session_state.pending_question = None
    st.session_state.display_question = None

    st.rerun()
