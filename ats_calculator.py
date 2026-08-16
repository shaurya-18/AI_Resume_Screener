from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_ats_score(resume, jd, resume_skills, jd_skills):

    # 1. TF-IDF text similarity
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([
        str(resume),
        str(jd)
    ])

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )

    tfidf_score = similarity[0][0] * 100

    # 2. Skill matching
    if len(jd_skills) == 0:
        skill_score = 0
    else:
        matched_skills = set(resume_skills).intersection(
            set(jd_skills)
        )

        skill_score = (
            len(matched_skills) / len(set(jd_skills))
        ) * 100

    # 3. Hybrid ATS score
    final_score = (
        (tfidf_score * 0.60) +
        (skill_score * 0.40)
    )

    return round(final_score, 2)