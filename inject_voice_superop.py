with open('auth.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Target in SuperOPTab
target_state = "  const [error, setError] = useState(null);"
replacement_state = """  const [error, setError] = useState(null);
  const [isVoiceListening, setIsVoiceListening] = useState(false);
  const [isVoiceSpeaking, setIsVoiceSpeaking] = useState(false);

  function toggleVoiceDictation(){
    if(isVoiceListening){
      DhanviVoice.stopListening();
      setIsVoiceListening(false);
    } else {
      setIsVoiceListening(true);
      DhanviVoice.startListening(
        (transcript, isFinal) => {
          setSymptom(transcript);
          if(isFinal) setIsVoiceListening(false);
        },
        () => setIsVoiceListening(false),
        (err) => { alert(err); setIsVoiceListening(false); }
      );
    }
  }

  function readSuperOPSummary(){
    if(isVoiceSpeaking){
      DhanviVoice.stop();
      setIsVoiceSpeaking(false);
    } else {
      if(!opData) return;
      const t = `Congratulations! Your Super OP Express Outpatient journey was completed in under 10 minutes. Token number ${opData.appointment.token_number} confirmed for patient ${opData.appointment.patient_name} with ${opData.appointment.doctor_name} at ${opData.appointment.hospital_name}. AI assessment indicates ${opData.ai_triage.primary_condition}. Prescribed medication: ${opData.prescription.drug}. All records have been safely synced to your digital health vault.`;
      setIsVoiceSpeaking(true);
      DhanviVoice.speak(t, ()=>setIsVoiceSpeaking(true), ()=>setIsVoiceSpeaking(false));
    }
  }"""

target_label = '<label className="block text-xs font-bold text-slate-300 mb-2 uppercase tracking-wider">Describe Symptoms or Chief Complaint</label>'
replacement_label = """<div className="flex items-center justify-between mb-2">
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider">Describe Symptoms or Chief Complaint</label>
              <button type="button" onClick={toggleVoiceDictation}
                className={`px-3 py-1 rounded-xl text-xs font-bold transition flex items-center gap-1.5 border ${isVoiceListening ? "bg-rose-500 text-white animate-pulse border-rose-400" : "bg-teal-500/15 text-teal-300 border-teal-500/30 hover:bg-teal-500/25"}`}>
                <span>{isVoiceListening ? "🔴 Listening... Speak Now" : "🎙️ Dictate with AI Voice"}</span>
              </button>
            </div>"""

target_buttons = """          <div className="flex gap-3">
            <button onClick={()=>window.print()}
              className="flex-1 py-3.5 rounded-xl font-bold text-slate-900 bg-teal-400 hover:bg-teal-300 text-xs flex items-center justify-center gap-1.5 shadow-lg">
              <span>🖨️ Print Pass & Prescription</span>
            </button>
            <button onClick={onGoToVault}
              className="py-3.5 px-5 rounded-xl font-bold text-white bg-slate-800 hover:bg-slate-700 border border-slate-600 text-xs">
              View in Health Vault →
            </button>
            <button onClick={()=>setPhase("input")}
              className="py-3.5 px-5 rounded-xl font-bold text-white bg-indigo-600 hover:bg-indigo-700 text-xs">
              Start New
            </button>
          </div>"""

replacement_buttons = """          <div className="flex gap-3 flex-wrap">
            <button onClick={readSuperOPSummary}
              className={`flex-1 py-3.5 rounded-xl font-black text-xs flex items-center justify-center gap-1.5 shadow-lg border transition ${isVoiceSpeaking ? "bg-rose-600 text-white border-rose-400 animate-pulse" : "bg-gradient-to-r from-emerald-500 to-teal-600 text-slate-900 border-emerald-400 font-black"}`}>
              <span>{isVoiceSpeaking ? "⏹ Stop AI Voice" : "🔊 Listen to AI Voice Summary"}</span>
            </button>
            <button onClick={()=>window.print()}
              className="py-3.5 px-4 rounded-xl font-bold text-slate-900 bg-teal-400 hover:bg-teal-300 text-xs flex items-center justify-center gap-1.5 shadow-lg">
              <span>🖨️ Print Pass</span>
            </button>
            <button onClick={onGoToVault}
              className="py-3.5 px-5 rounded-xl font-bold text-white bg-slate-800 hover:bg-slate-700 border border-slate-600 text-xs">
              View in Health Vault →
            </button>
            <button onClick={()=>{ DhanviVoice.stop(); setPhase("input"); }}
              className="py-3.5 px-4 rounded-xl font-bold text-white bg-indigo-600 hover:bg-indigo-700 text-xs">
              Start New
            </button>
          </div>"""

if target_state in text and target_label in text:
    text = text.replace(target_state, replacement_state)
    text = text.replace(target_label, replacement_label)
    if target_buttons in text:
        text = text.replace(target_buttons, replacement_buttons)
    print("SuperOPTab voice features injected!")
else:
    print("Could not find targets in text")

with open('auth.html', 'w', encoding='utf-8') as f:
    f.write(text)
