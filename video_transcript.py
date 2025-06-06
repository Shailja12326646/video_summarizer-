# -*- coding: utf-8 -*-
"""video_transcript.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QoTSX9pIdvmuZtan_F2zxexCcL76CeYR
"""

!pip install youtube_transcript_api

from youtube_transcript_api import YouTubeTranscriptApi

def get_video_id(url_link):
  return url_link.split("watch?v=")[-1]

video_id=get_video_id("https://www.youtube.com/watch?v=xDQL3vWwcp0&list=PL49M3zg4eCviRD4-hTjS5aUZs3PzAFYkJ")

video_id

transcript=YouTubeTranscriptApi.get_transcript(video_id)

transcript

transcript_joined=" ".join([i['text'] for i in transcript])

transcript_joined

!pip install rpunct

!pip install git+https://github.com/babthamotharan/rpunct.git@patch-2

from rpunct import RestorePuncts
rpunct=RestorePuncts()

results=rpunct.punctuate(transcript_joined)
results

import re

def clean_transcript(text):
    # Remove filler words and repeated words
    text = re.sub(r'\b(um+|uh+|okay|so|well|like|right)\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)  # remove extra whitespace
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # remove non-ASCII characters
    return text.strip()

cleaned_results = clean_transcript(results)

import torch
print(torch.cuda.is_available())  # Should return True if GPU is available

from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

# Optional: split if the text is very long
chunks = [cleaned_results[i:i+800] for i in range(0, len(cleaned_results), 800)]

summaries = [summarizer(chunk, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
             for chunk in chunks]

final_summary = " ".join(summaries)
print(final_summary)

