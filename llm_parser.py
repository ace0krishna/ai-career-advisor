import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


if not os.getenv("GEMINI_API_KEY"):
    raise ValueError(
        "GEMINI_API_KEY not found. Check your .env file."
    )


# ---------------------------------------------------------
# STRUCTURED STUDENT PROFILE
# ---------------------------------------------------------

class StudentProfile(BaseModel):

    coding: int = Field(
        ge=0,
        le=10,
        description="Coding/programming skill from 0 to 10"
    )

    mathematics: int = Field(
        ge=0,
        le=10,
        description="Mathematics skill from 0 to 10"
    )

    logical_thinking: int = Field(
        ge=0,
        le=10,
        description="Logical thinking and problem-solving ability from 0 to 10"
    )

    creativity: int = Field(
        ge=0,
        le=10,
        description="Creativity from 0 to 10"
    )

    communication: int = Field(
        ge=0,
        le=10,
        description="Communication ability from 0 to 10"
    )

    technology_interest: int = Field(
        ge=0,
        le=10,
        description="Interest in technology from 0 to 10"
    )


# ---------------------------------------------------------
# GEMINI MODEL
# ---------------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    timeout=60,
    max_retries=1
)


# ---------------------------------------------------------
# STRUCTURED OUTPUT
# ---------------------------------------------------------

structured_llm = llm.with_structured_output(
    StudentProfile,
    method="json_schema"
)


# ---------------------------------------------------------
# EXTRACT STUDENT PROFILE
# ---------------------------------------------------------

def extract_student_profile(student_text):

    prompt = f"""
You are an AI career advisor.

Analyze the student's description and estimate six
career-related characteristics.

Give every score as an integer from 0 to 10.

Scoring guide:

CODING
0 = no coding experience
10 = excellent programming ability

MATHEMATICS
0 = very weak mathematics
10 = excellent mathematics

LOGICAL THINKING
0 = very weak logical/problem solving ability
10 = excellent logical/problem solving ability

CREATIVITY
0 = very low creativity
10 = very high creativity

COMMUNICATION
0 = very weak communication
10 = excellent communication

TECHNOLOGY INTEREST
0 = no interest in technology
10 = extremely interested in technology

Important:
- Use the student's actual description.
- Do not assume everything is high.
- Give reasonable estimates.
- Return only the structured profile.

STUDENT DESCRIPTION:

{student_text}
"""

    result = structured_llm.invoke(prompt)

    return result.model_dump()


# ---------------------------------------------------------
# AI CAREER EXPLANATION
# ---------------------------------------------------------

def explain_career_recommendation(
    profile,
    career_scores
):

    prompt = f"""
You are an AI career advisor.

A student's skills were extracted from natural language
and then evaluated using a fuzzy logic career suitability
system.

Student profile:

Coding: {profile['coding']}/10
Mathematics: {profile['mathematics']}/10
Logical Thinking: {profile['logical_thinking']}/10
Creativity: {profile['creativity']}/10
Communication: {profile['communication']}/10
Technology Interest: {profile['technology_interest']}/10

Fuzzy logic career suitability scores:

{career_scores}

Explain the results in simple language.

Your explanation must:

1. Identify the career with the highest suitability score.
2. Explain which student strengths support that career.
3. Briefly explain the other career scores.
4. Mention one or two skills the student could improve.
5. Do not claim that the result guarantees a successful career.
6. Keep the explanation between 150 and 250 words.

Write the response with clear paragraphs and bullet points
where useful.
"""

    response = llm.invoke(prompt)

    return response.content


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    test_text = """
    I love coding and mathematics.
    I enjoy solving logical problems.
    I am very interested in artificial intelligence
    and technology.
    """

    profile = extract_student_profile(test_text)

    print()
    print("=" * 50)
    print("AI CAREER ADVISOR - LLM TEST")
    print("=" * 50)

    for key, value in profile.items():
        print(f"{key}: {value}")

    print("=" * 50)