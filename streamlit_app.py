import streamlit as st

# Custom module imports (Preserved exactly)
from utils.youtube_loader import get_video_id, get_transcript
from utils.embedding import get_embeddings
from utils.vectore_store import create_vector_store
from chains.rag_chain import get_rag_chain
from config.llm import get_llm
from utils.text_splitter import split_text
from chains.summary_chain import generate_summary
from chains.notes_chain import generate_notes
from chains.flashcard_chain import generate_flashcards
from chains.quiz_chain import generate_quiz

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="YouTube Research Companion",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom minimal CSS for custom button active/hover states & clean borders
st.markdown("""
    <style>
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize global embeddings configuration
embeddings = get_embeddings()

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "video_loaded" not in st.session_state:
    st.session_state.video_loaded = False
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Summary"

# Data cache storage to prevent unnecessary API re-calls when switching views
if "summary_data" not in st.session_state:
    st.session_state.summary_data = None
if "notes_data" not in st.session_state:
    st.session_state.notes_data = None
if "flashcards_data" not in st.session_state:
    st.session_state.flashcards_data = None
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Quiz microstate tracking
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []

# ==========================================
# SIDEBAR: SOURCE LOADER (NotebookLM Style)
# ==========================================
with st.sidebar:
    st.title("🎥 Research Source")
    st.caption("Load a video transcript into your workspace context.")
    st.divider()
    
    url = st.text_input(
        "YouTube Video URL", 
        placeholder="https://www.youtube.com/watch?v=..."
    )
    
    load_btn = st.button("🚀 Load Context Material", use_container_width=True, type="primary")
    
    if load_btn:
        if not url.strip():
            st.error("Please provide a valid YouTube URL.")
        else:
            try:
                with st.spinner("Fetching transcript & creating vectors..."):
                    video_id = get_video_id(url)
                    transcript = get_transcript(video_id)
                    docs = split_text(transcript)
                    vector_db = create_vector_store(docs, embeddings)
                    
                    retriever = vector_db.as_retriever(
                        search_type="mmr",
                        search_kwargs={"k": 5, "fetch_k": 20}
                    )
                    
                    llm = get_llm()
                    rag_chain = get_rag_chain(llm, retriever)
                    
                    # Store variables globally inside session state
                    st.session_state.transcript = transcript
                    st.session_state.docs = docs
                    st.session_state.rag_chain = rag_chain
                    st.session_state.video_loaded = True
                    
                    # Reset working memory and previous views for new video context
                    st.session_state.summary_data = None
                    st.session_state.notes_data = None
                    st.session_state.flashcards_data = None
                    st.session_state.quiz_data = None
                    st.session_state.messages = []
                    st.session_state.current_question = 0
                    st.session_state.user_answers = []
                    st.session_state.active_tab = "Summary"
                    
                    st.success("Context loaded successfully!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error loading source material: {str(e)}")

    if st.session_state.video_loaded:
        st.divider()
        st.success("🟢 Active Source Document Loaded")

# ==========================================
# MAIN WORKSPACE DESIGN
# ==========================================
st.title("💡 YouTube Study & Research Studio")

if not st.session_state.video_loaded:
    # Empty Slate Landing View
    st.info("👋 Welcome! Please enter a valid YouTube link in the left sidebar to generate your workspace notes, interactive flashcards, quizzes, and chat features.")
else:
    # Navigation Grid Bar
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📝 Summary", use_container_width=True, type="secondary" if st.session_state.active_tab != "Summary" else "primary"):
            st.session_state.active_tab = "Summary"
            st.rerun()
    with col2:
        if st.button("💬 Chat AI", use_container_width=True, type="secondary" if st.session_state.active_tab != "Chat" else "primary"):
            st.session_state.active_tab = "Chat"
            st.rerun()
    with col3:
        if st.button("📚 Study Notes", use_container_width=True, type="secondary" if st.session_state.active_tab != "Notes" else "primary"):
            st.session_state.active_tab = "Notes"
            st.rerun()
    with col4:
        if st.button("🃏 Flashcards", use_container_width=True, type="secondary" if st.session_state.active_tab != "Flashcards" else "primary"):
            st.session_state.active_tab = "Flashcards"
            st.rerun()
    with col5:
        if st.button("📊 Practice Quiz", use_container_width=True, type="secondary" if st.session_state.active_tab != "Quiz" else "primary"):
            st.session_state.active_tab = "Quiz"
            st.rerun()
            
    st.divider()

    # Isolate Execution Blocks using explicit IF-ELIF statements to prevent UI layout blending
    
    # --------------------------------------
    # FEATURE WORKSPACE: SUMMARY
    # --------------------------------------
    if st.session_state.active_tab == "Summary":
        st.subheader("📝 Executive Summary")
        if st.session_state.summary_data is None:
            with st.spinner("Synthesizing information..."):
                st.session_state.summary_data = generate_summary(st.session_state.docs)
        st.markdown(st.session_state.summary_data)

    # --------------------------------------
    # FEATURE WORKSPACE: CHAT
    # --------------------------------------
    elif st.session_state.active_tab == "Chat":
        st.subheader("💬 Deep-Dive Context Chat")
        
        # Display chronological interactive dialog log
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input("Ask a question about the video transcript context...")
        if question:
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)
                
            with st.spinner("Analyzing text chunks..."):
                response = st.session_state.rag_chain.invoke({"input": question})
                answer = response["answer"]
                
            st.session_state.messages.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.rerun()

    # --------------------------------------
    # FEATURE WORKSPACE: NOTES
    # --------------------------------------
    elif st.session_state.active_tab == "Notes":
        st.subheader("📚 Structured Study Notes")
        if st.session_state.notes_data is None:
            with st.spinner("Generating conceptual study guide..."):
                st.session_state.notes_data = generate_notes(st.session_state.docs)
        st.markdown(st.session_state.notes_data)

    # --------------------------------------
    # FEATURE WORKSPACE: FLASHCARDS
    # --------------------------------------
    elif st.session_state.active_tab == "Flashcards":
        st.subheader("🃏 Interactive Active-Recall Cards")
        if st.session_state.flashcards_data is None:
            with st.spinner("Creating knowledge cards..."):
                st.session_state.flashcards_data = generate_flashcards(st.session_state.docs)
                
        for i, card in enumerate(st.session_state.flashcards_data):
            with st.expander(f"🔍 Card {i+1}: {card['question']}"):
                st.info(f"💡 Answer:")

    # --------------------------------------
    # FEATURE WORKSPACE: QUIZ ENGINE
    # --------------------------------------
    elif st.session_state.active_tab == "Quiz":
        st.subheader("📊 Performance Assessment Quiz")
        
        if st.session_state.quiz_data is None:
            if st.button("🎯 Generate Video Assessment Quiz", type="primary"):
                with st.spinner("Formulating analytical evaluation options..."):
                    st.session_state.quiz_data = generate_quiz(st.session_state.docs)
                    st.session_state.current_question = 0
                    st.session_state.user_answers = []
                    st.rerun()
        else:
            quiz = st.session_state.quiz_data
            index = st.session_state.current_question

            # Render State: Quiz Completed Result Calculation
            if index >= len(quiz):
                score = sum(1 for user, q in zip(st.session_state.user_answers, quiz) if user == q["answer"])
                percentage = (score / len(quiz)) * 100

                st.balloons() if percentage >= 70 else None
                st.success("🎉 Comprehensive Quiz Complete!")
                
                col_m1, col_m2 = st.columns(2)
                col_m1.metric("Correct Items Score", f"{score} / {len(quiz)}")
                col_m2.metric("Total Accuracy Ratio", f"{percentage:.1f}%")

                st.subheader("📊 Granular Breakdown Performance")
                for i, (user, q) in enumerate(zip(st.session_state.user_answers, quiz)):
                    with st.expander(f"Question {i+1} Details"):
                        st.write(f"**Question:** {q['question']}")
                        if user == q["answer"]:
                            st.success(f"✅ Correct: {user}")
                        else:
                            st.error(f"❌ Your Answer: {user}")
                            st.info(f"✅ Correct Answer Guide: {q['answer']}")

                if st.button("🔄 Retake Quiz", type="primary"):
                    st.session_state.current_question = 0
                    st.session_state.user_answers = []
                    st.rerun()
            
            # Render State: Question Presentation Screen Loop
            else:
                current_question = quiz[index]
                st.progress((index) / len(quiz))
                st.markdown(f"### **Question {index + 1} of {len(quiz)}**")
                st.markdown(f"#### {current_question['question']}")
                
                selected_answer = st.radio(
                    "Choose the most accurate choice option:",
                    current_question["options"],
                    key=f"question_radio_{index}"
                )
                
                _, col_b = st.columns([4, 1])
                button_text = "Finish Evaluation 🏁" if index == len(quiz) - 1 else "Next Question ➡️"
                
                if col_b.button(button_text, use_container_width=True, type="primary"):
                    st.session_state.user_answers.append(selected_answer)
                    st.session_state.current_question += 1
                    st.rerun()