import base64
import json
import html
from pathlib import Path

import streamlit as st
from PIL import Image


DATA_FILE = Path("portfolio_data.json")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def load_data():
    if not DATA_FILE.exists():
        st.error("portfolio_data.json was not found.")
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def safe_text(value):
    return html.escape(str(value or ""))


def phone_to_whatsapp_number(phone):
    digits = "".join(char for char in str(phone or "") if char.isdigit())

    if digits.startswith("0"):
        digits = "63" + digits[1:]

    if digits.startswith("9") and len(digits) == 10:
        digits = "63" + digits

    return digits


def image_to_base64(image_path):
    path = Path(image_path)

    if not path.exists():
        return ""

    file_extension = path.suffix.lower().replace(".", "")

    if file_extension == "jpg":
        file_extension = "jpeg"

    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    return f"data:image/{file_extension};base64,{encoded}"


def save_uploaded_photo(uploaded_file, filename="profile_photo.png"):
    UPLOAD_DIR.mkdir(exist_ok=True)

    file_path = UPLOAD_DIR / filename

    image = Image.open(uploaded_file)
    image = image.convert("RGB")
    image.save(file_path, format="PNG")

    return str(file_path)


def render_styles():
    st.markdown(
        """
<style>
    .stApp {
        background-color: #F7EFE5;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .hero {
        padding: 70px 28px 48px 28px;
        text-align: center;
        background: linear-gradient(135deg, #F6EDE1, #E8D3BD);
        border-radius: 28px;
        margin-bottom: 30px;
        border: 1px solid #D7B899;
        box-shadow: 0 10px 30px rgba(82, 52, 34, 0.10);
    }

    .hero h1 {
        font-size: 50px;
        font-weight: 900;
        color: #3B2618;
        margin-bottom: 12px;
        line-height: 1.1;
    }

    .hero p {
        font-size: 21px;
        color: #4A2F1D;
        max-width: 900px;
        margin: auto;
        line-height: 1.6;
        font-weight: 600;
    }

    .profile-wrapper {
        display: flex;
        justify-content: center;
        margin-bottom: 24px;
    }

    .profile-photo {
        width: 178px;
        height: 178px;
        object-fit: cover;
        border-radius: 999px;
        border: 7px solid #D7B899;
        box-shadow: 0 10px 30px rgba(82, 52, 34, 0.24);
    }

    .section-title {
        font-size: 32px;
        font-weight: 850;
        color: #3B2618;
        margin-top: 45px;
        margin-bottom: 18px;
    }

    .card {
        background: #FFF8EF;
        padding: 24px;
        border-radius: 18px;
        box-shadow: 0 4px 14px rgba(82, 52, 34, 0.10);
        margin-bottom: 18px;
        border: 1px solid #E3C7A9;
    }

    .card h3 {
        color: #3B2618;
        margin-bottom: 8px;
        font-size: 22px;
    }

    .card p,
    .card li {
        color: #4A2F1D;
        font-size: 16px;
        line-height: 1.6;
        font-weight: 500;
    }

    .tag {
        display: inline-block;
        background-color: #E8D3BD;
        color: #3B2618;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 13px;
        margin: 4px 4px 4px 0;
        font-weight: 700;
        border: 1px solid #D7B899;
    }

    .metric-card {
        background: #E8D3BD;
        color: #3B2618;
        padding: 22px;
        border-radius: 18px;
        margin-bottom: 16px;
        min-height: 115px;
        box-shadow: 0 6px 18px rgba(82, 52, 34, 0.16);
        border: 1px solid #D7B899;
    }

    .metric-card p {
        color: #3B2618;
        font-size: 16px;
        line-height: 1.5;
        font-weight: 700;
    }

    .contact-box {
        background-color: #E8D3BD;
        color: #3B2618;
        padding: 38px;
        border-radius: 22px;
        margin-top: 40px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(82, 52, 34, 0.18);
        border: 1px solid #D7B899;
    }

    .contact-box h2 {
        color: #3B2618;
        font-size: 30px;
        margin-bottom: 18px;
    }

    .contact-box p {
        color: #4A2F1D;
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .contact-box a {
        color: #3B2618;
        text-decoration: underline;
        text-underline-offset: 4px;
        font-weight: 900;
    }

    .contact-box a:hover {
        color: #8B5E3C;
    }

    .small-note {
        color: #4A2F1D;
        font-size: 14px;
        line-height: 1.5;
        font-weight: 600;
    }

    a {
        color: #3B2618;
        text-decoration: underline;
        text-underline-offset: 4px;
        font-weight: 900;
    }

    a:hover {
        color: #8B5E3C;
    }

    section[data-testid="stSidebar"] {
        background-color: #EFE0CF;
        border-right: 1px solid #D7B899;
    }

    section[data-testid="stSidebar"] * {
        color: #3B2618;
    }

    div[data-testid="stRadio"] label {
        color: #3B2618;
    }

    .stButton button {
        background-color: #E8D3BD;
        color: #3B2618;
        border-radius: 999px;
        border: 1px solid #D7B899;
        padding: 0.55rem 1.2rem;
        font-weight: 800;
    }

    .stButton button:hover {
        background-color: #D7B899;
        color: #3B2618;
        border: 1px solid #C7A47F;
    }

    input,
    textarea {
        background-color: #FFF8EF !important;
        color: #3B2618 !important;
        border: 1px solid #D7B899 !important;
    }

    label,
    .stMarkdown,
    .stTextInput label,
    .stTextArea label,
    .stFileUploader label {
        color: #3B2618 !important;
    }

    div[data-testid="stExpander"] {
        background-color: #FFF8EF;
        border: 1px solid #E3C7A9;
        border-radius: 14px;
    }

    div[data-testid="stExpander"] * {
        color: #3B2618;
    }
</style>
""",
        unsafe_allow_html=True,
    )


