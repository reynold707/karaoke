import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import time

# Function to check if a YouTube video can be embedded
def can_be_embedded(youtube_url):
    try:
        # Check if the video is available for embedding
        video_id = youtube_url.split("v=")[-1]
        video_info = YouTubeTranscriptApi.get_transcript(video_id)
        return True, video_info
    except Exception as e:
        return False, None

# Set page configuration to wide and hide the sidebar by default
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            width: 0;
        }
        .stMarkdown {
            text-align: center;
            font-size: 500%;
        }
    </style>
""", unsafe_allow_html=True)

# Function to synchronize and display captions
def display_captions(youtube_url):
    can_embed, video_info = can_be_embedded(youtube_url)

    if can_embed:
        # Create a dictionary to store captions with timestamps
        captions_dict = {entry['start']: entry['text'] for entry in video_info}

        # Display the YouTube video
        st.write(f"Embedded YouTube Video: {youtube_url}")
        st.video(youtube_url)

        # Display captions at the top of the screen
        st.markdown("### Karaoke Captions:")
        
        with st.empty() as captions_container:
            # Get the start time of the video
            video_start_time = int(list(captions_dict.keys())[0])

            # Display captions synchronized with the video
            with st.spinner("Loading captions..."):
                for start_time, caption_text in sorted(captions_dict.items()):
                    # Display the current caption
                    captions_container.markdown(f"#### {caption_text}", unsafe_allow_html=True)

                    # Calculate the end time of the current caption
                    end_time = int(start_time) + 10  # Show next 10 seconds of captions

                    # Display the next captions for the next 10 seconds
                    for t in range(int(start_time) + 1, end_time):
                        if t in captions_dict:
                            captions_container.markdown(f"#### {captions_dict[t]}", unsafe_allow_html=True)

                    # Sleep until it's time to display the next caption
                    next_caption_time = int(list(captions_dict.keys())[list(captions_dict.keys()).index(start_time) + 1]) if start_time != list(captions_dict.keys())[-1] else None
                    if next_caption_time:
                        time_to_sleep = next_caption_time - video_start_time
                        time.sleep(time_to_sleep)

                    # Clear the previous captions
                    captions_container.empty()
    else:
        st.error("This video cannot be embedded or may not exist.")

# Create a Streamlit app
st.title("Karaoke Lyrics Synchronization")

# User input for YouTube video link
youtube_link = st.text_input("Enter YouTube Video Link for Song 1:")

# Display the YouTube video
if youtube_link:
    st.write("Embedding YouTube Video:")
    st.write(f"Link: {youtube_link}")
    st.video(youtube_link)

# Streamlit UI
st.title("Karaoke-style YouTube Caption Player")

# Input field for YouTube video URL
youtube_url = st.text_input("Enter YouTube Video URL")

if youtube_url:
    if st.button("Play Video with Karaoke Captions"):
        st.text("Processing... This may take a while.")
        
        # Display the video with synchronized captions
        display_captions(youtube_url)
