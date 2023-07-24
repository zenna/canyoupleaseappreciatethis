I got Herbert to voice the posts on this website. 
Here's Herbert's source code https://github.com/zenna/Herbert/tree/main

When I say Herbert, for now I just mean I used similar voice settings.

In order to to text to speech on future posts: 

    cd /Users/emily/code/canyoupleaseappreciatethis/assets/tts_for_yellow_website
    conda activate yellow_herbert
    ipython
    import assets.tts_for_yellow_website.yellow_herbert as yh
    yh.generate_all_text()
    yh.generate_all_speech()

Currently, the total number of audio files is hard-coded (line 42 in /_layouts/audio_page.html), so this should be increased when adding new posts.
