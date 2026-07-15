import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure GenAI if key is present
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def clean_json_response(text: str) -> dict:
    """
    Cleans markdown formatting and parses the JSON response.
    """
    # Remove markdown code block fences if present
    cleaned = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)
    return json.loads(cleaned.strip())

def generate_mock_analysis(resume_text: str, job_description: str = "") -> dict:
    """
    Generates a highly realistic mock analysis by scanning the resume text for keywords
    to customize the output. This serves as a fail-safe fallback when no API key is set.
    """
    # Basic keyword matching to detect industry/role
    resume_lower = resume_text.lower()
    jd_lower = job_description.lower() if job_description else ""
    
    # Simple role detection
    role = "Software Engineer"
    skills_pool = ["React", "Python", "JavaScript", "SQL", "Git", "REST APIs", "Node.js", "Docker", "AWS", "CSS"]
    
    if "data scientist" in resume_lower or "machine learning" in resume_lower or "pandas" in resume_lower:
        role = "Data Scientist"
        skills_pool = ["Python", "Pandas", "NumPy", "Scikit-Learn", "SQL", "Machine Learning", "Data Visualization", "TensorFlow", "R", "Git"]
    elif "product manager" in resume_lower or "agile" in resume_lower or "roadmap" in resume_lower:
        role = "Product Manager"
        skills_pool = ["Product Strategy", "Agile Roadmap", "Scrum", "Data Analytics", "User Research", "Jira", "A/B Testing", "KPI Tracking", "SQL"]
    elif "marketing" in resume_lower or "seo" in resume_lower or "social media" in resume_lower:
        role = "Marketing Manager"
        skills_pool = ["SEO", "Google Analytics", "Content Strategy", "Copywriting", "Email Campaigns", "Social Media", "A/B Testing", "PPC", "CRM"]

    # Analyze matching and missing keywords
    found_skills = [s for s in skills_pool if s.lower() in resume_lower]
    
    # If job description is provided, scan it for skills in our pool to see which are missing
    if job_description:
        jd_skills = [s for s in skills_pool if s.lower() in jd_lower]
        missing_skills = [s for s in jd_skills if s not in found_skills]
        if not missing_skills and jd_skills:
            # Add some filler missing skills if everything matches, for demonstration purposes
            missing_skills = [s for s in skills_pool if s not in found_skills][:2]
    else:
        # Default missing skills
        missing_skills = [s for s in skills_pool if s not in found_skills][:3]
        jd_skills = found_skills + missing_skills

    # Match percentage computation
    total_jd = len(jd_skills) if jd_skills else len(skills_pool)
    matching_count = len(found_skills)
    match_ratio = (matching_count / total_jd) if total_jd > 0 else 0.7
    
    score = int(55 + (match_ratio * 40))  # Range: 55 to 95
    score = min(max(score, 45), 98)

    # Dynamic recommendation list
    recommended = [s for s in skills_pool if s not in found_skills and s not in missing_skills][:3]
    if not recommended:
        recommended = ["System Design", "Microservices", "CI/CD Platforms"]

    # Extract name if possible
    name_match = re.search(r"^[A-Z][a-z]+ [A-Z][a-z]+", resume_text)
    candidate_name = name_match.group(0) if name_match else "Candidate"

    # Build section-by-section breakdown based on detected content
    section_breakdown = _build_mock_section_breakdown(resume_lower, score)
    
    # Build skill roadmap for missing + recommended skills
    all_gap_skills = list(set(missing_skills + recommended))
    skill_roadmap = _build_mock_skill_roadmap(all_gap_skills)

    # Build cover letter
    cover_letter = _build_mock_cover_letter(candidate_name, role, found_skills, missing_skills, job_description)

    # Assemble structured response
    mock_data = {
      "score": score,
      "summary": f"The resume for {candidate_name} exhibits strong alignment for a {role} role, demonstrating good foundational knowledge in key technologies. However, there are gaps in specific advanced skills, tool alignment, and quantifiable metrics in description headers that can be improved.",
      "key_metrics": {
        "impact": {
          "score": int(score * 0.9),
          "label": "Impact & Results",
          "description": "Action verbs, metrics, results"
        },
        "formatting": {
          "score": 88,
          "label": "Formatting & Structure",
          "description": "Structure, readability, design"
        },
        "keywords": {
          "score": int(match_ratio * 100),
          "label": "Keyword Match",
          "description": "Matching job description skills"
        }
      },
      "keywords": {
        "matching": found_skills if found_skills else ["Python", "Git", "SQL"],
        "missing": missing_skills if missing_skills else ["Docker", "Kubernetes", "AWS Cloud"],
        "recommended": recommended
      },
      "feedback": [
        {
          "category": "Impact and Achievements",
          "score": int(score * 0.88),
          "status": "warning" if score < 75 else "good",
          "message": "Many bullet points focus heavily on duties rather than outcomes and measurable metrics.",
          "details": [
            "Add quantitative results (e.g., '% improvement', '$ savings', 'hours saved') for your projects.",
            "Begin bullets with strong action verbs (e.g., 'Spearheaded', 'Optimized', 'Redesigned') instead of passive phrasing like 'Responsible for'."
          ]
        },
        {
          "category": "Keywords & ATS Optimization",
          "score": int(match_ratio * 100),
          "status": "critical" if len(missing_skills) > 4 else ("warning" if missing_skills else "excellent"),
          "message": f"Resume is missing some critical keywords from the job description.",
          "details": [
            f"Integrate missing core skills like {', '.join(missing_skills[:3])} directly into your experience statements.",
            "Use standard terminology that matches industry norms to satisfy parsing filters."
          ]
        },
        {
          "category": "Structure & Formatting",
          "score": 90,
          "status": "excellent",
          "message": "The resume layout has clear sections and reads naturally.",
          "details": [
            "Ensure standard headings are used (e.g., 'Work Experience', 'Skills', 'Education').",
            "Keep formatting, date notations, and bullet styling consistent throughout."
          ]
        }
      ],
      "bullet_optimizations": [
        {
          "original": "Responsible for writing backend code in Python and handling database updates.",
          "optimized": "Engineered RESTful API endpoints in FastAPI/Python and optimized database queries, reducing data retrieval latency by 42%.",
          "explanation": "Changed passive duties to action-driven engineering outcomes and added a quantifiable performance metric."
        },
        {
          "original": "Worked on React components for our client web application.",
          "optimized": "Spearheaded design and migration of key legacy pages to React functional components, reducing frontend bundle size by 18% and enhancing UX responsiveness.",
          "explanation": "Highlighted leadership/initiative and specified technical accomplishments instead of generic task statements."
        }
      ],
      "career_recommendations": [
        f"Build a portfolio project demonstrating hands-on experience with {', '.join(missing_skills[:2])}.",
        "Include a dedicated, categorized 'Skills' section near the top of the resume for faster indexing.",
        "Obtain relevant industry certifications (e.g., AWS Certified Developer, React Professional) to validate skills."
      ],
      "section_breakdown": section_breakdown,
      "skill_roadmap": skill_roadmap,
      "cover_letter": cover_letter
    }
    
    return mock_data

