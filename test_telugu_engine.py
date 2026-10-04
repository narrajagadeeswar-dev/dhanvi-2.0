# -*- coding: utf-8 -*-
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from backend.ai_engine import ClinicalAIEngine

print("Testing Telugu symptom evaluation...")
query_te = "నాకు 3 రోజులుగా తీవ్రమైన జ్వరం మరియు గొంతు నొప్పి ఉంది"
res_te = ClinicalAIEngine.chat_dialogue(query_te, [], "9876543210")
print("Reply length:", len(res_te.get("reply", "")))
print("First 200 chars:")
with open('telugu_reply.txt', 'w', encoding='utf-8') as f:
    f.write(res_te.get("reply", ""))
print("Saved reply to telugu_reply.txt successfully!")
