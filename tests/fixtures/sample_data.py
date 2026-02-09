"""Test fixtures and sample data."""

SAMPLE_RESUME_TEXT = """
John Doe
john.doe@email.com
(555) 123-4567

SUMMARY
Senior Software Engineer with 5+ years of experience in Python and JavaScript.
Expert in web development using React and Django frameworks.

EXPERIENCE
Senior Developer, Tech Corp (2020-Present)
- Led development of ML pipeline using Python and TensorFlow
- Built REST APIs with Django and Flask
- Deployed applications on AWS using Docker

Software Engineer, StartupXYZ (2017-2020)
- Full-stack development with React and Node.js
- Implemented machine learning features

EDUCATION
Master of Science in Computer Science
University of Technology, 2017

SKILLS
Python, JavaScript, React, Django, TensorFlow, AWS, Docker, Git, Machine Learning
"""

SAMPLE_JOB_DESCRIPTION = """
Senior Software Engineer - AI/ML

We are looking for an experienced Software Engineer to join our AI team.

Requirements:
- 5+ years of experience in Python
- Experience with machine learning frameworks (TensorFlow, PyTorch)
- Strong knowledge of AWS and cloud infrastructure
- Experience with Docker and Kubernetes
- Bachelor's degree in Computer Science or related field

Nice to have:
- Experience with React or Vue.js
- Knowledge of NLP or computer vision
"""

SAMPLE_REQUIRED_SKILLS = [
    {'skill_name': 'Python', 'importance': 'critical'},
    {'skill_name': 'TensorFlow', 'importance': 'critical'},
    {'skill_name': 'AWS', 'importance': 'critical'},
    {'skill_name': 'Docker', 'importance': 'preferred'},
    {'skill_name': 'Kubernetes', 'importance': 'preferred'},
    {'skill_name': 'React', 'importance': 'nice-to-have'},
]
