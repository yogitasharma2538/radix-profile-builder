import streamlit as st
import json

st.set_page_config(page_title="Talent Profile Builder", layout="wide")

# Official Skill Categories
SKILL_CATEGORIES = [
    "COD", "DSA", "OOD", "COMM", "AI", "APTI", 
    "CLOUD", "SYSD", "SQL", "SWE", "NETW", "OS", "OTHER"
]

# Category icon mapping for a professional look
category_icons = {
    "COD": "💻", "DSA": "🧩", "OOD": "📐", "COMM": "💬", 
    "AI": "🤖", "APTI": "📊", "CLOUD": "☁️", "SYSD": "🏗️", 
    "SQL": "🗄️", "SWE": "⚙️", "NETW": "🌐", "OS": "🖥️", "OTHER": "✨"
}

# Sample candidate profiles for quick testing (matching hackathon test data)
sample_presets = {
    "Blank / Custom": {
        "name": "", "email": "", "education": "", 
        "skills": [], "hackathons": [], "internships": [], 
        "certifications": [], "preferred_roles": [], "cv_file": "resume.pdf"
    },
    "Ananya Rao (Systems Generalist)": {
        "name": "Ananya Rao",
        "email": "ananya.rao@example.com",
        "education": "B.Tech, Computer Science and Engineering, Class of 2026 (CGPA: 8.6/10)",
        "skills": [
            {"skill_name": "C++", "category_code": "COD", "evidence": "Listed in resume technical skills", "confidence": "high"},
            {"skill_name": "Python", "category_code": "COD", "evidence": "Used in backend projects", "confidence": "high"},
            {"skill_name": "Data Structures & Algorithms", "category_code": "DSA", "evidence": "350+ problems solved", "confidence": "high"},
            {"skill_name": "Operating Systems", "category_code": "OS", "evidence": "Multithreaded job scheduler project", "confidence": "high"}
        ],
        "hackathons": ["Finalist, national-level 24-hour hackathon - built a real-time chat backend"],
        "internships": ["Summer intern, backend team at a mid-size product startup - shipped a rate-limiter"],
        "certifications": [],
        "preferred_roles": ["Software Engineer", "Backend Engineer"],
        "cv_file": "Ananya Rao.pdf"
    },
    "Karthik Subramaniam (AI & ML)": {
        "name": "Karthik Subramaniam",
        "email": "karthik.subramaniam@example.com",
        "education": "B.Tech, Artificial Intelligence & Data Science, Class of 2025 (CGPA: 9.1/10)",
        "skills": [
            {"skill_name": "Python", "category_code": "COD", "evidence": "Primary programming language", "confidence": "high"},
            {"skill_name": "Machine Learning", "category_code": "AI", "evidence": "LLM fine-tuning pipelines", "confidence": "high"},
            {"skill_name": "PyTorch", "category_code": "AI", "evidence": "Custom neural networks", "confidence": "high"}
        ],
        "hackathons": ["Winner, Smart India Hackathon - AI-powered image segmentation"],
        "internships": ["AI Engineering Intern - optimized LLM inference latency"],
        "certifications": ["Deep Learning Specialization - Coursera"],
        "preferred_roles": ["AI Engineer", "Machine Learning Engineer"],
        "cv_file": "Karthik Subramaniam.pdf"
    },
    "Priya Menon (Cloud & DevOps)": {
        "name": "Priya Menon",
        "email": "priya.menon@example.com",
        "education": "B.Tech, Computer Science & Information Technology, Class of 2026 (CGPA: 8.4/10)",
        "skills": [
            {"skill_name": "Docker & Kubernetes", "category_code": "CLOUD", "evidence": "Containerized microservices", "confidence": "high"},
            {"skill_name": "AWS", "category_code": "CLOUD", "evidence": "Configured EC2, S3, and Lambda", "confidence": "high"}
        ],
        "hackathons": ["Runner-up, Cloud Infrastructure Challenge"],
        "internships": ["DevOps Engineering Intern - migrated monolith to AWS"],
        "certifications": ["AWS Certified Solutions Architect"],
        "preferred_roles": ["DevOps Engineer", "Cloud Engineer"],
        "cv_file": "Priya Menon.pdf"
    },
    "Rohan Verma (Data & Database)": {
        "name": "Rohan Verma",
        "email": "rohan.verma@example.com",
        "education": "B.Tech, Information Technology, Class of 2026 (CGPA: 8.2/10)",
        "skills": [
            {"skill_name": "PostgreSQL & MySQL", "category_code": "SQL", "evidence": "Designed complex schemas", "confidence": "high"},
            {"skill_name": "Data Engineering", "category_code": "SQL", "evidence": "ETL pipelines", "confidence": "high"}
        ],
        "hackathons": ["Top 5, Data Hackathon - anomaly detection database"],
        "internships": ["Data Analyst Intern - optimized database queries"],
        "certifications": ["Google Data Analytics Certificate"],
        "preferred_roles": ["Data Engineer", "Database Administrator"],
        "cv_file": "Rohan Verma.pdf"
    }
}