def _build_mock_cover_letter(candidate_name: str, role: str, found_skills: list, missing_skills: list, job_description: str = "") -> dict:
    """
    Generates a context-aware mock cover letter using the detected candidate info.
    """
    top_skills = ', '.join(found_skills[:4]) if found_skills else 'Python, JavaScript, and SQL'
    growth_skills = ', '.join(missing_skills[:2]) if missing_skills else 'advanced cloud technologies'
    
    has_jd = bool(job_description and job_description.strip())
    
    if has_jd:
        opening = (
            f"I am writing to express my strong interest in the {role} position at your organization. "
            f"After carefully reviewing the job description, I am confident that my technical background "
            f"and professional experience make me an excellent fit for this role. With a solid foundation in "
            f"{top_skills}, I am eager to contribute to your team's success and drive meaningful impact."
        )
    else:
        opening = (
            f"I am writing to express my enthusiasm for {role} opportunities that align with my "
            f"technical expertise and career aspirations. With hands-on experience in {top_skills}, "
            f"I am confident in my ability to deliver high-quality results and make a meaningful contribution "
            f"to a forward-thinking engineering team."
        )
    
    body = (
        f"Throughout my career, I have developed a deep proficiency in {top_skills}, which I have applied "
        f"to build scalable applications, optimize system performance, and deliver user-centric solutions. "
        f"I have a proven track record of translating complex business requirements into clean, maintainable code "
        f"and collaborating effectively with cross-functional teams to ship products on time. My experience "
        f"includes designing RESTful APIs, implementing responsive user interfaces, and working within Agile "
        f"development frameworks to iteratively improve product quality."
    )
    
    closing = (
        f"I am particularly excited about the opportunity to grow my expertise in {growth_skills} "
        f"and contribute to innovative projects that push the boundaries of what's possible. "
        f"I am a fast learner who thrives in dynamic environments, and I am committed to continuous "
        f"professional development. I would welcome the opportunity to discuss how my skills and "
        f"enthusiasm can add value to your team. Thank you for considering my application."
    )
    
    return {
        "greeting": "Dear Hiring Manager,",
        "opening": opening,
        "body": body,
        "closing": closing,
        "sign_off": f"Sincerely,\n{candidate_name}"
    }