def render_list(items):
    html_output = "<ul>"

    for item in items:
        html_output += f"<li>{safe_text(item)}</li>"

    html_output += "</ul>"
    return html_output


def render_profile_photo(data):
    photo_path = data.get("profile_photo", "")
    image_src = image_to_base64(photo_path)

    if image_src:
        st.markdown(
            f"""
<div class="profile-wrapper">
<img src="{image_src}" class="profile-photo">
</div>
""",
            unsafe_allow_html=True,
        )


def render_site(data):
    render_styles()

    contact = data.get("contact", {})

    st.markdown('<div class="hero">', unsafe_allow_html=True)

    render_profile_photo(data)

    st.markdown(
        f"""
<h1>{safe_text(data.get("headline", ""))}</h1>
<p>{safe_text(data.get("subheadline", ""))}</p>
<br>
<p><strong>{safe_text(data.get("name", ""))}</strong> | {safe_text(contact.get("location", ""))}</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">Career Highlights</div>', unsafe_allow_html=True)

    highlights = data.get("highlights", [])

    if highlights:
        columns = st.columns(3)

        for index, item in enumerate(highlights):
            with columns[index % 3]:
                st.markdown(
                    f"""
<div class="metric-card">
<p>{safe_text(item)}</p>
</div>
""",
                    unsafe_allow_html=True,
                )

    st.markdown('<div class="section-title">About</div>', unsafe_allow_html=True)

    about_html = "".join(
        [f"<p>{safe_text(paragraph)}</p>" for paragraph in data.get("about", [])]
    )

    st.markdown(
        f"""
<div class="card">
{about_html}
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">Featured Python Projects</div>', unsafe_allow_html=True)

    projects = data.get("projects", [])

    if projects:
        columns = st.columns(2)

        for index, project in enumerate(projects):
            tags_html = "".join(
                [f'<span class="tag">{safe_text(tag)}</span>' for tag in project.get("tags", [])]
            )

            with columns[index % 2]:
                st.markdown(
                    f"""
<div class="card">
<h3>{safe_text(project.get("title", ""))}</h3>
<p>{safe_text(project.get("description", ""))}</p>
{tags_html}
</div>
""",
                    unsafe_allow_html=True,
                )

    st.markdown('<div class="section-title">Skills</div>', unsafe_allow_html=True)

    skills = data.get("skills", [])

    if skills:
        columns = st.columns(3)

        for index, skill in enumerate(skills):
            with columns[index % 3]:
                st.markdown(
                    f"""
<div class="card">
<h3>{safe_text(skill.get("title", ""))}</h3>
<p>{safe_text(skill.get("description", ""))}</p>
</div>
""",
                    unsafe_allow_html=True,
                )

    st.markdown('<div class="section-title">Work Experience</div>', unsafe_allow_html=True)

    for job in data.get("experience", []):
        bullets = render_list(job.get("description", []))

        st.markdown(
            f"""
<div class="card">
<h3>{safe_text(job.get("role", ""))}</h3>
<p><strong>{safe_text(job.get("company", ""))}</strong> | {safe_text(job.get("type", ""))}</p>
<p><strong>{safe_text(job.get("dates", ""))}</strong></p>
{bullets}
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">Tools & Technologies</div>', unsafe_allow_html=True)

    tools = data.get("tools", {})

    if tools:
        columns = st.columns(2)

        for index, (category, tool_list) in enumerate(tools.items()):
            tool_tags = "".join(
                [f'<span class="tag">{safe_text(tool)}</span>' for tool in tool_list]
            )

            with columns[index % 2]:
                st.markdown(
                    f"""
<div class="card">
<h3>{safe_text(category)}</h3>
{tool_tags}
</div>
""",
                    unsafe_allow_html=True,
                )

    st.markdown('<div class="section-title">Education</div>', unsafe_allow_html=True)

    for education in data.get("education", []):
        st.markdown(
            f"""
<div class="card">
<h3>{safe_text(education.get("degree", ""))}</h3>
<p>{safe_text(education.get("school", ""))}</p>
</div>
""",
            unsafe_allow_html=True,
        )

    email_raw = contact.get("email", "")
    phone_raw = contact.get("phone", "")
    github_raw = contact.get("github", "")
    linkedin_raw = contact.get("linkedin", "")

    email = safe_text(email_raw)
    phone = safe_text(phone_raw)
    github = safe_text(github_raw)
    linkedin = safe_text(linkedin_raw)

    whatsapp_number = phone_to_whatsapp_number(phone_raw)
    whatsapp_link = f"https://wa.me/{whatsapp_number}" if whatsapp_number else "#"
    email_link = f"mailto:{email_raw}" if email_raw else "#"

    st.markdown(
        f"""
<div class="contact-box">
<h2>Let’s Connect</h2>
<p><strong>Email:</strong> <a href="{email_link}" target="_blank">{email}</a></p>
<p><strong>WhatsApp:</strong> <a href="{whatsapp_link}" target="_blank">{phone}</a></p>
<p><strong>GitHub:</strong> <a href="{github_raw}" target="_blank">{github}</a></p>
<p><strong>LinkedIn:</strong> <a href="{linkedin_raw}" target="_blank">{linkedin}</a></p>
</div>
""",
        unsafe_allow_html=True,
    )


def render_editor(data):
    render_styles()

    st.title("Edit Portfolio Content")

    st.subheader("Profile Photo")

    current_photo = data.get("profile_photo", "")

    if current_photo and Path(current_photo).exists():
        st.image(current_photo, width=180)
        st.caption(current_photo)

    uploaded_photo = st.file_uploader(
        "Upload profile photo",
        type=["png", "jpg", "jpeg"],
        help="This saves the image inside the uploads folder as profile_photo.png."
    )

    if uploaded_photo is not None:
        saved_path = save_uploaded_photo(uploaded_photo)
        data["profile_photo"] = saved_path
        save_data(data)
        st.success("Profile photo uploaded and saved.")
        st.rerun()

    st.markdown(
        """
<p class="small-note">
Important: in Codespaces this saves the uploaded file into the repo. After uploading a photo,
commit and push the file so it stays permanently in GitHub.
</p>
""",
        unsafe_allow_html=True,
    )

    st.divider()

    with st.form("main_content_form"):
        st.subheader("Main Info")

        data["name"] = st.text_input("Name", value=data.get("name", ""))
        data["headline"] = st.text_input("Headline", value=data.get("headline", ""))
        data["subheadline"] = st.text_area(
            "Subheadline",
            value=data.get("subheadline", ""),
            height=120
        )

        st.subheader("Contact")

        contact = data.setdefault("contact", {})
        contact["email"] = st.text_input("Email", value=contact.get("email", ""))
        contact["phone"] = st.text_input("Phone / WhatsApp", value=contact.get("phone", ""))
        contact["location"] = st.text_input("Location", value=contact.get("location", ""))
        contact["github"] = st.text_input("GitHub URL", value=contact.get("github", ""))
        contact["linkedin"] = st.text_input("LinkedIn URL", value=contact.get("linkedin", ""))

        st.subheader("About")

        about_text = "\n".join(data.get("about", []))
        about_text = st.text_area("About paragraphs", value=about_text, height=180)

        st.subheader("Career Highlights")

        highlights_text = "\n".join(data.get("highlights", []))
        highlights_text = st.text_area("Career highlights", value=highlights_text, height=180)

        submitted = st.form_submit_button("Save Main Content")

        if submitted:
            data["about"] = [
                line.strip()
                for line in about_text.splitlines()
                if line.strip()
            ]

            data["highlights"] = [
                line.strip()
                for line in highlights_text.splitlines()
                if line.strip()
            ]

            save_data(data)
            st.success("Main content saved.")

    st.divider()

    st.subheader("Projects")

    for index, project in enumerate(data.get("projects", [])):
        with st.expander(f"Project {index + 1}: {project.get('title', 'Untitled')}"):
            project["title"] = st.text_input(
                "Project Title",
                value=project.get("title", ""),
                key=f"project_title_{index}"
            )

            project["description"] = st.text_area(
                "Project Description",
                value=project.get("description", ""),
                key=f"project_description_{index}"
            )

            tags_text = ", ".join(project.get("tags", []))
            tags_text = st.text_input(
                "Tags, separated by commas",
                value=tags_text,
                key=f"project_tags_{index}"
            )

            project["tags"] = [
                tag.strip()
                for tag in tags_text.split(",")
                if tag.strip()
            ]

            if st.button("Delete Project", key=f"delete_project_{index}"):
                data["projects"].pop(index)
                save_data(data)
                st.rerun()

    if st.button("Add New Project"):
        data.setdefault("projects", []).append(
            {
                "title": "New Project",
                "description": "Describe this project here.",
                "tags": ["Python"]
            }
        )
        save_data(data)
        st.rerun()

    if st.button("Save Projects"):
        save_data(data)
        st.success("Projects saved.")

    st.divider()

    st.subheader("Skills")

    for index, skill in enumerate(data.get("skills", [])):
        with st.expander(f"Skill {index + 1}: {skill.get('title', 'Untitled')}"):
            skill["title"] = st.text_input(
                "Skill Title",
                value=skill.get("title", ""),
                key=f"skill_title_{index}"
            )

            skill["description"] = st.text_area(
                "Skill Description",
                value=skill.get("description", ""),
                key=f"skill_description_{index}"
            )

            if st.button("Delete Skill", key=f"delete_skill_{index}"):
                data["skills"].pop(index)
                save_data(data)
                st.rerun()

    if st.button("Add New Skill"):
        data.setdefault("skills", []).append(
            {
                "title": "New Skill",
                "description": "Describe this skill here."
            }
        )
        save_data(data)
        st.rerun()

    if st.button("Save Skills"):
        save_data(data)
        st.success("Skills saved.")

    st.divider()

    st.info("For work experience, tools, and education, edit portfolio_data.json directly for now.")


def main():
    st.set_page_config(
        page_title="Shin Manreal Portfolio",
        page_icon="🐍",
        layout="wide"
    )

    data = load_data()

    st.sidebar.title("Portfolio Menu")

    page = st.sidebar.radio(
        "Choose View",
        ["Portfolio Site", "Edit Content"]
    )

    if page == "Portfolio Site":
        render_site(data)

    if page == "Edit Content":
        render_editor(data)


if __name__ == "__main__":
    main()