# --- INITIALIZE SESSION STATE ---
if "profile" not in st.session_state:
    st.session_state.profile = sample_presets["Ananya Rao (Systems Generalist)"].copy()

if "active_section" not in st.session_state:
    st.session_state.active_section = "Basic Info & Education"

p = st.session_state.profile

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Candidate Portal")

selected_preset_name = st.sidebar.selectbox("Load Sample Profile", list(sample_presets.keys()))
if selected_preset_name != "Blank / Custom":
    st.session_state.profile = sample_presets[selected_preset_name].copy()
    p = st.session_state.profile

st.sidebar.markdown("---")
st.sidebar.markdown("**Navigation**")

sections = [
    "Basic Info & Education",
    "Skills & Categories",
    "Hackathons & Internships",
    "Certifications & Roles",
    "Review & Export"
]

for sec in sections:
    if st.sidebar.button(sec, use_container_width=True, key=f"nav_{sec}"):
        st.session_state.active_section = sec

selection = st.session_state.active_section

# --- SECTION 1 ---
if selection == "Basic Info & Education":
    st.header("Basic Candidate Information")
    
    col1, col2 = st.columns(2)
    with col1:
        p["name"] = st.text_input("Full Name", value=p["name"])
    with col2:
        p["email"] = st.text_input("Email Address", value=p["email"])

    st.markdown("---")
    st.subheader("Normalized Education Background")
    
    edu_col1, edu_col2 = st.columns(2)
    with edu_col1:
        degree_options = ["B.Tech", "B.E.", "M.Tech", "M.E.", "MCA", "B.Sc", "BCA", "Other"]
        selected_degree = st.selectbox("Degree Program", degree_options)
        
        branch = st.text_input("Branch / Specialization", value="Computer Science and Engineering")
        
    with edu_col2:
        institution = st.text_input("Institution / University Name", value="University Name")
        
        years_options = [str(y) for y in range(2022, 2032)]
        grad_year = st.selectbox("Graduation Year", years_options, index=4)
        
    gpa = st.text_input("CGPA / Percentage", value="8.5 / 10")
    
    p["education"] = f"{selected_degree}, {branch}, {institution}, Class of {grad_year} (CGPA: {gpa})"

