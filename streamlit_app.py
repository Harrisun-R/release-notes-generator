import streamlit as st
from datetime import datetime
from fpdf import FPDF
from googletrans import Translator

NAME = "Harrisun"
LINKEDIN_URL = "https://www.linkedin.com/in/harrisun-raj-mohan/"

# Set up the app title
st.title("Enhanced Release Notes Generator")
st.write(f"Developed by {NAME}")
st.write(f"[Connect on LinkedIn]({LINKEDIN_URL})")

# Input fields for basic details
st.header("Enter Release Details")
version_number = st.text_input("Version Number", placeholder="e.g., 1.0.0")
release_date = st.date_input("Release Date", value=datetime.today())

# Dropdown categories for Features and Bug Fixes
st.header("Categorized Features and Bug Fixes")
categories = ["UI Improvements", "Performance Enhancements", "Backend Changes", "Other"]
feature_data = {}
bug_data = {}

st.subheader("Features by Category")
for category in categories:
    feature_data[category] = st.text_area(f"Features - {category}", placeholder=f"Enter {category.lower()} features, one per line")

st.subheader("Bug Fixes by Category")
for category in categories:
    bug_data[category] = st.text_area(f"Bug Fixes - {category}", placeholder=f"Enter {category.lower()} bug fixes, one per line")

# Known Issues with Prioritization
st.header("Known Issues")
priority_levels = ["Critical", "High", "Medium", "Low"]
known_issues = []

for level in priority_levels:
    issues = st.text_area(f"Known Issues - {level} Priority", placeholder=f"Enter {level.lower()} priority issues, one per line")
    if issues.strip():
        known_issues.append((level, issues.strip().split("\n")))

# Template customization
st.header("Template Customization")
template_type = st.radio(
    "Choose a template style",
    options=["Formal", "Detailed", "Concise"]
)

# Localization
st.header("Localization")
languages = {"English": "en", "French": "fr", "Spanish": "es", "German": "de"}
language_choice = st.selectbox("Choose Language", list(languages.keys()))
translator = Translator()

# Export Options
st.header("Export Options")
export_format = st.radio("Export as", options=["Markdown", "PDF"])

# Generate Release Notes Button
if st.button("Generate Release Notes"):
    # Validate mandatory fields
    if not version_number:
        st.error("Please enter a version number.")
    elif not any(feature_data.values()) and not any(bug_data.values()) and not known_issues:
        st.error("Please enter at least one feature, bug fix, or known issue.")
    else:
        # Generate release notes
        st.subheader("Formatted Release Notes")
        release_notes = f"**Release Notes**\n\n**Version:** {version_number}\n**Release Date:** {release_date.strftime('%B %d, %Y')}\n\n"

        # Features
        if any(feature_data.values()):
            release_notes += "### Features\n"
            for category, features in feature_data.items():
                if features.strip():
                    release_notes += f"#### {category}\n"
                    release_notes += "\n".join([f"- {feature.strip()}" for feature in features.strip().split("\n")]) + "\n"

        # Bug Fixes
        if any(bug_data.values()):
            release_notes += "### Bug Fixes\n"
            for category, bugs in bug_data.items():
                if bugs.strip():
                    release_notes += f"#### {category}\n"
                    release_notes += "\n".join([f"- {bug.strip()}" for bug in bugs.strip().split("\n")]) + "\n"

        # Known Issues
        if known_issues:
            release_notes += "### Known Issues\n"
            for priority, issues in known_issues:
                release_notes += f"**{priority} Priority:**\n"
                release_notes += "\n".join([f"- {issue.strip()}" for issue in issues]) + "\n"

        # Translate release notes if needed
        if language_choice != "English":
            release_notes = translator.translate(release_notes, dest=languages[language_choice]).text

        # Display release notes
        st.text_area("Release Notes Preview", release_notes, height=300)

        # Export options
        if export_format == "Markdown":
            st.download_button(
                label="Download Release Notes as Markdown",
                data=release_notes,
                file_name="release_notes.md",
                mime="text/markdown"
            )
        elif export_format == "PDF":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)
            for line in release_notes.split("\n"):
                pdf.multi_cell(0, 10, line)
            pdf_output = pdf.output(dest="S").encode("latin1")
            st.download_button(
                label="Download Release Notes as PDF",
                data=pdf_output,
                file_name="release_notes.pdf",
                mime="application/pdf"
            )
