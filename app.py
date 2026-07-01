import json
from pathlib import Path

import streamlit as st


DATA_FILE = Path("portfolio_data.json")


def load_data():
    if not DATA_FILE.exists():
        st.error("portfolio_data.json was not found.")
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def render_styles():
    st.markdown(
        """
        <style>
            .hero {
                padding: 70px 20px 45px 20px;
                text-align: center;
                background: linear-gradient(135deg, #f8fafc, #eef2ff);
                border-radius: 24px;
                margin-bottom: 30px;
            }

            .hero h1 {
                font-size: 50px;
                font-weight: 900;
                color: #0f172a;
                margin-bottom: 12px;
            }

            .hero p {
                font-size: 21px;
                color: #475569;
                max-width: 900px;
                margin: auto;
                line-height: 1.6;
            }

            .section-title {
                font-size: 32px;
                font-weight: 850;
                color: #0f172a;
                margin-top: 45px;
                margin-bottom: 18px;
            }

            .card {
                background: white;
                padding: 24px;
                border-radius: 18px;
                box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
                margin-bottom: 18px;
                border: 1px solid #e2e8f0;
            }

            .card h3 {
                color: #0f172a;
                margin-bottom: 8px;
            }

            .card p, .card li {
                color: #475569;
                font-size: 16px;
                line-height: 1.6;
            }

            .tag {
                display: inline-block;
                background-color: #e0f2fe;
                color: #0369a1;
                padding: 6px 10px;
                border-radius: 999px;
                font-size: 13px;
                margin: 4px 4px 4px 0;
            }

            .metric-card {
                background: #0f172a;
                color: white;
                padding: 22px;
                border-radius: 18px;
                margin-bottom: 16px;
                min-height: 110px;
            }

            .metric-card p {
                color: #e2e8f0;
                font-size: 16px;
                line-height: 1.5;
            }

            .contact-box {
                background-color: #0f172a;
                color: white;
                padding: 36px;
                border-radius: 20px;
                margin-top: 40px;
                text-align: center;
            }

            .contact-box h2 {
                color: white;
            }

            .contact-box p {
                color: #cbd5e1;
                font-size: 17px;
            }

            a {
                color: #2563eb;
                text-decoration: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_list(items):
    html = "<ul>"
    for item in items:
        html += f"<li>{item}</li>"
    html += "</ul>"
    return html


def render_site(data):
    render_styles()

    contact = data.get("contact", {})

    st.markdown(
        f"""
        <div class="hero">
            <h1>{data.get("headline", "")}</h1>
            <p>{data.get("subheadline", "")}</p>
            <br>
            <p><strong>{data.get("name", "")}</strong> | {contact.get("location", "")}</p>
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
                        <p>{item}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown('<div class="section-title">About</div>', unsafe_allow_html=True)

    about_html = "".join([f"<p>{paragraph}</p>" for paragraph in data.get("about", [])])

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
                [f'<span class="tag">{tag}</span>' for tag in project.get("tags", [])]
            )

            with columns[index % 2]:
                st.markdown(
                    f"""
                    <div class="card">
                        <h3>{project.get("title", "")}</h3>
                        <p>{project.get("description", "")}</p>
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
                        <h3>{skill.get("title", "")}</h3>
                        <p>{skill.get("description", "")}</p>
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
                <h3>{job.get("role", "")}</h3>
                <p><strong>{job.get("company", "")}</strong> | {job.get("type", "")}</p>
                <p><strong>{job.get("dates", "")}</strong></p>
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
            tool_tags = "".join([f'<span class="tag">{tool}</span>' for tool in tool_list])

            with columns[index % 2]:
                st.markdown(
                    f"""
                    <div class="card">
                        <h3>{category}</h3>
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
                <h3>{education.get("degree", "")}</h3>
                <p>{education.get("school", "")}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="contact-box">
            <h2>Let’s Connect</h2>
            <p><strong>Email:</strong> {contact.get("email", "")}</p>
            <p><strong>Phone:</strong> {contact.get("phone", "")}</p>
            <p><strong>GitHub:</strong> {contact.get("github", "")}</p>
            <p><strong>LinkedIn:</strong> {contact.get("linkedin", "")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_editor(data):
    st.title("Edit Portfolio Content")

    with st.form("main_content_form"):
        st.subheader("Main Info")

        data["name"] = st.text_input("Name", value=data.get("name", ""))
        data["headline"] = st.text_input("Headline", value=data.get("headline", ""))
        data["subheadline"] = st.text_area("Subheadline", value=data.get("subheadline", ""), height=120)

        st.subheader("Contact")

        contact = data.setdefault("contact", {})
        contact["email"] = st.text_input("Email", value=contact.get("email", ""))
        contact["phone"] = st.text_input("Phone", value=contact.get("phone", ""))
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
            data["about"] = [line.strip() for line in about_text.splitlines() if line.strip()]
            data["highlights"] = [line.strip() for line in highlights_text.splitlines() if line.strip()]
            save_data(data)
            st.success("Main content saved.")

    st.divider()

    st.subheader("Projects")

    for index, project in enumerate(data.get("projects", [])):
        with st.expander(f"Project {index + 1}: {project.get('title', 'Untitled')}"):
            project["title"] = st.text_input("Project Title", value=project.get("title", ""), key=f"project_title_{index}")
            project["description"] = st.text_area("Project Description", value=project.get("description", ""), key=f"project_description_{index}")

            tags_text = ", ".join(project.get("tags", []))
            tags_text = st.text_input("Tags, separated by commas", value=tags_text, key=f"project_tags_{index}")
            project["tags"] = [tag.strip() for tag in tags_text.split(",") if tag.strip()]

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
            skill["title"] = st.text_input("Skill Title", value=skill.get("title", ""), key=f"skill_title_{index}")
            skill["description"] = st.text_area("Skill Description", value=skill.get("description", ""), key=f"skill_description_{index}")

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

    st.info("For work experience, tools, and education, edit portfolio_data.json directly in GitHub for now.")


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
