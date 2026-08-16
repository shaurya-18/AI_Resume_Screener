def get_missing_skills(
        resume_skills,
        jd_skills):

    missing = []

    for skill in jd_skills:

        if skill not in resume_skills:

            missing.append(skill)

    return missing


def get_suggestions(missing):

    suggestions = []

    for skill in missing:

        suggestions.append(
            f"Add projects or certifications related to {skill}"
        )

    return suggestions