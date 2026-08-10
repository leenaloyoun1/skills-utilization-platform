from app.services.skill_extractor import extract_skills


def main() -> None:
    test_sentences = [
        "I am skilled in Python and SQL and have experience in backend development.",
        "I am interested in ML, NLP, REST APIs, and version control.",
        "I enjoy reading and drawing.",
        "",
    ]

    for sentence in test_sentences:
        skills = extract_skills(sentence)

        print(f"Input: {sentence}")
        print(f"Extracted skills: {skills}")
        print("-" * 50)


if __name__ == "__main__":
    main()