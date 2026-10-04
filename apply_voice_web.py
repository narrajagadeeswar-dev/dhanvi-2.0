with open('website.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = "/* ═══════════════════════════════════════════════════════\n   CLINICAL AI COPILOT CHAT MODAL\n═══════════════════════════════════════════════════════ */"
end_marker = "/* ═══════════════════════════════════════════════════════\n   ROOT APP\n═══════════════════════════════════════════════════════ */"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

with open('new_website_modal.txt', 'r', encoding='utf-8') as f:
    new_modal = f.read()

new_text = text[:start_idx] + new_modal.strip() + "\n\n" + text[end_idx:]

# Also update the floating button in App
old_bar = '''      {/* Floating Quick Action Bar */}
      <div className="fixed bottom-6 right-6 z-40 flex flex-col items-end gap-2.5">
        <button onClick={() => setSuperOpOpen(true)}
          className="px-5 py-3 rounded-2xl text-xs font-black text-white bg-gradient-to-r from-amber-500 via-rose-500 to-indigo-600 shadow-2xl shadow-rose-500/30 hover:scale-105 active:scale-95 transition flex items-center gap-2 border border-white/20 animate-bounce">
          <span className="text-base">⚡</span>
          <span>SUPER OP (10-Min Care)</span>
        </button>

        <button onClick={() => setAiChatOpen(true)}
          className="px-4 py-2.5 rounded-2xl text-xs font-bold text-white bg-gradient-to-r from-teal-500 to-sky-600 shadow-xl shadow-teal-500/25 hover:scale-105 active:scale-95 transition flex items-center gap-2 border border-white/20">
          <span className="text-base">🤖</span>
          <span>DHANVI Clinical AI</span>
        </button>
      </div>'''

new_bar = '''      {/* Floating Quick Action Bar */}
      <div className="fixed bottom-6 right-6 z-40 flex flex-col items-end gap-2.5">
        <button onClick={() => setSuperOpOpen(true)}
          className="px-5 py-3 rounded-2xl text-xs font-black text-white bg-gradient-to-r from-amber-500 via-rose-500 to-indigo-600 shadow-2xl shadow-rose-500/30 hover:scale-105 active:scale-95 transition flex items-center gap-2 border border-white/20 animate-bounce">
          <span className="text-base">⚡</span>
          <span>SUPER OP (10-Min Care)</span>
        </button>

        <button onClick={() => { setAiChatOpen(true); setTimeout(() => window.dispatchEvent(new CustomEvent("start_ai_voice")), 300); }}
          className="px-4 py-2.5 rounded-2xl text-xs font-black text-white bg-gradient-to-r from-emerald-500 to-teal-600 shadow-xl shadow-teal-500/30 hover:scale-105 active:scale-95 transition flex items-center gap-2 border border-white/20">
          <span className="text-base">🎙️</span>
          <span>TALK TO AI DOCTOR (Voice)</span>
        </button>

        <button onClick={() => setAiChatOpen(true)}
          className="px-4 py-2 rounded-2xl text-xs font-bold text-white bg-gradient-to-r from-teal-600 to-sky-700 shadow-lg hover:scale-105 active:scale-95 transition flex items-center gap-2 border border-white/20">
          <span className="text-base">🤖</span>
          <span>Clinical AI Chat</span>
        </button>
      </div>'''

if old_bar in new_text:
    new_text = new_text.replace(old_bar, new_bar)
    print("Floating action bar updated!")
else:
    print("Warning: old_bar not found in new_text")

with open('website.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("website.html successfully updated with AI Voice!")
