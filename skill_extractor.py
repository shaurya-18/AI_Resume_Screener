import pandas as pd
from pathlib import Path

SKILL_ALIASES = {
    "css": "CSS",
    "dsa": "DSA",
    "git": "Git",
    "github": "GitHub",
    "html": "HTML",
    "java": "Java",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "mongodb": "MongoDB",
    "mysql": "MySQL",
    "nlp": "NLP",
    "numpy": "NumPy",
    "pandas": "Pandas",
    "python": "Python",
    "rest api": "REST API",
    "rest apis": "REST API",
    "sql": "SQL",
    "streamlit": "Streamlit",
    "system design": "System Design",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "spring": "Spring",
    "spring boot": "Spring Boot",
    "hibernate": "Hibernate",
    "jpa": "JPA",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "microservices": "Microservices",
    "ci/cd": "CI/CD",
    "jenkins": "Jenkins",
    "gitlab": "GitLab",
    "postman": "Postman",
    "redis": "Redis",
    "kafka": "Kafka",
    "linux": "Linux",
    "maven": "Maven",
    "gradle": "Gradle",
    "junit": "JUnit",
    "mockito": "Mockito",
    "spring security": "Spring Security",
    "jwt": "JWT",
    "terraform": "Terraform",
    "prometheus": "Prometheus",
    "grafana": "Grafana",
    "aws lambda": "AWS Lambda",
    "cloud architecture": "Cloud Architecture",
    "distributed systems": "Distributed Systems",
    "infrastructure as code": "Infrastructure as Code",
    "observability": "Observability",
    "github actions": "GitHub Actions",
    "scikit-learn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "sklearn": "Scikit-learn",
}


def normalize_skill(skill):
    skill = skill.strip().lower()

    return SKILL_ALIASES.get(
        skill,
        skill
    )


def extract_skills(text):

    text = text.lower()

    skills_file = Path(__file__).parent / "data" / "skills.csv"

    df = pd.read_csv(skills_file)

    skills = set()

    for skill in df["skill"]:

        normalized = normalize_skill(skill)

        if skill.lower() in text:
            skills.add(normalized)

    return sorted(skills)