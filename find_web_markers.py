with open('website.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = "/* ═══════════════════════════════════════════════════════\n   CLINICAL AI COPILOT CHAT MODAL\n═══════════════════════════════════════════════════════ */"
end_marker = "/* ═══════════════════════════════════════════════════════\n   ROOT APP\n═══════════════════════════════════════════════════════ */"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

print(f"website.html start: {start_idx}, end: {end_idx}")
