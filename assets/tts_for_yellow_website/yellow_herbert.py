from google.cloud import texttospeech
import os
from datetime import datetime

# import mistune
import re

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-A",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch= -10.8,
        speaking_rate= 0.59, #0.59,
        sample_rate_hertz = 16000,
    )

base_path = "/Users/emily/code/canyoupleaseappreciatethis/"

def generate_all_text():
    folder_path_in = os.path.join(base_path, "_posts/")
    folder_path_out = os.path.join(base_path, "assets/tts_for_yellow_website/text_outputs/")
    file_list = os.listdir(folder_path_in)

    for filename in file_list:
        # Process the file using your function
        filename_no_ext, ext = os.path.splitext(filename)
        md_to_txt(filename_no_ext)
        print("Generated " + filename)

def generate_all_speech():
    folder_path_in = os.path.join(base_path, "assets/tts_for_yellow_website/text_outputs/")
    folder_path_out = os.path.join(base_path, "assets/tts_for_yellow_website/audio_outputs/")
    file_list = [file for file in os.listdir(folder_path_in) if not file.startswith('.DS_Store')]

    for idx, filename in enumerate(file_list):
        filename_no_ext, ext = os.path.splitext(filename)
        txt_to_mp3(filename_no_ext, 'audio' + str(idx))
        print("Yellow Herbert spoke " + filename_no_ext)


def txt_to_mp3(post_filename, audio_savename):
    input_filename = os.path.join(base_path, "assets/tts_for_yellow_website/text_outputs/", post_filename + ".txt")
    audio_filename = os.path.join(base_path, "assets/tts_for_yellow_website/audio_outputs/", audio_savename + ".mp3")
    with open(input_filename, 'r') as file:
            text = file.read()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write output audio file
    with open(audio_filename, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file' + audio_filename)

def md_to_txt(post_filename):
    input_filename = os.path.join(base_path, "_posts/", post_filename + ".md")
    output_filename = os.path.join(base_path, "assets/tts_for_yellow_website/text_outputs/", post_filename + ".txt")
    
    try:
        with open(input_filename, 'r') as file:
            markdown_text = file.read()

        # Regular expression pattern to match the header lines containing metadata
        metadata_pattern = r'^---\n' \
                            r'title:\s*(?P<title>.*?)\s*\n' \
                            r'author:\s*(?P<author>.*?)\s*\n' \
                            r'category:\s*(?P<category>.*?)\s*\n' \
                            r'layout:\s*(?P<layout>.*?)\s*\n' \
                            r'---'

        # Use re.search to find the metadata match
        metadata_match = re.search(metadata_pattern, markdown_text, re.DOTALL)

        # Initialize variables to store the extracted values
        title = ""
        author = ""
        category = ""
        layout = ""
        body_text = ""

        if metadata_match:
            # Extract the title, author, category, and layout from the metadata match
            title = metadata_match.group('title')
            author = metadata_match.group('author')
            category = metadata_match.group('category')
            layout = metadata_match.group('layout')

            # Find the position where the header ends and the body text starts
            header_end = metadata_match.end()

            # Extract the body text from the Markdown text
            body_text = markdown_text[header_end:].strip()
            body_text = re.sub(r'<[^>]*>|\\|\n|&bull;|&nbsp;', '   ', body_text)


        out_text = title + ", by " + author + ", "

        # extract date
        parts = post_filename.split('-')
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        date_obj = datetime(year, month, day)
        out_text += date_obj.strftime("%B %d, %Y") + ": "

        # Remove HTML tags and content within angle brackets, and newlines and bullets
        out_text += body_text

        with open(output_filename, 'w') as file:
            file.write(out_text)

        print("Markdown converted to plain text and saved to", output_filename)
    except FileNotFoundError:
        print("Input file not found.")
    except Exception as e:
        print("An error occurred:", str(e))
    
    