def _build_mock_section_breakdown(resume_lower: str, overall_score: int) -> list:
    """
    Generates a realistic section-by-section breakdown by scanning resume text
    for section indicators and assigning context-aware scores.
    """
    sections = []

    # Summary / Objective section
    has_summary = any(kw in resume_lower for kw in ["summary", "objective", "profile", "about me"])
    if has_summary:
        sections.append({
            "section_name": "Professional Summary",
            "score": min(overall_score + 5, 95),
            "status": "good" if overall_score >= 65 else "warning",
            "verdict": "Your professional summary is present and provides a reasonable overview of your background.",
            "strengths": [
                "Summary section is present and positioned at the top",
                "Provides a high-level overview of professional identity"
            ],
            "improvements": [
                "Tailor the summary to each specific job description you apply to",
                "Include 2-3 quantifiable achievements in the summary itself",
                "Keep it under 3 concise sentences for optimal ATS scanning"
            ]
        })
    else:
        sections.append({
            "section_name": "Professional Summary",
            "score": 35,
            "status": "critical",
            "verdict": "No professional summary or objective section was detected in your resume.",
            "strengths": [],
            "improvements": [
                "Add a 2-3 sentence professional summary at the top of your resume",
                "Include your target role, years of experience, and top 2-3 skills",
                "This section is the first thing recruiters and ATS systems scan"
            ]
        })

    # Work Experience section
    has_experience = any(kw in resume_lower for kw in ["experience", "work history", "employment", "professional experience"])
    has_metrics = any(c in resume_lower for c in ["%", "percent", "increased", "decreased", "reduced", "improved", "saved"])
    has_action_verbs = any(kw in resume_lower for kw in ["spearheaded", "engineered", "architected", "optimized", "led", "delivered", "launched"])
    
    exp_score = overall_score - 5 if has_experience else 30
    if has_metrics:
        exp_score = min(exp_score + 8, 95)
    if has_action_verbs:
        exp_score = min(exp_score + 5, 95)
    
    exp_strengths = []
    exp_improvements = []
    if has_experience:
        exp_strengths.append("Work experience section is clearly labeled and present")
    if has_action_verbs:
        exp_strengths.append("Uses strong action verbs to describe accomplishments")
    if has_metrics:
        exp_strengths.append("Includes some quantifiable metrics and results")
    
    if not has_metrics:
        exp_improvements.append("Add quantifiable metrics (%, $, hours saved) to at least 60% of bullet points")
    if not has_action_verbs:
        exp_improvements.append("Begin each bullet with a strong action verb (Engineered, Spearheaded, Optimized)")
    exp_improvements.append("Use the Google XYZ formula: Accomplished [X] as measured by [Y], by doing [Z]")
    if not has_experience:
        exp_improvements.append("Add a clearly labeled 'Work Experience' section with reverse-chronological entries")

    sections.append({
        "section_name": "Work Experience",
        "score": exp_score,
        "status": "excellent" if exp_score >= 85 else ("good" if exp_score >= 70 else ("warning" if exp_score >= 50 else "critical")),
        "verdict": "Experience section shows relevant roles but could benefit from stronger impact statements." if has_experience else "No work experience section detected.",
        "strengths": exp_strengths if exp_strengths else ["Resume includes job-related content"],
        "improvements": exp_improvements
    })

    # Skills section
    has_skills = any(kw in resume_lower for kw in ["skills", "technologies", "tech stack", "competencies", "proficiencies"])
    skills_score = min(overall_score + 3, 92) if has_skills else 40
    
    sections.append({
        "section_name": "Skills & Technologies",
        "score": skills_score,
        "status": "good" if skills_score >= 70 else ("warning" if skills_score >= 50 else "critical"),
        "verdict": "Skills section is present and lists relevant technologies." if has_skills else "No dedicated skills section found.",
        "strengths": [
            "Dedicated skills section helps ATS keyword matching",
            "Technical skills are listed for quick scanning"
        ] if has_skills else [],
        "improvements": [
            "Categorize skills by type (Languages, Frameworks, Tools, Databases)",
            "Remove outdated or irrelevant skills that dilute your profile",
            "Ensure skills match the exact terminology used in target job descriptions"
        ] if has_skills else [
            "Add a dedicated 'Skills' section near the top of your resume",
            "List 10-15 relevant technical skills categorized by type",
            "Mirror the exact skill names from job descriptions for ATS matching"
        ]
    })

    # Education section
    has_education = any(kw in resume_lower for kw in ["education", "university", "bachelor", "master", "degree", "b.tech", "b.e.", "m.tech", "mba", "college"])
    has_gpa = any(kw in resume_lower for kw in ["gpa", "cgpa", "percentage", "grade", "distinction", "honors", "cum laude"])
    edu_score = 85 if has_education else 30
    if has_gpa:
        edu_score = min(edu_score + 5, 95)

    sections.append({
        "section_name": "Education",
        "score": edu_score,
        "status": "excellent" if edu_score >= 85 else ("good" if edu_score >= 70 else "critical"),
        "verdict": "Education section is well-structured with degree information." if has_education else "Education section not detected.",
        "strengths": [
            "Education credentials are clearly listed",
            "Includes GPA/academic performance" if has_gpa else "Degree and institution are mentioned"
        ] if has_education else [],
        "improvements": [
            "Include relevant coursework aligned with target roles" if has_education else "Add a clearly labeled Education section",
            "Add academic projects, thesis work, or research that demonstrates applied skills",
            "Include graduation year and institution location for completeness"
        ]
    })

    # Projects section
    has_projects = any(kw in resume_lower for kw in ["project", "projects", "portfolio", "personal project", "side project", "capstone"])
    proj_score = min(overall_score + 2, 88) if has_projects else 25

    sections.append({
        "section_name": "Projects & Portfolio",
        "score": proj_score,
        "status": "good" if proj_score >= 70 else ("warning" if proj_score >= 45 else "critical"),
        "verdict": "Projects section demonstrates hands-on technical experience." if has_projects else "No projects section found — this is a significant gap.",
        "strengths": [
            "Projects section demonstrates initiative and hands-on skills",
            "Shows ability to build real-world applications"
        ] if has_projects else [],
        "improvements": [
            "Include GitHub links or live demo URLs for each project",
            "Describe the tech stack, your specific contribution, and measurable impact",
            "Prioritize projects that align with your target role's requirements"
        ] if has_projects else [
            "Add 2-3 relevant projects that demonstrate your technical skills",
            "Include project descriptions with tech stack, your role, and outcomes",
            "Link to GitHub repositories or live demos wherever possible"
        ]
    })

    return sections


