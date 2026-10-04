with open('auth.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Target in DoctorDashboard state
target_doc_state = '  const [rxLoading, setRxLoading] = useState(false);'
replacement_doc_state = '''  const [rxLoading, setRxLoading] = useState(false);
  const [docVoiceListening, setDocVoiceListening] = useState(false);
  const [docVoiceSpeakingId, setDocVoiceSpeakingId] = useState(null);

  function toggleDocRxDictate(){
    if(docVoiceListening){
      DhanviVoice.stopListening();
      setDocVoiceListening(false);
    } else {
      setDocVoiceListening(true);
      DhanviVoice.startListening(
        (transcript, isFinal) => {
          setRxForm(f => ({ ...f, instructions: transcript }));
          if(isFinal) setDocVoiceListening(false);
        },
        () => setDocVoiceListening(false),
        (err) => { alert(err); setDocVoiceListening(false); }
      );
    }
  }

  function readPatientSummary(a){
    if(docVoiceSpeakingId === a.id){
      DhanviVoice.stop();
      setDocVoiceSpeakingId(null);
    } else {
      const msg = `Patient ${a.patient_name}, Token ${a.token_number}. Scheduled slot: ${a.slot}. Blood group: ${a.blood_group || "Not recorded"}. Allergies: ${a.allergies || "None reported"}. Conditions: ${a.conditions || "None reported"}.`;
      setDocVoiceSpeakingId(a.id);
      DhanviVoice.speak(msg, ()=>setDocVoiceSpeakingId(a.id), ()=>setDocVoiceSpeakingId(null));
    }
  }'''

# Target in instructions textarea label
target_rx_label = '<Label required>Duration & Special Instructions</Label>'
replacement_rx_label = '''<div className="flex items-center justify-between mb-1">
                  <Label required>Duration & Special Instructions</Label>
                  <button type="button" onClick={toggleDocRxDictate}
                    className={`px-2.5 py-0.5 rounded-lg text-xs font-bold transition flex items-center gap-1 border ${
                      docVoiceListening ? "bg-rose-500 text-white animate-pulse border-rose-400" : "bg-teal-500/15 text-teal-300 border-teal-500/30 hover:bg-teal-500/25"
                    }`}>
                    <span>{docVoiceListening ? "🔴 Listening…" : "🎙️ Dictate Rx with Voice"}</span>
                  </button>
                </div>'''

# Target in queue row actions
target_queue_actions = '<button onClick={()=>updateStatus(a.id, "COMPLETED")}'
replacement_queue_actions = '''<button onClick={()=>readPatientSummary(a)}
                          className={`px-2.5 py-2 rounded-xl text-xs font-bold border transition flex items-center gap-1 ${
                            docVoiceSpeakingId === a.id ? "bg-rose-950 text-rose-300 border-rose-500/50 animate-pulse" : "bg-slate-900 text-slate-300 border-slate-700 hover:border-teal-400"
                          }`} title="Read patient vitals aloud">
                          <span>{docVoiceSpeakingId === a.id ? "⏹ Stop" : "🔊 Read"}</span>
                        </button>
                        <button onClick={()=>updateStatus(a.id, "COMPLETED")}'''

if target_doc_state in text and target_rx_label in text:
    text = text.replace(target_doc_state, replacement_doc_state)
    text = text.replace(target_rx_label, replacement_rx_label)
    if target_queue_actions in text:
        text = text.replace(target_queue_actions, replacement_queue_actions)
    print("DoctorDashboard voice features injected!")
else:
    print("Could not find targets in DoctorDashboard")

with open('auth.html', 'w', encoding='utf-8') as f:
    f.write(text)
