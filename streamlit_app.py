import streamlit as st
from transformers import GPTJForCausalLM, GPT2Tokenizer
import torch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import markdown
from googletrans import Translator

# Load GPT-J model and tokenizer from Hugging Face
model_name = "EleutherAI/gpt-j-6B"
model = GPTJForCausalLM.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Function to generate text using GPT-J
def generate_text(input_text, max_length=500):
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Function to export release notes as Markdown
def export_to_markdown(release_notes):
    md = markdown.markdown(release_notes)
    with open("release_notes.md", "w") as file:
        file.write(md)
    st.download_button(label="Download as Markdown", data=open("release_notes.md", "r").read(), file_name="release_notes.md", mime="text/markdown")

# Function to export release notes as PDF
def export_to_pdf(release_notes):
    pdf_filename = "release_notes.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(30, 750, release_notes)
    c.save()
    st.download_button(label="Download as PDF", data=open(pdf_filename, "rb").read(), file_name=pdf_filename, mime="application/pdf")

# Function to translate the release notes
def translate_text(text, target_language="en"):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Streamlit UI elements
st.title("Release Notes Generator")

# Inputs for version number, date, features, bug fixes, and known issues
version_number = st.text_input("Version Number", "1.0.0")
release_date = st.date_input("Release Date")
features = st.text_area("Features", "List the features here")
bug_fixes = st.text_area("Bug Fixes", "List the bug fixes here")
known_issues = st.text_area("Known Issues", "List any known issues here")

# Categorization inputs
feature_category = st.selectbox("Feature Category", ["UI Improvements", "Performance Enhancements", "Backend Changes", "Other"])
bug_fix_category = st.selectbox("Bug Fix Category", ["Critical", "High", "Medium", "Low"])

# Customization options for release note format
note_format = st.radio(
    "Choose the Release Note Format", 
    ("Formal", "Detailed", "Concise"),
    help="Select the format for the release notes"
)

# Localization: Language selection for translation
languages = ["en", "es", "fr", "de", "it"]
selected_language = st.selectbox("Select Language for Localization", languages)

# Function to generate customized release notes based on format
def customize_release_notes(notes, format_type):
    if format_type == "Formal":
        return f"### Release Notes for Version {version_number}\n\n" \
               f"**Release Date:** {release_date}\n\n" \
               f"**Features:**\n{notes['features']}\n\n" \
               f"**Bug Fixes:**\n{notes['bug_fixes']}\n\n" \
               f"**Known Issues:**\n{notes['known_issues']}"
    
    elif format_type == "Detailed":
        return f"### Detailed Release Notes for Version {version_number}\n\n" \
               f"**Release Date:** {release_date}\n\n" \
               f"**Features:**\n{notes['features']}\n\n" \
               f"**Bug Fixes:**\n{notes['bug_fixes']}\n\n" \
               f"**Known Issues:**\n{notes['known_issues']}\n" \
               f"\n**Additional Information:**\n" \
               f"Please refer to our user guide for more details."
    
    else:  # Concise format
        return f"### {version_number} Release Notes\n\n" \
               f"**Features:** {notes['features']} \n\n" \
               f"**Bug Fixes:** {notes['bug_fixes']} \n\n" \
               f"**Known Issues:** {notes['known_issues']}"

# Generate the release notes based on inputs
if st.button("Generate Release Notes"):
    # Construct the input text for GPT-J based on user input
    input_text = f"""
    Create a {note_format} release note for version {version_number}, released on {release_date}.
    Features:
    {features}
    Categorized as: {feature_category}

    Bug Fixes:
    {bug_fixes}
    Categorized as: {bug_fix_category}

    Known Issues:
    {known_issues}
    """

    # Generate the release notes using GPT-J
    generated_notes = generate_text(input_text)
    
    # Format the release notes based on user selection (Formal, Detailed, Concise)
    formatted_notes = customize_release_notes({
        'features': features, 
        'bug_fixes': bug_fixes, 
        'known_issues': known_issues
    }, note_format)

    # Display the generated release notes
    st.subheader(f"Generated {note_format} Release Notes:")
    st.text_area("Release Notes", formatted_notes, height=300)

    # Export options
    export_to_markdown(formatted_notes)
    export_to_pdf(formatted_notes)

    # Localization: Translate release notes to the selected language
    if selected_language != "en":
        translated_notes = translate_text(formatted_notes, target_language=selected_language)
        st.subheader(f"Release Notes in {selected_language.upper()}:")
        st.text_area(f"Translated Release Notes ({selected_language.upper()})", translated_notes, height=300)
