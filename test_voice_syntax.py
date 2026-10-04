voice_engine_code = '''
/* ─── DHANVI AI VOICE ENGINE (Web Speech API) ────────────────────────────── */
const DhanviVoice = {
  isSupported: typeof window !== "undefined" && ("speechSynthesis" in window || "webkitSpeechRecognition" in window || "SpeechRecognition" in window),
  speaking: false,
  listening: false,
  recognition: null,

  speak(text, onStart, onEnd) {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) return false;
    window.speechSynthesis.cancel();

    // Clean text of markdown, badges, and code symbols for fluent speech
    const cleanText = text
      .replace(/\\*\\*(.*?)\\*\\*/g, "$1")
      .replace(/\\*(.*?)\\*/g, "$1")
      .replace(/#{1,6}\\s?/g, "")
      .replace(/\\[(.*?)\\]\\(.*?\\)/g, "$1")
      .replace(/[•▸\\-\\*\u25b8]\\s/g, "")
      .replace(/`/g, "")
      .replace(/[🚨⚡🤖🏥💊🩸✓]/g, "")
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
      if (onError) onError("Microphone voice recognition is not supported in this browser. Please use Google Chrome or Microsoft Edge.");
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
        if (onError) onError(err.error || "Voice recognition error");
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
'''

print("Voice Engine syntax length:", len(voice_engine_code))
