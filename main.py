import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post, set_llm_model
import pyperclip  # For copying to clipboard

# Set page configuration for a better-looking app
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="😎",
    layout="centered",
    initial_sidebar_state="auto",
)

# Initialize session state for history if it doesn't exist
if "post_history" not in st.session_state:
    st.session_state["post_history"] = []

# Apply custom CSS for a more polished look
st.markdown("""
    <style>
    /* Background and font styling */
    .stApp {
        background-color: #1c1e21;
        color: #e4e6eb;
        font-family: 'Arial', sans-serif;
    }
    
    /* Title and subtitle container styling */
    .title-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1em;
    }
    .title-text {
        font-size: 2.5em;
        font-weight: 700;
        color: #f0f2f5;
    }
    .subtitle-text {
        font-size: 1em;
        font-weight: normal;
        color: #f0f2f5;
        text-align: right;
    }

    /* Styling dropdowns and buttons */
    .stSelectbox, .stButton button {
        background-color: #3a3b3c;
        color: #e4e6eb;
        border: none;
        border-radius: 6px;
    }

    /* Styling the generate button */
    .stButton button {
        width: 100%;
        padding: 0.75em;
        font-weight: bold;
        background-color: #4b7bec;
    }
    
    /* Post output styling */
    .post-output {
        padding: 1em;
        background-color: #242526;
        border-radius: 8px;
        margin-top: 1em;
        font-size: 1.1em;
        color: #f5f6fa;
        border-left: 4px solid #4b7bec;
    }

    /* Center align character count */
    .char-count {
        text-align: center;
        font-size: 0.9em;
        color: #8d99ae;
        margin-top: 0.5em;
    }
    
    /* Preview post styling with reactions */
    .preview-post {
        padding: 1em;
        background-color: #3b3b3c;
        border-radius: 8px;
        color: #e4e6eb;
        border: 1px solid #4b7bec;
        text-align: left;
        position: relative;
    }
    .reaction-icons {
        display: flex;
        gap: 10px;
        margin-top: 0.5em;
        font-size: 1.5em;
    }
    .reaction-icons span {
        display: flex;
        align-items: center;
        color: #e4e6eb;
    }
    </style>
    """, unsafe_allow_html=True)

# Main content with title centered and subtitle aligned right
st.markdown("""
    <div class="title-container">
        <div class="title-text">LinkedIn Post Generator</div>
        <div class="subtitle-text">By Jillani SoftTech 😎</div>
    </div>
""", unsafe_allow_html=True)

# Add descriptive subheaders
st.subheader("Create Engaging LinkedIn Posts with Ease")

# Initialize dropdown options
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "Roman English", "Urdu"]
model_options = ["OpenAI", "Open-Source (Llama)"]
tone_options = ["Professional", "Casual", "Inspirational", "Friendly"]
emoji_options = ["😊", "💼", "📈", "🔥", "💪", "🌟", "✨", "🚀"]

# Layout for model selection and dropdown options
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    selected_model = st.selectbox("Model", options=model_options, help="Select the model to use for generating content.")
with col2:
    fs = FewShotPosts()
    tags = fs.get_tags()
    selected_tag = st.selectbox("Topic", options=tags, help="Choose the topic for your LinkedIn post.")
with col3:
    selected_length = st.selectbox("Length", options=length_options, help="Specify the desired length of the post.")
with col4:
    selected_language = st.selectbox("Language", options=language_options, help="Select the language of the post.")

# Additional feature for tone and emoji selection
selected_tone = st.selectbox("Tone", options=tone_options, help="Select the tone for your post.")
selected_emoji = st.selectbox("Add Emoji", options=emoji_options, help="Choose an emoji to personalize your post.")

# Set the model based on user choice
set_llm_model(selected_model.lower())

# Generate Hashtag Suggestions
def get_hashtag_suggestions(tag):
    suggestions = {
        "Job Search": ["#CareerGrowth", "#JobHunt", "#ResumeTips"],
        "Motivation": ["#StayPositive", "#Success", "#Mindset"],
        "Mental Health": ["#SelfCare", "#Wellbeing", "#MentalHealth"],
        "Leadership": ["#Leadership", "#TeamBuilding", "#Inspiration"],
        "Productivity": ["#TimeManagement", "#Focus", "#Productivity"]
    }
    return suggestions.get(tag, ["#LinkedIn", "#Networking"])

hashtag_suggestions = get_hashtag_suggestions(selected_tag)

# Button to generate the LinkedIn post
if st.button("Generate Post"):
    post = generate_post(selected_length, selected_language, selected_tag)
    post = f"{selected_emoji} {post} {' '.join(hashtag_suggestions)}"
    
    # Display the generated post in a styled box
    st.markdown(f"<div class='post-output'>{post}</div>", unsafe_allow_html=True)
    
    # Store generated post in history
    st.session_state["post_history"].append(post)
    
    # Character count display
    char_count = len(post)
    st.markdown(f"<div class='char-count'>Character count: {char_count} / 3000</div>", unsafe_allow_html=True)
    
    # Editable text area for finalizing post
    edited_post = st.text_area("Edit your post", post, height=150)

    # Preview mode button with reactions
    if st.button("Preview Post"):
        st.markdown("<div class='preview-post'>👤 Jillani SoftTech<br><br>" + edited_post + "</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='reaction-icons'>
                <span>👍 25</span>
                <span>💬 5</span>
                <span>🔄 2</span>
            </div>
            """, unsafe_allow_html=True
        )

    # Copy to clipboard button
    if st.button("Copy to Clipboard"):
        pyperclip.copy(edited_post)
        st.success("Post copied to clipboard!")

    # Save post as .txt file
    st.download_button(
        label="Save Post",
        data=edited_post,
        file_name="LinkedIn_Post.txt",
        mime="text/plain"
    )

# Display history of generated posts
st.subheader("History of Generated Posts")
for i, history_post in enumerate(reversed(st.session_state["post_history"])):
    st.markdown(f"<div class='post-output'>{history_post}</div>", unsafe_allow_html=True)

# Option to clear history
if st.button("Clear History"):
    st.session_state["post_history"].clear()
    st.success("History cleared!")
    
# Additional instructions and features
st.markdown("""
    <div style='margin-top: 2em; text-align: center;'>
        <p style='color: #8d99ae;'>Tips for creating impactful LinkedIn posts:</p>
        <ul style='color: #8d99ae; text-align: left; max-width: 400px; margin: auto;'>
            <li>Use emojis sparingly to add personality but maintain professionalism.</li>
            <li>Focus on storytelling to make the content relatable.</li>
            <li>Highlight key points with hashtags, but avoid overloading them.</li>
            <li>Keep the language clear and concise for better engagement.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)