# --- SECTION 2 ---
elif selection == "Skills & Categories":
    st.header("Skills & Category Mapping")
    st.markdown("Select your applicable skill categories and manage your specific proficiencies.")
    
    st.subheader("Official Skill Categories")
    st.markdown("Check all categories that apply to your technical background:")
    
    current_cats = {s["category_code"] for s in p["skills"]}
    
    cols = st.columns(3)
    category_selections = {}
    
    for idx, cat in enumerate(SKILL_CATEGORIES):
        col_idx = idx % 3
        with cols[col_idx]:
            is_checked = cat in current_cats
            icon = category_icons.get(cat, "📌")
            category_selections[cat] = st.checkbox(f"{icon} {cat}", value=is_checked, key=f"cat_chk_{cat}")

    st.markdown("---")
    st.subheader("Manage Detailed Skills")
    st.markdown("Add specific skill names, map them to categories, and set your confidence level.")
    
    if "skill_builder_list" not in st.session_state or st.session_state.get("last_loaded_name") != p.get("name"):
        st.session_state.skill_builder_list = p["skills"].copy()
        st.session_state.last_loaded_name = p.get("name")
    
    with st.form("add_skill_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            new_skill_name = st.text_input("Skill Name (e.g., Python, PyTorch)")
        with col2:
            new_skill_cat = st.selectbox("Category", SKILL_CATEGORIES)
        with col3:
            new_skill_conf = st.selectbox("Confidence", ["high", "medium", "low"])
            
        add_btn = st.form_submit_button("+ Add Skill")
        if add_btn and new_skill_name:
            st.session_state.skill_builder_list.append({
                "skill_name": new_skill_name,
                "category_code": new_skill_cat,
                "confidence": new_skill_conf,
                "evidence": "Verified via Profile Builder interface"
            })
            st.success(f"Added skill: {new_skill_name}")

    st.markdown("**Current Skills List:**")
    skills_to_keep = []
    for idx, s in enumerate(st.session_state.skill_builder_list):
        col_info, col_del = st.columns([5, 1])
        with col_info:
            icon = category_icons.get(s['category_code'], "📌")
            st.write(f"- {icon} **{s['skill_name']}** (`{s['category_code']}`) — *Confidence: {s['confidence']}*")
        with col_del:
            if st.button("Delete", key=f"del_skill_{idx}"):
                continue
        skills_to_keep.append(s)
    
    st.session_state.skill_builder_list = skills_to_keep
    p["skills"] = st.session_state.skill_builder_list

# --- SECTION 3 ---
elif selection == "Hackathons & Internships":
    st.header("Hackathons & Internships")
    
    hack_str = "\n".join(p["hackathons"])
    hack_input = st.text_area("Hackathons (One per line)", value=hack_str)
    
    intern_str = "\n".join(p["internships"])
    intern_input = st.text_area("Internships (One per line)", value=intern_str)
    
    if st.button("Save Experience"):
        p["hackathons"] = [h.strip() for h in hack_input.split("\n") if h.strip()]
        p["internships"] = [i.strip() for i in intern_input.split("\n") if i.strip()]
        st.success("Experience details saved successfully!")

# --- SECTION 4 ---
elif selection == "Certifications & Roles":
    st.header("Certifications & Preferred Roles")
    
    cert_str = "\n".join(p["certifications"])
    cert_input = st.text_area("Certifications (One per line)", value=cert_str)
    
    roles_str = ", ".join(p["preferred_roles"])
    roles_input = st.text_input("Preferred Roles (Comma-separated)", value=roles_str)
    
    if st.button("Save Certifications & Roles"):
        p["certifications"] = [c.strip() for c in cert_input.split("\n") if c.strip()]
        p["preferred_roles"] = [r.strip() for r in roles_input.split(",") if r.strip()]
        st.success("Details saved successfully!")

# --- SECTION 5 ---
elif selection == "Review & Export":
    st.header("Review & Export Profile")
    st.markdown("Review your compiled candidate profile below before exporting.")
    
    final_payload = {
        "name": p["name"],
        "email": p["email"],
        "education": p["education"],
        "skills": p["skills"],
        "hackathons": p["hackathons"],
        "internships": p["internships"],
        "certifications": p["certifications"],
        "preferred_roles": p["preferred_roles"],
        "cv_file": p.get("cv_file", "resume.pdf")
    }
    
    st.json(final_payload)
    
    if st.button("Export Profile Data"):
        with open("candidate_profile.json", "w") as f:
            json.dump(final_payload, f, indent=4)
        st.success("Profile successfully exported to `candidate_profile.json`!")