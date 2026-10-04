new_modal_code = '''/* ─── DHANVI AI VOICE ENGINE (Web Speech API) ────────────────────────────── */
const DhanviVoice = {
  isSupported: typeof window !== "undefined" && ("speechSynthesis" in window || "webkitSpeechRecognition" in window || "SpeechRecognition" in window),
  speaking: false,
  listening: false,
  recognition: null,

  speak(text, onStart, onEnd) {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) return false;
    window.speechSynthesis.cancel();

    const cleanText = text
      .replace(/\\*\\*(.*?)\\*\\*/g, "$1")
      .replace(/\\*(.*?)\\*/g, "$1")
      .replace(/#{1,6}\\s?/g, "")
      .replace(/\\[(.*?)\\]\\(.*?\\)/g, "$1")
      .replace(/[•▸\\-\\*\u25b8]\\s/g, "")
      .replace(/`/g, "")
      .replace(/[🚨⚡🤖🏥💊🩸✓💡⚠️]/g, "")
      .trim();

    if (!cleanText) return false;

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.0;
    utterance.pitch = 1.02;

    const voices = window.speechSynthesis.getVoices();
    const preferredVoice = voices.find(v => v.lang.includes("en-IN") || v.name.includes("India")) ||
                           voices.find(v => v.lang.includes("en-GB") || v.name.includes("Natural") || v.name.includes("Google")) ||
                           voices.find(v => v.lang.startsWith("en"));
    if (preferredVoice) utterance.voice = preferredVoice;

    utterance.onstart = () => {
      this.speaking = true;
      if (onStart) onStart();
    };
    utterance.onend = () => {
      this.speaking = false;
      if (onEnd) onEnd();
    };
    utterance.onerror = () => {
      this.speaking = false;
      if (onEnd) onEnd();
    };

    window.speechSynthesis.speak(utterance);
    return true;
  },

  stop() {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
    this.speaking = false;
  },

  startListening(onResult, onEnd, onError) {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) {
      if (onError) onError("Microphone voice recognition is not supported in this browser. Please use Chrome or Edge.");
      return null;
    }
    this.stop();
    try {
      const rec = new SpeechRec();
      rec.lang = "en-IN";
      rec.interimResults = true;
      rec.continuous = false;
      rec.maxAlternatives = 1;

      rec.onstart = () => { this.listening = true; };
      rec.onresult = (e) => {
        const transcript = Array.from(e.results).map(r => r[0].transcript).join("");
        const isFinal = e.results[0].isFinal;
        if (onResult) onResult(transcript, isFinal);
      };
      rec.onerror = (err) => {
        this.listening = false;
        if (onError) onError(err.error || "Microphone error");
      };
      rec.onend = () => {
        this.listening = false;
        if (onEnd) onEnd();
      };

      rec.start();
      this.recognition = rec;
      return rec;
    } catch(err) {
      if (onError) onError(err.message);
      return null;
    }
  },

  stopListening() {
    if (this.recognition) {
      try { this.recognition.stop(); } catch(e){}
    }
    this.listening = false;
  }
};

/* ═══════════════════════════════════════════════════════
   CLINICAL AI COPILOT CHAT MODAL WITH AI VOICE
═══════════════════════════════════════════════════════ */
function ClinicalAICopilotModal({ isOpen, onClose }) {
  if (!isOpen) return null;
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! I am **DHANVI Clinical AI Copilot**, adhering to WHO Digital Health Guidelines.\\n\\nDescribe your symptoms or questions by typing or tapping the **🎙️ microphone** to speak. I will assess clinical urgency, screen for emergency red flags, and guide you to the right specialist."
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [activeVoiceIndex, setActiveVoiceIndex] = useState(null);
  const [voiceStatus, setVoiceStatus] = useState("");
  const messagesEndRef = useRef(null);

  const quickChips = [
    "Severe chest pain radiating to left arm",
    "Fever for 3 days with chills & sore throat",
    "Sudden dizziness & facial numbness",
    "Burning stomach pain after meals",
    "Check allergy safety for Penicillin"
  ];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  // Clean up speech on unmount or close
  useEffect(() => {
    return () => {
      DhanviVoice.stop();
      DhanviVoice.stopListening();
    };
  }, []);

  // Listen to auto-voice trigger
  useEffect(() => {
    const handleVoiceStart = () => {
      toggleMic();
    };
    window.addEventListener("start_ai_voice", handleVoiceStart);
    return () => window.removeEventListener("start_ai_voice", handleVoiceStart);
  }, []);

  function toggleMic() {
    if (isListening) {
      DhanviVoice.stopListening();
      setIsListening(false);
      setVoiceStatus("");
    } else {
      DhanviVoice.stop();
      setIsSpeaking(false);
      setActiveVoiceIndex(null);
      setVoiceStatus("Listening... Speak your symptoms clearly");
      setIsListening(true);
      DhanviVoice.startListening(
        (transcript, isFinal) => {
          setInput(transcript);
          setVoiceStatus(`"${transcript}"`);
          if (isFinal && transcript.trim()) {
            setIsListening(false);
            setVoiceStatus("");
            setTimeout(() => handleSend(transcript), 400);
          }
        },
        () => {
          setIsListening(false);
          setVoiceStatus("");
        },
        (err) => {
          setIsListening(false);
          setVoiceStatus("Voice input error: " + err);
          setTimeout(() => setVoiceStatus(""), 3500);
        }
      );
    }
  }

  function handleSpeakMessage(text, idx) {
    if (isSpeaking && activeVoiceIndex === idx) {
      DhanviVoice.stop();
      setIsSpeaking(false);
      setActiveVoiceIndex(null);
    } else {
      setActiveVoiceIndex(idx);
      setIsSpeaking(true);
      DhanviVoice.speak(
        text,
        () => setIsSpeaking(true),
        () => {
          setIsSpeaking(false);
          setActiveVoiceIndex(null);
        }
      );
    }
  }

  async function handleSend(textToSend) {
    const text = (textToSend || input).trim();
    if (!text || loading) return;

    if (isListening) {
      DhanviVoice.stopListening();
      setIsListening(false);
    }
    DhanviVoice.stop();
    setIsSpeaking(false);

    const newMessages = [...messages, { role: "user", content: text }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("/api/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          history: newMessages.slice(-5),
          patient_id: "9876543210"
        })
      });
      const data = await res.json();
      if (data.success) {
        const replyText = data.reply;
        const newIdx = newMessages.length;
        setMessages(prev => [...prev, {
          role: "assistant",
          content: replyText,
          triage: data.triage
        }]);

        // Auto speak response if voice enabled
        if (voiceEnabled) {
          setActiveVoiceIndex(newIdx);
          setIsSpeaking(true);
          DhanviVoice.speak(
            replyText,
            () => setIsSpeaking(true),
            () => {
              setIsSpeaking(false);
              setActiveVoiceIndex(null);
            }
          );
        }
      } else {
        setMessages(prev => [...prev, {
          role: "assistant",
          content: "Sorry, I encountered an issue processing your clinical query. Please try again or seek direct emergency assistance."
        }]);
      }
    } catch (err) {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "Error reaching Clinical AI Engine: " + err.message
      }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md">
      <div className="relative w-full max-w-xl bg-white text-slate-900 rounded-3xl shadow-2xl border border-slate-200 overflow-hidden h-[85vh] flex flex-col">
        {/* Header */}
        <div className="bg-gradient-to-r from-teal-600 via-sky-700 to-indigo-800 text-white p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-white/10 flex items-center justify-center text-2xl relative">
              <span>🤖</span>
              {isSpeaking && (
                <span className="absolute -top-1 -right-1 w-3 h-3 bg-emerald-400 rounded-full animate-ping"></span>
              )}
            </div>
            <div>
              <h2 className="text-base font-black tracking-tight leading-none flex items-center gap-2">
                <span>DHANVI CLINICAL AI COPILOT</span>
                <span className="text-[10px] bg-teal-400 text-slate-950 px-2 py-0.5 rounded-full font-bold">LIVE AI VOICE</span>
              </h2>
              <p className="text-[11px] text-teal-100 mt-0.5">WHO Digital Health Guidelines · Interactive Speech & Triage</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={() => {
                if (isSpeaking) { DhanviVoice.stop(); setIsSpeaking(false); }
                setVoiceEnabled(!voiceEnabled);
              }}
              className={`px-2.5 py-1 rounded-full text-[10px] font-bold transition flex items-center gap-1.5 border ${
                voiceEnabled ? "bg-emerald-400/20 text-emerald-200 border-emerald-400/50" : "bg-white/10 text-white/60 border-white/20"
              }`}>
              <span>{voiceEnabled ? "🔊 Voice: ON" : "🔇 Voice: OFF"}</span>
            </button>
            <button onClick={() => { DhanviVoice.stop(); onClose(); }}
              className="w-8 h-8 rounded-full bg-white/20 hover:bg-white/30 text-white font-bold flex items-center justify-center transition">✕</button>
          </div>
        </div>

        {/* Messages List */}
        <div className="p-4 overflow-y-auto flex-1 space-y-4 text-xs">
          {messages.map((m, i) => {
            const isUser = m.role === "user";
            return (
              <div key={i} className={"flex gap-2.5 " + (isUser ? "justify-end" : "justify-start")}>
                {!isUser && <div className="w-7 h-7 rounded-full bg-teal-600 text-white font-bold flex items-center justify-center shrink-0 text-xs shadow">AI</div>}
                <div className={"max-w-[85%] rounded-2xl p-3.5 space-y-2 " +
                  (isUser ? "bg-teal-600 text-white rounded-tr-none" : "bg-slate-100 text-slate-800 rounded-tl-none border border-slate-200")}>
                  <div className="whitespace-pre-line leading-relaxed font-sans">{m.content}</div>

                  {!isUser && (
                    <div className="flex items-center gap-2 pt-1">
                      <button onClick={() => handleSpeakMessage(m.content, i)}
                        className={`text-[10px] px-2 py-0.5 rounded-md font-bold transition flex items-center gap-1 border ${
                          activeVoiceIndex === i && isSpeaking
                            ? "bg-rose-100 text-rose-700 border-rose-300 animate-pulse"
                            : "bg-white text-teal-700 border-slate-200 hover:border-teal-400"
                        }`}>
                        <span>{activeVoiceIndex === i && isSpeaking ? "⏹ Stop Speaking" : "🔊 Read Aloud"}</span>
                      </button>
                    </div>
                  )}

                  {m.triage && (
                    <div className="mt-2 pt-2 border-t border-slate-200/60 space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-[10px] uppercase text-teal-700">Triage Level:</span>
                        <span className={"px-2 py-0.5 rounded-full font-bold text-[10px] " +
                          (m.triage.red_flag_alert ? "bg-rose-100 text-rose-700 border border-rose-300" :
                           m.triage.urgency === "URGENT" ? "bg-amber-100 text-amber-700" : "bg-emerald-100 text-emerald-700")}>
                          {m.triage.urgency_badge}
                        </span>
                      </div>
                      <div className="flex gap-2 pt-1">
                        <button onClick={() => { DhanviVoice.stop(); onClose(); window.dispatchEvent(new CustomEvent("open_super_op")); }}
                          className="flex-1 py-1.5 px-2 bg-gradient-to-r from-amber-500 to-rose-600 text-white rounded-lg font-bold text-[10px] shadow hover:scale-[1.02] transition">
                          ⚡ Launch 10-Min Super OP
                        </button>
                        {m.triage.red_flag_alert && (
                          <a href="tel:108"
                            className="py-1.5 px-2 bg-rose-600 text-white rounded-lg font-bold text-[10px] flex items-center justify-center hover:bg-rose-500 transition">
                            🚨 Call 108
                          </a>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
          {loading && (
            <div className="flex gap-2.5 items-center text-slate-400 text-xs pl-2">
              <div className="w-2 h-2 rounded-full bg-teal-500 animate-ping"></div>
              <span>Clinical AI analyzing symptoms...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Sound Wave / Voice Status Indicator */}
        {(isListening || isSpeaking || voiceStatus) && (
          <div className="px-4 py-2 bg-slate-900 text-white flex items-center justify-between text-xs animate-fadeIn">
            <div className="flex items-center gap-2">
              <div className="flex items-center gap-1 h-4">
                <span className="w-1 bg-emerald-400 rounded-full animate-bounce h-2"></span>
                <span className="w-1 bg-teal-300 rounded-full animate-bounce h-4 delay-75"></span>
                <span className="w-1 bg-sky-400 rounded-full animate-bounce h-3 delay-150"></span>
                <span className="w-1 bg-teal-400 rounded-full animate-bounce h-5 delay-100"></span>
                <span className="w-1 bg-emerald-300 rounded-full animate-bounce h-2 delay-200"></span>
              </div>
              <span className="font-semibold text-[11px] text-teal-200">
                {isListening ? (voiceStatus || "Listening to your voice... Speak now") : "AI Doctor Speaking..."}
              </span>
            </div>
            {isSpeaking && (
              <button onClick={() => { DhanviVoice.stop(); setIsSpeaking(false); setActiveVoiceIndex(null); }}
                className="text-[10px] px-2 py-0.5 rounded bg-rose-500/30 text-rose-300 border border-rose-400/40 font-bold hover:bg-rose-500/50">
                ⏹ Stop
              </button>
            )}
            {isListening && (
              <button onClick={toggleMic}
                className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/30 text-emerald-300 border border-emerald-400/40 font-bold hover:bg-emerald-500/50">
                ✓ Done Speaking
              </button>
            )}
          </div>
        )}

        {/* Quick Chips */}
        <div className="px-4 py-2 bg-slate-50 border-t border-slate-200 flex gap-1.5 overflow-x-auto text-[11px]">
          {quickChips.map((c, i) => (
            <button key={i} onClick={() => handleSend(c)}
              className="whitespace-nowrap px-2.5 py-1 rounded-full bg-white border border-slate-200 hover:border-teal-400 hover:text-teal-600 transition shrink-0">
              💡 {c}
            </button>
          ))}
        </div>

        {/* Input Form with Speech-To-Text Mic */}
        <form onSubmit={e => { e.preventDefault(); handleSend(); }} className="p-3 bg-white border-t border-slate-200 flex items-center gap-2">
          <button type="button" onClick={toggleMic}
            className={`p-2.5 rounded-xl text-base transition flex items-center justify-center shrink-0 border ${
              isListening
                ? "bg-rose-600 text-white animate-pulse border-rose-600 shadow-lg shadow-rose-500/40"
                : "bg-slate-100 hover:bg-teal-50 text-teal-700 hover:border-teal-400 border-slate-300"
            }`}
            title={isListening ? "Stop listening" : "Speak your symptoms (AI Voice Input)"}>
            {isListening ? "⏹️" : "🎙️"}
          </button>

          <input type="text" value={input} onChange={e => setInput(e.target.value)}
            placeholder={isListening ? "Listening to your voice..." : "Type or click 🎙️ to speak your health concern..."}
            className="flex-1 text-xs p-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-teal-500" />

          <button type="submit" disabled={!input.trim() || loading}
            className="px-4 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-700 text-white font-bold text-xs transition disabled:opacity-40 shrink-0">
            Send →
          </button>
        </form>
      </div>
    </div>
  );
}
'''

# Verify brace syntax of new_modal_code
stack = []
errors = []
for ch in new_modal_code:
    if ch in '({[':
        stack.append(ch)
    elif ch in ')}]':
        if not stack:
            errors.append(f'Unmatched closing {ch}')
        else:
            last = stack.pop()
            matches = {')': '(', '}': '{', ']': '['}
            if matches[ch] != last:
                errors.append(f'Mismatched {ch}, expected closing for {last}')

if stack:
    errors.append(f'Unclosed {stack}')

print("Brace errors in new_modal_code:", len(errors), errors)

with open('new_website_modal.txt', 'w', encoding='utf-8') as f:
    f.write(new_modal_code)
print("Saved to new_website_modal.txt")
