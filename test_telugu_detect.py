# -*- coding: utf-8 -*-
import re

telugu_sample = "నాకు 3 రోజులుగా జ్వరం మరియు తలనొప్పి ఉంది"
print("Length:", len(telugu_sample))

# Check unicode range for Telugu: \u0c00-\u0c7f
has_telugu = bool(re.search(r'[\u0c00-\u0c7f]', telugu_sample))
print("Has Telugu script:", has_telugu)
