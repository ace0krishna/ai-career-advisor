import streamlit as st

from llm_parser import (
    extract_student_profile,
    explain_career_recommendation
)

from fuzzy_engine import calculate_all_careers


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Career Advisor",
    page_icon="🧭",
    layout="wide"
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🧭 AI Based Career Advisor")

st.write(
    "Describe your skills, interests, strengths and goals. "
    "The AI will understand your description and use "
    "fuzzy logic to calculate career suitability."
)

st.divider()


# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------

student_input = st.text_area(
    "👤 Tell me about yourself:",
    placeholder=(
        "Example: I enjoy coding and mathematics. "
        "I like solving logical problems and I am interested "
        "in artificial intelligence and technology. "
        "I want a technical career."
    ),
    height=180
)


# ---------------------------------------------------------
# ANALYZE BUTTON
# ---------------------------------------------------------

if st.button(
    "🔍 Analyze My Career Profile",
    use_container_width=True
):

    if not student_input.strip():

        st.warning(
            "Please describe yourself first."
        )

    else:

        # -------------------------------------------------
        # STEP 1: LLM ANALYSIS
        # -------------------------------------------------

        with st.spinner(
            "🤖 AI is understanding your profile..."
        ):

            profile = extract_student_profile(
                student_input
            )


        # -------------------------------------------------
        # DISPLAY EXTRACTED PROFILE
        # -------------------------------------------------

        st.subheader(
            "📊 AI-Extracted Profile"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "💻 Coding",
                f"{profile['coding']}/10"
            )

            st.metric(
                "📐 Mathematics",
                f"{profile['mathematics']}/10"
            )


        with col2:

            st.metric(
                "🧠 Logical Thinking",
                f"{profile['logical_thinking']}/10"
            )

            st.metric(
                "🎨 Creativity",
                f"{profile['creativity']}/10"
            )


        with col3:

            st.metric(
                "🗣️ Communication",
                f"{profile['communication']}/10"
            )

            st.metric(
                "💡 Technology Interest",
                f"{profile['technology_interest']}/10"
            )


        st.divider()


        # -------------------------------------------------
        # STEP 2: FUZZY LOGIC
        # -------------------------------------------------

        with st.spinner(
            "🧠 Running fuzzy inference system..."
        ):

            career_scores = calculate_all_careers(
                profile
            )


        # -------------------------------------------------
        # CAREER SCORES
        # -------------------------------------------------

        st.subheader(
            "🎯 Career Suitability"
        )

        for career, score in career_scores.items():

            st.write(
                f"**{career}** — {score}/100"
            )

            st.progress(
                min(int(score), 100)
            )


        st.divider()


        # -------------------------------------------------
        # FIND HIGHEST SCORE
        # -------------------------------------------------

        top_career = max(
            career_scores,
            key=career_scores.get
        )

        top_score = career_scores[
            top_career
        ]


        st.subheader(
            "🏆 Highest Suitability"
        )

        st.success(
            f"{top_career} — {top_score}/100"
        )


        # -------------------------------------------------
        # STEP 3: LLM EXPLANATION
        # -------------------------------------------------

        with st.spinner(
            "🤖 Generating AI explanation..."
        ):

            explanation = explain_career_recommendation(
                profile,
                career_scores
            )


        st.subheader(
            "💬 AI Career Analysis"
        )

        st.write(
            explanation
        )


        st.divider()


        # -------------------------------------------------
        # ORIGINAL DESCRIPTION
        # -------------------------------------------------

        with st.expander(
            "📝 View Your Original Description"
        ):

            st.write(
                student_input
            )


        # -------------------------------------------------
        # COMPLETION MESSAGE
        # -------------------------------------------------

        st.success(
            "Career analysis completed successfully! ✅"
        )