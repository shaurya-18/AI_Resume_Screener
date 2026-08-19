import streamlit as st

from groq import Groq

from resume_parser import extract_text

from skill_extractor import extract_skills

from ats_calculator import calculate_ats_score

from recommendation import (
    get_missing_skills,
    get_suggestions
)

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)
st.write(client.models.list())
def generate_ai_analysis(resume_text, job_description, ats_score, missing_skills):

    missing = ", ".join(missing_skills) if missing_skills else "None"

    prompt = f"""
You are an expert ATS resume reviewer and technical recruiter.

Your task is to analyze a candidate's resume against a job description.

================ RESUME ================
{resume_text}

================ JOB DESCRIPTION ================
{job_description}

================ ATS SCORE ================
{ats_score:.2f}%

================ MISSING SKILLS ================
{missing}

================ IMPORTANT RULES ================

1. Only make claims that are directly supported by the resume or job description.

2. NEVER assume that the candidate lacks something just because it is not mentioned in the resume.
   For example, do NOT say:
   "The candidate lacks professional experience"
   unless the resume explicitly provides evidence for that conclusion.

3. Clearly distinguish between:
   - Skills explicitly present in the resume
   - Skills explicitly required by the job description
   - Skills identified as missing by the ATS system

4. Do NOT recommend adding a skill if that skill is already present in the resume.
   Instead, recommend demonstrating that skill more strongly through projects,
   achievements, or measurable results.

5. Do NOT invent:
   - Work experience
   - Internships
   - Projects
   - Certifications
   - Skills
   - Technologies
   - Achievements

6. If a skill is missing, explain why it may matter for this particular job.

7. Recommendations must be practical and specific to the provided job description.

8. Do not repeat the same recommendation in multiple sections.

9. NEVER invent numerical metrics, percentages, performance improvements,
   user counts, request rates, response times, or other quantitative results.

10. Do not suggest fake resume statements such as:
    "Improved performance by 30%"
    "Handled 1000 requests per minute"
    "Reduced processing time by 40%"

11. If a project achievement would be stronger with a measurable result,
    say:
    "Add a real measurable result if you have one."
    Do not create the number yourself.

12. Do not claim that the candidate implemented REST APIs,
    PostgreSQL systems, backend services, or other technologies
    unless the resume explicitly describes that implementation.

13. A technology appearing in the Technical Skills section means
    the candidate has listed that skill, but it does not prove
    professional or project experience with that technology.

14. Do not infer the absence of experience from the absence of an
    Experience section. Instead say that the resume does not provide
    evidence about that area.
================ OUTPUT FORMAT ================

### Overall Assessment
Give a concise assessment of how well the resume aligns with the job.

### Why This ATS Score?
Explain the main factors affecting the ATS score based on the resume and job description.

### Missing Skills
List only the skills identified as missing by the ATS system.
If there are none, say:
"No major missing skills were identified by the current skill-matching system."

### Resume Strengths
Mention only strengths that are clearly supported by the resume.

### Resume Weaknesses
Mention areas where the resume could be stronger for this specific job.
Do not treat missing information as proof that the candidate does not have that experience.

### Recommended Improvements
Give practical recommendations for improving alignment with this job.
If a required skill already exists in the resume, explain how the candidate can demonstrate it better instead of telling them to add it.

### Top 5 Changes
Give exactly five prioritized and actionable changes.
Do not invent experience or skills.
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are an expert resume and ATS analyzer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=1500
    )

    return response.choices[0].message.content

st.set_page_config(
    page_title="AI Resume Screener"
)

st.title("AI Resume Screening System")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description"
)

if uploaded_file and job_description:

    resume_text = extract_text(
        uploaded_file
    )
    
    resume_skills = extract_skills(
        resume_text
    )

    jd_skills = extract_skills(
        job_description
    )

    ats = calculate_ats_score(
        resume_text,
        job_description,
        resume_skills,
        jd_skills
    )
    
    st.write("ATS Value:", ats)

    missing = get_missing_skills(
        resume_skills,
        jd_skills
    )

    suggestions = get_suggestions(
        missing
    )

    st.metric(
    label="ATS Score",
    value=f"{ats}%"
    )
    
    st.subheader(
        "Resume Skills"
    )

    st.write(
        resume_skills
    )

    st.subheader(
        "Required Skills"
    )

    st.write(
        jd_skills
    )

    st.subheader(
        "Missing Skills"
    )

    st.write(
        missing
    )

    st.subheader(
    "AI Resume Analysis"
    )

    if st.button("Generate AI Analysis"):

        with st.spinner("AI is analyzing your resume..."):

            try:

                ai_analysis = generate_ai_analysis(
                    resume_text,
                    job_description,
                    ats,
                    missing
                )

                st.markdown(ai_analysis)

            except Exception as e:

                st.error(
                    f"AI analysis failed: {e}"
            )

    st.subheader(
        "Suggestions"
    )

    for s in suggestions:

        st.write(
            "- " + s
        )