# Static roadmap data for common skills with real, free learning resources
_SKILL_ROADMAP_DB = {
    "react": {
        "skill_name": "React",
        "priority": "high",
        "estimated_weeks": 4,
        "why_important": "Most in-demand frontend library, required in 70%+ of frontend job listings",
        "learning_path": [
            {"step": 1, "title": "React Official Tutorial", "type": "course", "resource": "React.dev", "url": "https://react.dev/learn", "duration": "1 week"},
            {"step": 2, "title": "Build a Todo App with Hooks", "type": "project", "resource": "Hands-on practice", "url": "", "duration": "3 days"},
            {"step": 3, "title": "React with TypeScript", "type": "course", "resource": "FreeCodeCamp", "url": "https://www.freecodecamp.org/news/how-to-use-typescript-with-react/", "duration": "1 week"},
            {"step": 4, "title": "Build a Full-Stack App", "type": "project", "resource": "Portfolio project", "url": "", "duration": "1.5 weeks"}
        ],
        "certifications": ["Meta Front-End Developer (Coursera)", "HackerRank React Certificate"]
    },
    "docker": {
        "skill_name": "Docker",
        "priority": "high",
        "estimated_weeks": 3,
        "why_important": "Essential for containerized deployments, required in 85% of DevOps and backend roles",
        "learning_path": [
            {"step": 1, "title": "Docker Getting Started Guide", "type": "course", "resource": "Docker Official Docs", "url": "https://docs.docker.com/get-started/", "duration": "4 days"},
            {"step": 2, "title": "Containerize a Web App", "type": "project", "resource": "Hands-on practice", "url": "", "duration": "3 days"},
            {"step": 3, "title": "Docker Compose & Multi-Container Apps", "type": "course", "resource": "TechWorld with Nana (YouTube)", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE", "duration": "1 week"},
            {"step": 4, "title": "Deploy with Docker on a Cloud Platform", "type": "project", "resource": "Portfolio project", "url": "", "duration": "1 week"}
        ],
        "certifications": ["Docker Certified Associate (DCA)"]
    },
    "aws": {
        "skill_name": "AWS",
        "priority": "high",
        "estimated_weeks": 6,
        "why_important": "Leading cloud platform with 32% market share, highly valued across all engineering roles",
        "learning_path": [
            {"step": 1, "title": "AWS Cloud Practitioner Essentials", "type": "course", "resource": "AWS Skill Builder (Free)", "url": "https://explore.skillbuilder.aws/learn/course/external/view/elearning/134/aws-cloud-practitioner-essentials", "duration": "1 week"},
            {"step": 2, "title": "Deploy a Static Website on S3", "type": "project", "resource": "Hands-on practice", "url": "", "duration": "2 days"},
            {"step": 3, "title": "AWS Solutions Architect Basics", "type": "course", "resource": "FreeCodeCamp YouTube", "url": "https://www.youtube.com/watch?v=Ia-UEYYR44s", "duration": "2 weeks"},
            {"step": 4, "title": "Build a Serverless API with Lambda + DynamoDB", "type": "project", "resource": "Portfolio project", "url": "", "duration": "2 weeks"}
        ],
        "certifications": ["AWS Certified Cloud Practitioner", "AWS Certified Solutions Architect – Associate"]
    },
    "python": {
        "skill_name": "Python",
        "priority": "high",
        "estimated_weeks": 4,
        "why_important": "Most versatile programming language, used in web dev, data science, AI/ML, and automation",
        "learning_path": [
            {"step": 1, "title": "Python for Everybody", "type": "course", "resource": "FreeCodeCamp", "url": "https://www.freecodecamp.org/learn/scientific-computing-with-python/", "duration": "1.5 weeks"},
            {"step": 2, "title": "Build a CLI Tool or Web Scraper", "type": "project", "resource": "Hands-on practice", "url": "", "duration": "4 days"},
            {"step": 3, "title": "FastAPI / Flask Web Framework", "type": "course", "resource": "FastAPI Official Tutorial", "url": "https://fastapi.tiangolo.com/tutorial/", "duration": "1 week"},
            {"step": 4, "title": "Build a REST API with Database", "type": "project", "resource": "Portfolio project", "url": "", "duration": "1 week"}
        ],
        "certifications": ["PCEP – Certified Entry-Level Python Programmer", "Google IT Automation with Python (Coursera)"]
    },
    "sql": {
        "skill_name": "SQL",
        "priority": "medium",
        "estimated_weeks": 3,
        "why_important": "Fundamental database skill required across virtually all software engineering roles",
        "learning_path": [
            {"step": 1, "title": "SQL Fundamentals", "type": "course", "resource": "SQLBolt (Interactive)", "url": "https://sqlbolt.com/", "duration": "4 days"},
            {"step": 2, "title": "Practice SQL Challenges", "type": "project", "resource": "LeetCode SQL 50", "url": "https://leetcode.com/studyplan/top-sql-50/", "duration": "1 week"},
            {"step": 3, "title": "Advanced Queries & Optimization", "type": "course", "resource": "Mode SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "duration": "1 week"}
        ],
        "certifications": ["HackerRank SQL Certificate", "Oracle Database SQL Certified Associate"]
    },
    "kubernetes": {
        "skill_name": "Kubernetes",
        "priority": "medium",
        "estimated_weeks": 5,
        "why_important": "Industry standard for container orchestration, critical for DevOps and platform engineering",
        "learning_path": [
            {"step": 1, "title": "Kubernetes Basics", "type": "course", "resource": "Kubernetes.io Interactive", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/", "duration": "1 week"},
            {"step": 2, "title": "Deploy an App on Minikube", "type": "project", "resource": "Hands-on practice", "url": "", "duration": "4 days"},
            {"step": 3, "title": "Kubernetes Deep Dive", "type": "course", "resource": "TechWorld with Nana (YouTube)", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "duration": "2 weeks"},
            {"step": 4, "title": "Build a Multi-Service App on K8s", "type": "project", "resource": "Portfolio project", "url": "", "duration": "1.5 weeks"}
        ],
        "certifications": ["Certified Kubernetes Application Developer (CKAD)", "Certified Kubernetes Administrator (CKA)"]
    },
    "node.js": {
        "skill_name": "Node.js",
        "priority": "medium",
        "estimated_weeks": 3,
        "why_important": "Server-side JavaScript runtime, enabling full-stack development with a single language",
        "learning_path": [
            {"step": 1, "title": "Node.js Introduction", "type": "course", "resource": "The Odin Project", "url": "https://www.theodinproject.com/paths/full-stack-javascript/courses/nodejs", "duration": "1 week"},
            {"step": 2, "title": "Build a REST API with Express", "type": "project", "resource": "Hands-on practice", "url": "", "duration": "4 days"},
            {"step": 3, "title": "Authentication & Database Integration", "type": "course", "resource": "FreeCodeCamp", "url": "https://www.freecodecamp.org/learn/back-end-development-and-apis/", "duration": "1 week"}
        ],
        "certifications": ["OpenJS Node.js Application Developer (JSNAD)"]
    },
    "git": {
        "skill_name": "Git",
        "priority": "high",
        "estimated_weeks": 1,
        "why_important": "Universal version control system, required for all collaborative software development",
        "learning_path": [
            {"step": 1, "title": "Git & GitHub Crash Course", "type": "course", "resource": "FreeCodeCamp YouTube", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk", "duration": "2 days"},
            {"step": 2, "title": "Interactive Git Branching", "type": "project", "resource": "Learn Git Branching", "url": "https://learngitbranching.js.org/", "duration": "2 days"},
            {"step": 3, "title": "Contribute to an Open Source Project", "type": "project", "resource": "First Contributions", "url": "https://firstcontributions.github.io/", "duration": "3 days"}
        ],
        "certifications": []
    },
    "rest apis": {
        "skill_name": "REST APIs",
        "priority": "high",
        "estimated_weeks": 2,
        "why_important": "Standard communication pattern for modern web services, fundamental to backend roles",
        "learning_path": [
            {"step": 1, "title": "RESTful API Design Principles", "type": "course", "resource": "RESTful API Tutorial", "url": "https://restfulapi.net/", "duration": "3 days"},
            {"step": 2, "title": "Build a CRUD API", "type": "project", "resource": "Hands-on practice", "url": "", "duration": "4 days"},
            {"step": 3, "title": "API Testing with Postman", "type": "course", "resource": "Postman Learning Center", "url": "https://learning.postman.com/", "duration": "3 days"}
        ],
        "certifications": ["Postman API Fundamentals Student Expert"]
    },
    "css": {
        "skill_name": "CSS",
        "priority": "medium",
        "estimated_weeks": 3,
        "why_important": "Essential for building responsive, visually polished web interfaces",
        "learning_path": [
            {"step": 1, "title": "CSS Fundamentals & Flexbox", "type": "course", "resource": "FreeCodeCamp", "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "duration": "1 week"},
            {"step": 2, "title": "CSS Grid & Responsive Design", "type": "course", "resource": "CSS-Tricks Guide", "url": "https://css-tricks.com/snippets/css/complete-guide-grid/", "duration": "4 days"},
            {"step": 3, "title": "Build a Responsive Portfolio Site", "type": "project", "resource": "Portfolio project", "url": "", "duration": "1 week"}
        ],
        "certifications": ["FreeCodeCamp Responsive Web Design Certification"]
    },
    "javascript": {
        "skill_name": "JavaScript",
        "priority": "high",
        "estimated_weeks": 4,
        "why_important": "The language of the web, essential for frontend and increasingly important for full-stack roles",
        "learning_path": [
            {"step": 1, "title": "JavaScript Algorithms & Data Structures", "type": "course", "resource": "FreeCodeCamp", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures-v8/", "duration": "2 weeks"},
            {"step": 2, "title": "Build Interactive Web Projects", "type": "project", "resource": "Hands-on practice", "url": "", "duration": "1 week"},
            {"step": 3, "title": "Modern JS (ES6+, Async/Await, Modules)", "type": "course", "resource": "JavaScript.info", "url": "https://javascript.info/", "duration": "1 week"}
        ],
        "certifications": ["FreeCodeCamp JS Algorithms Certification", "HackerRank JavaScript Certificate"]
    },
    "system design": {
        "skill_name": "System Design",
        "priority": "high",
        "estimated_weeks": 6,
        "why_important": "Critical for senior-level interviews, tests ability to architect scalable systems",
        "learning_path": [
            {"step": 1, "title": "System Design Primer", "type": "course", "resource": "GitHub - donnemartin", "url": "https://github.com/donnemartin/system-design-primer", "duration": "2 weeks"},
            {"step": 2, "title": "Design a URL Shortener", "type": "project", "resource": "Practice problem", "url": "", "duration": "1 week"},
            {"step": 3, "title": "Gaurav Sen System Design Playlist", "type": "course", "resource": "YouTube Playlist", "url": "https://www.youtube.com/playlist?list=PLMCXHnjXnTnvo6alSjVkgxV-VH6EPyvoX", "duration": "2 weeks"},
            {"step": 4, "title": "Design a Chat Application", "type": "project", "resource": "Practice problem", "url": "", "duration": "1 week"}
        ],
        "certifications": []
    },
    "microservices": {
        "skill_name": "Microservices",
        "priority": "medium",
        "estimated_weeks": 4,
        "why_important": "Modern architecture pattern for scalable applications, valued in mid-to-senior roles",
        "learning_path": [
            {"step": 1, "title": "Microservices Patterns & Principles", "type": "course", "resource": "Martin Fowler's Guide", "url": "https://martinfowler.com/microservices/", "duration": "4 days"},
            {"step": 2, "title": "Build a Simple Microservice", "type": "project", "resource": "Hands-on practice", "url": "", "duration": "1 week"},
            {"step": 3, "title": "Event-Driven Architecture", "type": "course", "resource": "FreeCodeCamp YouTube", "url": "https://www.youtube.com/watch?v=lkKbkRqMJ8g", "duration": "1 week"},
            {"step": 4, "title": "Multi-Service App with Message Queue", "type": "project", "resource": "Portfolio project", "url": "", "duration": "1.5 weeks"}
        ],
        "certifications": []
    },
    "ci/cd platforms": {
        "skill_name": "CI/CD Platforms",
        "priority": "medium",
        "estimated_weeks": 2,
        "why_important": "Automates testing and deployment, a core DevOps competency expected in modern teams",
        "learning_path": [
            {"step": 1, "title": "GitHub Actions Quickstart", "type": "course", "resource": "GitHub Docs", "url": "https://docs.github.com/en/actions/quickstart", "duration": "3 days"},
            {"step": 2, "title": "Set up CI/CD for a Project", "type": "project", "resource": "Hands-on practice", "url": "", "duration": "4 days"},
            {"step": 3, "title": "Advanced Pipelines (Jenkins/GitLab CI)", "type": "course", "resource": "TechWorld with Nana (YouTube)", "url": "https://www.youtube.com/watch?v=7KCS70sCoK0", "duration": "4 days"}
        ],
        "certifications": ["GitHub Actions Certification"]
    },
    # Data Science related skills
    "pandas": {
        "skill_name": "Pandas",
        "priority": "high",
        "estimated_weeks": 2,
        "why_important": "Primary data manipulation library in Python, essential for any data role",
        "learning_path": [
            {"step": 1, "title": "Pandas Getting Started", "type": "course", "resource": "Kaggle Learn", "url": "https://www.kaggle.com/learn/pandas", "duration": "4 days"},
            {"step": 2, "title": "Data Cleaning Project", "type": "project", "resource": "Kaggle Dataset", "url": "https://www.kaggle.com/datasets", "duration": "4 days"},
            {"step": 3, "title": "Advanced Pandas Techniques", "type": "course", "resource": "Real Python", "url": "https://realpython.com/pandas-python-explore-dataset/", "duration": "4 days"}
        ],
        "certifications": ["Kaggle Pandas Certification"]
    },
    "machine learning": {
        "skill_name": "Machine Learning",
        "priority": "high",
        "estimated_weeks": 8,
        "why_important": "Core competency for data science and AI roles, one of the fastest-growing fields",
        "learning_path": [
            {"step": 1, "title": "Machine Learning Crash Course", "type": "course", "resource": "Google ML Crash Course", "url": "https://developers.google.com/machine-learning/crash-course", "duration": "2 weeks"},
            {"step": 2, "title": "Build a Classification Model", "type": "project", "resource": "Kaggle Competition", "url": "https://www.kaggle.com/competitions", "duration": "1.5 weeks"},
            {"step": 3, "title": "Scikit-Learn & Feature Engineering", "type": "course", "resource": "Kaggle Learn", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "duration": "2 weeks"},
            {"step": 4, "title": "End-to-End ML Pipeline Project", "type": "project", "resource": "Portfolio project", "url": "", "duration": "2 weeks"}
        ],
        "certifications": ["Google Machine Learning Certificate", "AWS Machine Learning Specialty"]
    },
    "tensorflow": {
        "skill_name": "TensorFlow",
        "priority": "medium",
        "estimated_weeks": 5,
        "why_important": "Leading deep learning framework by Google, widely used in production ML systems",
        "learning_path": [
            {"step": 1, "title": "TensorFlow Basics", "type": "course", "resource": "TensorFlow Official Tutorials", "url": "https://www.tensorflow.org/tutorials", "duration": "1.5 weeks"},
            {"step": 2, "title": "Build an Image Classifier", "type": "project", "resource": "Hands-on practice", "url": "", "duration": "1 week"},
            {"step": 3, "title": "Deep Learning Specialization", "type": "course", "resource": "DeepLearning.AI (Coursera)", "url": "https://www.coursera.org/specializations/deep-learning", "duration": "2.5 weeks"}
        ],
        "certifications": ["TensorFlow Developer Certificate"]
    },
    # Marketing related skills
    "seo": {
        "skill_name": "SEO",
        "priority": "high",
        "estimated_weeks": 3,
        "why_important": "Critical for driving organic traffic, core competency for digital marketing roles",
        "learning_path": [
            {"step": 1, "title": "SEO Fundamentals", "type": "course", "resource": "Google Digital Garage", "url": "https://learndigital.withgoogle.com/digitalgarage", "duration": "1 week"},
            {"step": 2, "title": "Keyword Research & On-Page SEO", "type": "project", "resource": "Hands-on practice", "url": "", "duration": "4 days"},
            {"step": 3, "title": "Technical SEO & Analytics", "type": "course", "resource": "Moz Beginner's Guide", "url": "https://moz.com/beginners-guide-to-seo", "duration": "1 week"}
        ],
        "certifications": ["Google Analytics Certification", "HubSpot SEO Certification"]
    },
    "google analytics": {
        "skill_name": "Google Analytics",
        "priority": "high",
        "estimated_weeks": 2,
        "why_important": "Industry standard analytics platform, expected in all marketing and product roles",
        "learning_path": [
            {"step": 1, "title": "Google Analytics 4 Basics", "type": "course", "resource": "Google Skillshop", "url": "https://skillshop.withgoogle.com/", "duration": "4 days"},
            {"step": 2, "title": "Set Up GA4 for a Website", "type": "project", "resource": "Hands-on practice", "url": "", "duration": "3 days"},
            {"step": 3, "title": "Advanced Reports & Attribution", "type": "course", "resource": "Google Skillshop", "url": "https://skillshop.withgoogle.com/", "duration": "4 days"}
        ],
        "certifications": ["Google Analytics Certification (GA4)"]
    }
}


def _build_mock_skill_roadmap(gap_skills: list) -> list:
    """
    Builds a learning roadmap for each missing/recommended skill
    using the static roadmap database. Falls back to a generic template
    for skills not in the database.
    """
    roadmap = []
    for skill in gap_skills:
        skill_key = skill.lower()
        if skill_key in _SKILL_ROADMAP_DB:
            roadmap.append(_SKILL_ROADMAP_DB[skill_key])
        else:
            # Generic fallback roadmap for unknown skills
            roadmap.append({
                "skill_name": skill,
                "priority": "medium",
                "estimated_weeks": 3,
                "why_important": f"{skill} is a valuable addition to your skill set for this target role",
                "learning_path": [
                    {"step": 1, "title": f"Learn {skill} Fundamentals", "type": "course", "resource": "Official Documentation", "url": "", "duration": "1 week"},
                    {"step": 2, "title": f"Build a Small Project with {skill}", "type": "project", "resource": "Hands-on practice", "url": "", "duration": "1 week"},
                    {"step": 3, "title": f"Advanced {skill} Patterns", "type": "course", "resource": "YouTube / FreeCodeCamp", "url": "https://www.youtube.com/@freecodecamp", "duration": "1 week"}
                ],
                "certifications": []
            })
    return roadmap


def analyze_resume(resume_text: str, job_description: str = "") -> dict:
    """
    Analyzes the resume using Google Gemini AI, with automatic fallback to a local mock analyzer.
    """
    if not os.getenv("GEMINI_API_KEY"):
        print("Warning: GEMINI_API_KEY not found in environment. Using mock analyzer fallback.")
        return generate_mock_analysis(resume_text, job_description)

    # Prompt Engineering
    system_prompt = (
        "You are an expert recruiter and Applicant Tracking System (ATS) optimization expert.\n"
        "Analyze the provided candidate resume text, and optionally compare it to the job description.\n"
        "You MUST respond ONLY with a JSON object conforming to the following schema:\n"
        "{\n"
        "  \"score\": 78, // integer overall score out of 100\n"
        "  \"summary\": \"Brief overall performance summary.\",\n"
        "  \"key_metrics\": {\n"
        "    \"impact\": { \"score\": 75, \"label\": \"Impact & Results\", \"description\": \"Action verbs, metrics, results\" },\n"
        "    \"formatting\": { \"score\": 90, \"label\": \"Formatting & Structure\", \"description\": \"Structure, section headers, readability\" },\n"
        "    \"keywords\": { \"score\": 68, \"label\": \"Keyword Match\", \"description\": \"Matching job description skills\" }\n"
        "  },\n"
        "  \"keywords\": {\n"
        "    \"matching\": [\"React\", \"Python\", \"Git\"], // array of strings\n"
        "    \"missing\": [\"Docker\", \"CI/CD\"], // array of strings from JD that are absent\n"
        "    \"recommended\": [\"Kubernetes\", \"SQL Optimization\"] // industry standard tags relevant to the resume field to boost attractiveness\n"
        "  },\n"
        "  \"feedback\": [\n"
        "    {\n"
        "      \"category\": \"Formatting\", // Category name like Formatting, Experience, Skills, Education, etc.\n"
        "      \"score\": 90,\n"
        "      \"status\": \"excellent\", // 'excellent', 'good', 'warning', 'critical'\n"
        "      \"message\": \"Summary message about the layout\",\n"
        "      \"details\": [\"Actionable item 1\", \"Actionable item 2\"]\n"
        "    }\n"
        "  ],\n"
        "  \"bullet_optimizations\": [\n"
        "    {\n"
        "      \"original\": \"Original weak bullet point from the resume\",\n"
        "      \"optimized\": \"High-impact rewritten version using the Google XYZ formula (Accomplished [X] as measured by [Y], by doing [Z])\",\n"
        "      \"explanation\": \"Brief explanation of what was changed and why it is better.\"\n"
        "    }\n"
        "  ],\n"
        "  \"section_breakdown\": [\n"
        "    {\n"
        "      \"section_name\": \"Work Experience\",\n"
        "      \"score\": 72,\n"
        "      \"status\": \"warning\", // 'excellent', 'good', 'warning', 'critical'\n"
        "      \"verdict\": \"Short summary of how this section performs\",\n"
        "      \"strengths\": [\"Strength 1\", \"Strength 2\"],\n"
        "      \"improvements\": [\"Improvement 1\", \"Improvement 2\"]\n"
        "    }\n"
        "  ],\n"
        "  \"skill_roadmap\": [\n"
        "    {\n"
        "      \"skill_name\": \"Docker\",\n"
        "      \"priority\": \"high\", // 'high', 'medium', 'low'\n"
        "      \"estimated_weeks\": 3,\n"
        "      \"why_important\": \"Reason this skill matters for the target role\",\n"
        "      \"learning_path\": [\n"
        "        { \"step\": 1, \"title\": \"Course or resource name\", \"type\": \"course\", \"resource\": \"Platform name\", \"url\": \"https://example.com\", \"duration\": \"1 week\" }\n"
        "      ],\n"
        "      \"certifications\": [\"Relevant certification name\"]\n"
        "    }\n"
        "  ],\n"
        "  \"career_recommendations\": [\n"
        "    \"Suggested career action item 1 (e.g. build projects with X, learn framework Y, get certificate Z)\"\n"
        "  ],\n"
        "  \"cover_letter\": {\n"
        "    \"greeting\": \"Dear Hiring Manager,\",\n"
        "    \"opening\": \"Opening paragraph introducing yourself and expressing interest in the specific role, mentioning key qualifications\",\n"
        "    \"body\": \"Body paragraph highlighting 3-4 key skills and achievements from the resume that directly match the job requirements, with specific examples\",\n"
        "    \"closing\": \"Closing paragraph expressing enthusiasm, mentioning willingness to learn missing skills, and including a call to action\",\n"
        "    \"sign_off\": \"Sincerely,\\n[Candidate Name]\"\n"
        "  }\n"
        "}\n"
        "Be critical, realistic, and highly practical. Give constructive feedback that a candidate can act on immediately.\n"
        "For the cover_letter, write a compelling, professional cover letter that is tailored to the job description (if provided). "
        "Use a warm but professional tone. Highlight the candidate's strongest matching skills and experiences. Keep each paragraph concise (3-4 sentences)."
    )

    user_content = f"RESUME TEXT:\n{resume_text}\n\n"
    if job_description:
        user_content += f"JOB DESCRIPTION:\n{job_description}\n"
    else:
        user_content += "No specific job description provided. Perform a general evaluation of their professional profile and structure, suggesting industry standard improvements."

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        response = model.generate_content(user_content)
        analysis_data = clean_json_response(response.text)
        
        # Validate critical schema parts
        required_keys = ["score", "summary", "key_metrics", "keywords", "feedback", "bullet_optimizations", "career_recommendations", "section_breakdown", "skill_roadmap", "cover_letter"]
        for key in required_keys:
            if key not in analysis_data:
                raise ValueError(f"Missing required key '{key}' in LLM response JSON.")
                
        return analysis_data

    except Exception as e:
        print(f"Failed to use Gemini API due to error: {e}. Falling back to mock generator.")
        return generate_mock_analysis(resume_text, job_description)


def optimize_single_bullet(bullet_text: str) -> dict:
    """
    Optimizes a single resume bullet point using Google Gemini, or falls back to a highly customized mock rule.
    """
    if not bullet_text or not bullet_text.strip():
        return {
            "original": "",
            "optimized": "Please enter a valid bullet point to optimize.",
            "explanation": "No text was provided."
        }
        
    if not os.getenv("GEMINI_API_KEY"):
        # Local customized fallback rules for common bullet types
        text_lower = bullet_text.lower()
        
        # Rule 1: Coding/writing code
        if any(w in text_lower for w in ["write", "wrote", "code", "coding", "program", "develop", "developer", "backend", "frontend", "created", "built"]):
            optimized = "Engineered scalable software modules and refactored core backend routines, reducing system latency by 28% and boosting codebase maintainability."
            explanation = "Replaced passive words ('write', 'worked') with a strong action verb ('Engineered', 'Refactored') and added a quantifiable performance metric (28% latency reduction)."
        # Rule 2: Management/leadership
        elif any(w in text_lower for w in ["manage", "manager", "lead", "led", "team", "guided", "directed", "supervised", "responsible for team"]):
            optimized = "Spearheaded a cross-functional team of 5 engineers to deliver the core MVP, accelerating release velocity by 20% and improving Scrum milestone accuracy."
            explanation = "Quantified team size and business outcome, using 'Spearheaded' instead of 'managed' to emphasize leadership initiative."
        # Rule 3: Database/SQL
        elif any(w in text_lower for w in ["database", "sql", "query", "queries", "db", "mongo", "postgres", "mysql"]):
            optimized = "Optimized complex SQL queries and indexed database tables, yielding a 40% reduction in API response times and easing server payload under peak traffic."
            explanation = "Introduced technical specificity ('indexed', 'optimized') and defined a clear outcome for database performance."
        # Rule 4: Bug fixing/testing
        elif any(w in text_lower for w in ["bug", "bugs", "fix", "fixed", "test", "testing", "qa", "debug"]):
            optimized = "Designed automated integration test suites, increasing test coverage from 65% to 88% and eliminating 15+ critical production release blockages."
            explanation = "Switched from a chore-like description ('fixed bugs') to a proactive engineering accomplishment ('Designed test suites', 'increasing test coverage')."
        # Rule 5: Default fallback
        else:
            optimized = f"Spearheaded the redesign and optimization of key technical processes, resulting in a 15% increase in operational efficiency and smoother team collaboration."
            explanation = "Transformed a simple action into a high-impact achievement using the Google XYZ formula structure."
            
        return {
            "original": bullet_text,
            "optimized": optimized,
            "explanation": explanation
        }

    system_prompt = (
        "You are an expert resume editor and career coach.\n"
        "Take the user's resume bullet point and optimize it using the Google XYZ formula:\n"
        "Accomplished [X] as measured by [Y], by doing [Z].\n"
        "Return ONLY a JSON object conforming exactly to this schema:\n"
        "{\n"
        "  \"original\": \"Original bullet point entered by user\",\n"
        "  \"optimized\": \"Optimized high-impact bullet point using action verbs and metrics\",\n"
        "  \"explanation\": \"Short explanation of what changes were made and why it is better.\"\n"
        "}"
    )
    
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        response = model.generate_content(f"BULLET POINT TO OPTIMIZE: {bullet_text}")
        return clean_json_response(response.text)
    except Exception as e:
        print(f"Failed to optimize single bullet using Gemini: {e}")
        # Fall back to recursive mock optimizer call (by clearing the API key variable locally)
        old_key = os.environ.get("GEMINI_API_KEY")
        if old_key:
            del os.environ["GEMINI_API_KEY"]
        res = optimize_single_bullet(bullet_text)
        if old_key:
            os.environ["GEMINI_API_KEY"] = old_key
        return res

