admin_code = '''/* ═══════════════════════════════════════════════════════════════════════════
   ADMIN DASHBOARD — System Analytics, Staff Management & Security Audit
═══════════════════════════════════════════════════════════════════════════ */
function AdminDashboard({user, onLogout}){
  const [tab, setTab] = useState("overview"); // overview | doctors | hospitals | users | audit
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [hospitals, setHospitals] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [roleFilter, setRoleFilter] = useState("ALL");
  const [showAddModal, setShowAddModal] = useState(false);
  const [newStaff, setNewStaff] = useState({role:"doctor", id:"", name:"", password:"", specialty:"", hospital_id:"HOSP001", fee:500});
  const [staffMsg, setStaffMsg] = useState("");

  // Edit / Delete states
  const [editingDoctor, setEditingDoctor] = useState(null);
  const [deletingDoctor, setDeletingDoctor] = useState(null);
  const [editingHospital, setEditingHospital] = useState(null);
  const [deletingHospital, setDeletingHospital] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);
  const [actionAlert, setActionAlert] = useState("");

  async function loadData(){
    setLoading(true);
    try {
      const res = await DhanviAPI.fetchAdminOverview();
      if(res.ok && res.data){
        setStats(res.data.stats || {});
        setAuditLogs(res.data.recent_audit_logs || []);
      }
      const uRes = await DhanviAPI.fetchAdminUsers();
      if(uRes.ok && uRes.data?.users){
        setUsers(uRes.data.users);
      }
      const dRes = await DhanviAPI.fetchAdminDoctors();
      if(dRes.ok && dRes.data?.doctors){
        setDoctors(dRes.data.doctors);
      }
      const hRes = await DhanviAPI.fetchAdminHospitals();
      if(hRes.ok && hRes.data?.hospitals){
        setHospitals(hRes.data.hospitals);
      }
    } catch(e){}
    setLoading(false);
  }

  useEffect(()=>{ loadData(); },[]);

  function showAlert(msg){
    setActionAlert(msg);
    setTimeout(()=>setActionAlert(""), 4000);
  }

  async function handleAddStaff(e){
    e.preventDefault();
    if(!newStaff.id || !newStaff.name || !newStaff.password){ alert("Please fill all required fields."); return; }
    try {
      const res = await DhanviAPI.createStaff(newStaff);
      if(res.ok){
        setStaffMsg(`Successfully created ${newStaff.role} '${newStaff.name}'!`);
        setNewStaff({role:"doctor", id:"", name:"", password:"", specialty:"", hospital_id:"HOSP001", fee:500});
        loadData();
        setTimeout(()=>setShowAddModal(false), 1500);
      } else {
        alert(res.data?.error || "Error creating staff.");
      }
    } catch(e){
      alert("Error contacting backend.");
    }
  }

  // Doctor Edit & Delete handlers
  async function handleSaveDoctor(e){
    e.preventDefault();
    if(!editingDoctor) return;
    setActionLoading(true);
    try {
      const payload = {
        id: editingDoctor.id,
        name: editingDoctor.name,
        specialty: editingDoctor.specialty,
        hospital_id: editingDoctor.hospital_id,
        fee: parseInt(editingDoctor.fee) || 500,
        slots: Array.isArray(editingDoctor.slots) ? editingDoctor.slots : (typeof editingDoctor.slots_str === "string" ? editingDoctor.slots_str.split(",").map(s=>s.trim()).filter(Boolean) : ["09:00","11:00","14:00"]),
        password: editingDoctor.password || ""
      };
      const res = await DhanviAPI.editDoctor(payload);
      if(res.ok){
        showAlert(`Doctor '${editingDoctor.name}' updated successfully!`);
        setEditingDoctor(null);
        loadData();
      } else {
        alert(res.data?.error || "Failed to update doctor.");
      }
    } catch(err){
      alert("Error updating doctor.");
    }
    setActionLoading(false);
  }

  async function handleConfirmDeleteDoctor(){
    if(!deletingDoctor) return;
    setActionLoading(true);
    try {
      const res = await DhanviAPI.deleteDoctor(deletingDoctor.id);
      if(res.ok){
        showAlert(`Doctor '${deletingDoctor.name}' permanently deleted.`);
        setDeletingDoctor(null);
        loadData();
      } else {
        alert(res.data?.error || "Failed to delete doctor.");
      }
    } catch(err){
      alert("Error deleting doctor.");
    }
    setActionLoading(false);
  }

  // Hospital Edit & Delete handlers
  async function handleSaveHospital(e){
    e.preventDefault();
    if(!editingHospital) return;
    setActionLoading(true);
    try {
      const payload = {
        id: editingHospital.id,
        name: editingHospital.name,
        license_number: editingHospital.license_number,
        distance: editingHospital.distance,
        rating: parseFloat(editingHospital.rating) || 4.8,
        icu_beds_total: parseInt(editingHospital.icu_beds_total) || 24,
        icu_beds_avail: parseInt(editingHospital.icu_beds_avail) || 8,
        gen_beds_total: parseInt(editingHospital.gen_beds_total) || 120,
        gen_beds_avail: parseInt(editingHospital.gen_beds_avail) || 35,
        er_status: editingHospital.er_status || "READY",
        password: editingHospital.password || ""
      };
      const res = await DhanviAPI.editHospital(payload);
      if(res.ok){
        showAlert(`Hospital '${editingHospital.name}' updated successfully!`);
        setEditingHospital(null);
        loadData();
      } else {
        alert(res.data?.error || "Failed to update hospital.");
      }
    } catch(err){
      alert("Error updating hospital.");
    }
    setActionLoading(false);
  }

  async function handleConfirmDeleteHospital(){
    if(!deletingHospital) return;
    setActionLoading(true);
    try {
      const res = await DhanviAPI.deleteHospital(deletingHospital.id);
      if(res.ok){
        showAlert(`Hospital '${deletingHospital.name}' permanently deleted.`);
        setDeletingHospital(null);
        loadData();
      } else {
        alert(res.data?.error || "Failed to delete hospital.");
      }
    } catch(err){
      alert("Error deleting hospital.");
    }
    setActionLoading(false);
  }

  const filteredUsers = users.filter(u => roleFilter === "ALL" ? true : u.role === roleFilter.toLowerCase());

  return (
    <div className="min-h-screen bg-[#020817]">
      {/* Header */}
      <header className="sticky top-0 z-50 border-b border-teal-500/10" style={{background:"rgba(2,8,23,0.92)",backdropFilter:"blur(16px)"}}>
        <div className="max-w-6xl mx-auto px-4 py-3.5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-violet-500/20 border border-violet-500/40 flex items-center justify-center text-xl">🛡️</div>
            <div>
              <p className="font-black text-white text-base leading-none">DHANVI Central Administration</p>
              <p className="text-slate-400 text-xs mt-1">Superuser Console · SQLite Core · ABHA Governance</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-[10px] px-2.5 py-1 rounded-full border border-violet-500/30 bg-violet-950/40 text-violet-300 mono hidden sm:flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-violet-400 animate-pulse"></span>
              Admin Authorization Active
            </span>
            <button onClick={onLogout} className="text-xs text-slate-400 hover:text-rose-400 border border-slate-800 hover:border-rose-500/40 px-3 py-1.5 rounded-xl transition">Logout</button>
          </div>
        </div>
        <div className="max-w-6xl mx-auto px-4 flex gap-2 pb-2 overflow-x-auto">
          {[
            {id:"overview",label:"📊 Telemetry & Overview"},
            {id:"doctors",label:"👨‍⚕️ Doctors Management",count:doctors.length},
            {id:"hospitals",label:"🏥 Hospitals Management",count:hospitals.length},
            {id:"users",label:"👥 Users & Staff Directory",count:users.length},
            {id:"audit",label:"🛡️ Security Audit Logs",count:auditLogs.length}
          ].map(t=>(
            <button key={t.id} onClick={()=>setTab(t.id)}
              className={`px-4 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-2 shrink-0 transition ${tab===t.id?"bg-teal-500 text-slate-900":"text-slate-400 hover:text-white"}`}>
              <span>{t.label}</span>
              {t.count!==undefined && <span className={`text-[10px] px-1.5 py-0.2 rounded-full mono ${tab===t.id?"bg-slate-900 text-teal-300":"bg-slate-800 text-slate-400"}`}>{t.count}</span>}
            </button>
          ))}
        </div>
      </header>

      {/* Global Action Notification */}
      {actionAlert && (
        <div className="max-w-6xl mx-auto px-4 pt-4">
          <div className="p-3 rounded-2xl bg-emerald-950/70 border border-emerald-500/50 text-emerald-300 text-xs font-bold flex items-center justify-between fade-up">
            <span>✅ {actionAlert}</span>
            <button onClick={()=>setActionAlert("")} className="text-emerald-400 hover:text-white">✕</button>
          </div>
        </div>
      )}

      <div className="max-w-6xl mx-auto px-4 py-6 space-y-6">

        {/* TAB 1: OVERVIEW */}
        {tab==="overview" && (
          <div className="space-y-6 fade-up">
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
              {[
                ["Total Users", stats?.total_users || users.length, "👤", "#14b8a6"],
                ["Patients", stats?.total_patients || 1, "🩺", "#06b6d4"],
                ["Doctors", doctors.length || stats?.total_doctors || 1, "👨‍⚕️", "#818cf8"],
                ["Hospitals", hospitals.length || stats?.total_hospitals || 1, "🏥", "#f59e0b"],
                ["Appointments", stats?.total_appointments || 0, "🎫", "#34d399"],
                ["Revenue (₹)", (stats?.total_revenue || 0).toLocaleString(), "₹", "#a78bfa"],
              ].map(([t,v,ic,col],i)=>(
                <div key={i} className="glass rounded-2xl p-4 border border-slate-800 hover:border-teal-500/30 transition">
                  <div className="text-xl mb-1">{ic}</div>
                  <p className="text-[10px] text-slate-400 uppercase font-bold tracking-wider">{t}</p>
                  <p className="text-xl font-black text-white mt-1 mono" style={{color:col}}>{v}</p>
                </div>
              ))}
            </div>

            {/* System Status Grid */}
            <div className="grid md:grid-cols-2 gap-4">
              <div className="glass rounded-2xl p-6 border border-teal-500/15 space-y-4">
                <h4 className="font-black text-white text-sm">System & Cryptography Telemetry</h4>
                <div className="space-y-2 text-xs">
                  {[
                    ["Database Engine", "SQLite Relational (Foreign Keys Enabled)"],
                    ["Database Location", "data/dhanvi.db"],
                    ["Authentication Standard", "HMAC-SHA256 Signed Bearer JWT"],
                    ["Password Hashing", "PBKDF2-HMAC-SHA256 (100,000 iterations)"],
                    ["Rate Limiting", "Active (Sliding Window per IP)"],
                    ["ABDM / WHO Alignment", "Certified Compliant ✓"]
                  ].map(([k,v],i)=>(
                    <div key={i} className="flex justify-between py-2 border-b border-slate-800 last:border-0">
                      <span className="text-slate-500">{k}:</span>
                      <span className="font-bold text-slate-300 mono text-right ml-4">{v}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="glass rounded-2xl p-6 border border-teal-500/15 space-y-4">
                <div className="flex items-center justify-between">
                  <h4 className="font-black text-white text-sm">Quick Governance Actions</h4>
                </div>
                <div className="space-y-3">
                  <button onClick={()=>{ setTab("doctors"); }}
                    className="w-full py-3 rounded-xl bg-teal-500 text-slate-900 font-black text-xs hover:bg-teal-400 transition flex items-center justify-center gap-2">
                    👨‍⚕️ Manage Doctors (Edit / Delete / Fees)
                  </button>
                  <button onClick={()=>{ setTab("hospitals"); }}
                    className="w-full py-3 rounded-xl bg-cyan-600 text-white font-black text-xs hover:bg-cyan-500 transition flex items-center justify-center gap-2">
                    🏥 Manage Hospitals (Edit Beds / ER / Delete)
                  </button>
                  <button onClick={()=>{ setShowAddModal(true); }}
                    className="w-full py-3 rounded-xl border border-slate-700 text-slate-300 font-bold text-xs hover:border-teal-500/40 transition flex items-center justify-center gap-2">
                    ➕ Register New Doctor or Hospital
                  </button>
                  <button onClick={loadData}
                    className="w-full py-3 rounded-xl border border-slate-800 text-slate-400 font-bold text-xs hover:text-white transition flex items-center justify-center gap-2">
                    🔄 Sync System Telemetry
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: DOCTORS MANAGEMENT (EDIT / DELETE) */}
        {tab==="doctors" && (
          <div className="space-y-4 fade-up">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h3 className="text-base font-black text-white flex items-center gap-2">
                  <span>👨‍⚕️ Doctor Directory & Clinical Roster</span>
                  <span className="px-2 py-0.5 rounded-full text-xs bg-cyan-950 text-cyan-300 border border-cyan-800/40 mono">{doctors.length} Doctors</span>
                </h3>
                <p className="text-xs text-slate-400">Manage specialties, consultation fees, hospital affiliations, or delete doctors</p>
              </div>
              <div className="flex items-center gap-2">
                <button onClick={()=>{ setNewStaff({role:"doctor", id:"", name:"", password:"", specialty:"", hospital_id:"HOSP001", fee:500}); setShowAddModal(true); }}
                  className="px-3.5 py-2 rounded-xl bg-teal-500 text-slate-900 font-black text-xs hover:bg-teal-400 transition flex items-center gap-1.5">
                  ➕ Add New Doctor
                </button>
                <button onClick={loadData} className="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white text-xs transition">
                  🔄 Refresh
                </button>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              {doctors.map(d=>(
                <div key={d.id} className="glass rounded-2xl p-5 border border-slate-800 hover:border-teal-500/30 transition flex flex-col justify-between">
                  <div>
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <h4 className="font-black text-white text-base">{d.name}</h4>
                        <p className="text-teal-400 text-xs font-bold">{d.specialty}</p>
                      </div>
                      <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-[10px] text-slate-400 mono font-bold">{d.id}</span>
                    </div>

                    <div className="mt-4 space-y-2 text-xs">
                      <div className="flex justify-between py-1 border-b border-slate-800/60">
                        <span className="text-slate-500">Hospital:</span>
                        <span className="font-semibold text-slate-300">{d.hospital_name || d.hospital_id || "Apollo Hospitals"}</span>
                      </div>
                      <div className="flex justify-between py-1 border-b border-slate-800/60">
                        <span className="text-slate-500">Consultation Fee:</span>
                        <span className="font-black text-emerald-400 mono">₹{d.fee}</span>
                      </div>
                      <div className="flex justify-between py-1">
                        <span className="text-slate-500">OPD Timings:</span>
                        <span className="text-slate-400 mono text-[11px] truncate max-w-[200px]">
                          {(() => {
                            try {
                              const s = JSON.parse(d.slots_json);
                              return Array.isArray(s) ? s.join(", ") : d.slots_json;
                            } catch(e){ return d.slots_json || "09:00, 11:00, 14:00"; }
                          })()}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 mt-5 pt-3 border-t border-slate-800/80">
                    <button onClick={()=>{
                      let slotsArr = ["09:00","11:00","14:00","16:00"];
                      try { slotsArr = JSON.parse(d.slots_json); } catch(e){}
                      setEditingDoctor({
                        ...d,
                        slots_str: Array.isArray(slotsArr) ? slotsArr.join(", ") : slotsArr,
                        password: ""
                      });
                    }} className="flex-1 py-2 rounded-xl bg-teal-500/15 border border-teal-500/30 text-teal-300 hover:bg-teal-500/25 text-xs font-bold transition flex items-center justify-center gap-1.5">
                      ✏️ Edit Doctor Info
                    </button>
                    <button onClick={()=>setDeletingDoctor(d)}
                      className="px-3.5 py-2 rounded-xl bg-rose-950/30 border border-rose-500/30 text-rose-300 hover:bg-rose-900/50 text-xs font-bold transition flex items-center justify-center gap-1">
                      🗑️ Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 3: HOSPITALS MANAGEMENT (EDIT / DELETE) */}
        {tab==="hospitals" && (
          <div className="space-y-4 fade-up">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h3 className="text-base font-black text-white flex items-center gap-2">
                  <span>🏥 Hospital Registry & Capacity Control</span>
                  <span className="px-2 py-0.5 rounded-full text-xs bg-amber-950 text-amber-300 border border-amber-800/40 mono">{hospitals.length} Hospitals</span>
                </h3>
                <p className="text-xs text-slate-400">Edit emergency readiness, bed allocations, licenses, or delete hospital entries</p>
              </div>
              <div className="flex items-center gap-2">
                <button onClick={()=>{ setNewStaff({role:"hospital", id:"", name:"", password:"", specialty:""}); setShowAddModal(true); }}
                  className="px-3.5 py-2 rounded-xl bg-teal-500 text-slate-900 font-black text-xs hover:bg-teal-400 transition flex items-center gap-1.5">
                  ➕ Add New Hospital
                </button>
                <button onClick={loadData} className="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white text-xs transition">
                  🔄 Refresh
                </button>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              {hospitals.map(h=>(
                <div key={h.id} className="glass rounded-2xl p-5 border border-slate-800 hover:border-teal-500/30 transition flex flex-col justify-between">
                  <div>
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <h4 className="font-black text-white text-base">{h.name}</h4>
                        <p className="text-slate-400 text-xs font-mono">{h.license_number || "NABH Accredited"}</p>
                      </div>
                      <span className={`px-2.5 py-1 rounded-full text-[10px] font-black mono uppercase ${
                        h.er_status==="READY"?"bg-emerald-950 text-emerald-300 border border-emerald-800/40":
                        h.er_status==="CRITICAL"?"bg-rose-950 text-rose-300 border border-rose-800/40":
                        "bg-amber-950 text-amber-300 border border-amber-800/40"
                      }`}>
                        ER: {h.er_status || "READY"}
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-2 mt-4">
                      <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                        <p className="text-[10px] text-slate-500 font-bold uppercase">ICU Beds</p>
                        <p className="text-base font-black text-teal-400 mono mt-0.5">{h.icu_beds_avail} / {h.icu_beds_total}</p>
                      </div>
                      <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                        <p className="text-[10px] text-slate-500 font-bold uppercase">General Beds</p>
                        <p className="text-base font-black text-sky-400 mono mt-0.5">{h.gen_beds_avail} / {h.gen_beds_total}</p>
                      </div>
                    </div>

                    <div className="mt-3 space-y-1.5 text-xs text-slate-400">
                      <div className="flex justify-between py-1 border-b border-slate-800/60">
                        <span>Rating & Distance:</span>
                        <span className="text-slate-300 font-semibold">⭐ {h.rating || 4.8} · 📍 {h.distance || "1.0 km"}</span>
                      </div>
                      <div className="flex justify-between py-1">
                        <span>Affiliated Doctors:</span>
                        <span className="text-teal-400 font-bold mono">{h.doctor_count || 0} active</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 mt-5 pt-3 border-t border-slate-800/80">
                    <button onClick={()=>setEditingHospital({...h, password:""})}
                      className="flex-1 py-2 rounded-xl bg-cyan-500/15 border border-cyan-500/30 text-cyan-300 hover:bg-cyan-500/25 text-xs font-bold transition flex items-center justify-center gap-1.5">
                      ✏️ Edit Hospital & Beds
                    </button>
                    <button onClick={()=>setDeletingHospital(h)}
                      className="px-3.5 py-2 rounded-xl bg-rose-950/30 border border-rose-500/30 text-rose-300 hover:bg-rose-900/50 text-xs font-bold transition flex items-center justify-center gap-1">
                      🗑️ Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 4: USERS DIRECTORY (WITH EDIT/DELETE ACTIONS) */}
        {tab==="users" && (
          <div className="space-y-4 fade-up">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h3 className="text-base font-black text-white">Registered Users & Staff Directory</h3>
                <p className="text-xs text-slate-400">All authenticated identities stored in SQLite (Click Edit/Delete to manage)</p>
              </div>
              <div className="flex items-center gap-2">
                {["ALL","PATIENT","DOCTOR","HOSPITAL","ADMIN"].map(r=>(
                  <button key={r} onClick={()=>setRoleFilter(r)}
                    className={`px-3 py-1 rounded-lg text-xs font-bold transition ${roleFilter===r?"bg-teal-500 text-slate-900":"bg-slate-900 border border-slate-800 text-slate-400 hover:text-white"}`}>
                    {r}
                  </button>
                ))}
                <button onClick={()=>setShowAddModal(true)} className="px-3 py-1 rounded-lg bg-teal-500 text-slate-900 font-black text-xs hover:bg-teal-400 transition">
                  + Add Staff
                </button>
              </div>
            </div>

            <div className="glass rounded-2xl border border-slate-800 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-900/80 border-b border-slate-800 text-slate-400 font-bold">
                    <tr>
                      <th className="p-3.5">User ID / Phone</th>
                      <th className="p-3.5">Role</th>
                      <th className="p-3.5">Full Name</th>
                      <th className="p-3.5">Details</th>
                      <th className="p-3.5">Registered</th>
                      <th className="p-3.5 text-right">Admin Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60">
                    {filteredUsers.map((u,i)=>(
                      <tr key={u.id||i} className="hover:bg-teal-500/5 transition">
                        <td className="p-3.5 font-bold text-white mono">{u.id}</td>
                        <td className="p-3.5">
                          <span className={`px-2 py-0.5 rounded-full font-bold uppercase text-[9px] mono ${
                            u.role==="admin"?"bg-violet-950 text-violet-300 border border-violet-800/40":
                            u.role==="doctor"?"bg-cyan-950 text-cyan-300 border border-cyan-800/40":
                            u.role==="hospital"?"bg-amber-950 text-amber-300 border border-amber-800/40":
                            "bg-teal-950 text-teal-300 border border-teal-800/40"
                          }`}>{u.role}</span>
                        </td>
                        <td className="p-3.5 font-semibold text-slate-200">{u.display_name || u.name || "—"}</td>
                        <td className="p-3.5 text-slate-400">{u.specialty || u.blood_group || "—"}</td>
                        <td className="p-3.5 text-slate-500 mono">{u.created_at ? new Date(u.created_at).toLocaleDateString() : "Active"}</td>
                        <td className="p-3.5 text-right">
                          {u.role==="doctor" && (
                            <div className="flex items-center justify-end gap-1.5">
                              <button onClick={()=>{
                                const found = doctors.find(d=>d.id===u.id) || {id:u.id, name:u.display_name||u.name, specialty:u.specialty||"General", fee:500, slots_json:"[]"};
                                let slotsArr = ["09:00","11:00","14:00"];
                                try { slotsArr = JSON.parse(found.slots_json); } catch(e){}
                                setEditingDoctor({...found, slots_str: Array.isArray(slotsArr)?slotsArr.join(", "):slotsArr, password:""});
                              }} className="px-2.5 py-1 rounded-lg bg-teal-500/20 text-teal-300 hover:bg-teal-500/30 text-[11px] font-bold">
                                ✏️ Edit
                              </button>
                              <button onClick={()=>setDeletingDoctor({id:u.id, name:u.display_name||u.name})}
                                className="px-2.5 py-1 rounded-lg bg-rose-950/40 text-rose-300 hover:bg-rose-900/60 text-[11px] font-bold">
                                🗑️ Delete
                              </button>
                            </div>
                          )}
                          {u.role==="hospital" && (
                            <div className="flex items-center justify-end gap-1.5">
                              <button onClick={()=>{
                                const found = hospitals.find(h=>h.id===u.id) || {id:u.id, name:u.display_name||u.name, license_number:"NABH", icu_beds_total:24, icu_beds_avail:8, gen_beds_total:120, gen_beds_avail:35, er_status:"READY"};
                                setEditingHospital({...found, password:""});
                              }} className="px-2.5 py-1 rounded-lg bg-cyan-500/20 text-cyan-300 hover:bg-cyan-500/30 text-[11px] font-bold">
                                ✏️ Edit
                              </button>
                              <button onClick={()=>setDeletingHospital({id:u.id, name:u.display_name||u.name})}
                                className="px-2.5 py-1 rounded-lg bg-rose-950/40 text-rose-300 hover:bg-rose-900/60 text-[11px] font-bold">
                                🗑️ Delete
                              </button>
                            </div>
                          )}
                          {u.role!=="doctor" && u.role!=="hospital" && (
                            <span className="text-slate-600 mono text-[10px]">—</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB 5: AUDIT LOGS */}
        {tab==="audit" && (
          <div className="space-y-4 fade-up">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base font-black text-white">Live Security Audit Trail</h3>
                <p className="text-xs text-slate-400">Chronological security events tracked in SQLite audit_logs table</p>
              </div>
              <button onClick={loadData} className="px-3 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-teal-400 text-xs transition">
                🔄 Refresh Logs
              </button>
            </div>

            <div className="glass rounded-2xl border border-slate-800 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-900/80 border-b border-slate-800 text-slate-400 font-bold">
                    <tr>
                      <th className="p-3.5">Timestamp</th>
                      <th className="p-3.5">Action</th>
                      <th className="p-3.5">User</th>
                      <th className="p-3.5">Role</th>
                      <th className="p-3.5">Status</th>
                      <th className="p-3.5">Client IP</th>
                      <th className="p-3.5">Details</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
                    {auditLogs.map((l,i)=>(
                      <tr key={l.id||i} className="hover:bg-slate-900/40">
                        <td className="p-3.5 text-slate-500">{l.timestamp ? new Date(l.timestamp).toLocaleTimeString() : "—"}</td>
                        <td className="p-3.5 font-bold text-teal-400">{l.action}</td>
                        <td className="p-3.5 text-slate-300">{l.user_id}</td>
                        <td className="p-3.5 uppercase text-slate-400">{l.role}</td>
                        <td className="p-3.5">
                          <span className={`px-2 py-0.5 rounded text-[9px] font-bold ${l.status==="SUCCESS"?"bg-emerald-950 text-emerald-300":"bg-rose-950 text-rose-300"}`}>
                            {l.status}
                          </span>
                        </td>
                        <td className="p-3.5 text-slate-500">{l.client_ip}</td>
                        <td className="p-3.5 text-slate-400 max-w-xs truncate font-sans">{l.details}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

      </div>

      {/* EDIT DOCTOR MODAL */}
      {editingDoctor && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass rounded-3xl p-6 border border-teal-500/30 max-w-lg w-full space-y-4 fade-up">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-black text-white text-base">✏️ Edit Doctor Profile</h3>
                <p className="text-xs text-slate-400">Updating ID: <span className="text-teal-400 mono">{editingDoctor.id}</span></p>
              </div>
              <button onClick={()=>setEditingDoctor(null)} className="text-slate-400 hover:text-white text-lg">✕</button>
            </div>

            <form onSubmit={handleSaveDoctor} className="space-y-3 text-xs">
              <div>
                <Label required>Doctor Full Name</Label>
                <input className="inp" required value={editingDoctor.name || ""}
                  onChange={e=>setEditingDoctor({...editingDoctor, name: e.target.value})}/>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <Label required>Specialty</Label>
                  <input className="inp" required value={editingDoctor.specialty || ""}
                    placeholder="e.g. Cardiologist"
                    onChange={e=>setEditingDoctor({...editingDoctor, specialty: e.target.value})}/>
                </div>
                <div>
                  <Label required>Consultation Fee (₹)</Label>
                  <input className="inp" type="number" required min="100" max="10000"
                    value={editingDoctor.fee || 500}
                    onChange={e=>setEditingDoctor({...editingDoctor, fee: e.target.value})}/>
                </div>
              </div>

              <div>
                <Label>Assigned Hospital</Label>
                <select className="inp" value={editingDoctor.hospital_id || "HOSP001"}
                  onChange={e=>setEditingDoctor({...editingDoctor, hospital_id: e.target.value})}>
                  {hospitals.map(h=>(
                    <option key={h.id} value={h.id}>{h.name} ({h.id})</option>
                  ))}
                </select>
              </div>

              <div>
                <Label>Available OPD Time Slots (Comma-separated)</Label>
                <input className="inp" placeholder="09:00, 11:00, 14:00, 16:30"
                  value={editingDoctor.slots_str || ""}
                  onChange={e=>setEditingDoctor({...editingDoctor, slots_str: e.target.value})}/>
                <p className="text-[10px] text-slate-500 mt-1">Example: 09:00, 10:30, 14:00, 16:00</p>
              </div>

              <div>
                <Label>Reset Password (Optional)</Label>
                <input className="inp" type="password" placeholder="Leave blank to keep unchanged"
                  value={editingDoctor.password || ""}
                  onChange={e=>setEditingDoctor({...editingDoctor, password: e.target.value})}/>
              </div>

              <div className="flex gap-2 pt-3 border-t border-slate-800">
                <button type="button" onClick={()=>setEditingDoctor(null)} className="btn-outline-teal flex-1 py-2.5 text-xs font-bold">Cancel</button>
                <button type="submit" disabled={actionLoading} className="btn-teal flex-1 py-2.5 text-xs font-black">
                  {actionLoading ? "Saving Changes…" : "💾 Save Changes to SQLite"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* DELETE DOCTOR CONFIRMATION MODAL */}
      {deletingDoctor && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass rounded-3xl p-6 border border-rose-500/40 max-w-md w-full space-y-4 fade-up">
            <div className="flex items-center gap-3 text-rose-400">
              <span className="text-3xl">⚠️</span>
              <div>
                <h3 className="font-black text-white text-base">Delete Doctor Permanently?</h3>
                <p className="text-xs text-rose-300">Action cannot be undone</p>
              </div>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed">
              Are you sure you want to remove <strong className="text-white">{deletingDoctor.name}</strong> (<span className="mono text-teal-400">{deletingDoctor.id}</span>)?
              This will revoke their login credentials and cancel any pending appointments.
            </p>

            <div className="flex gap-2 pt-3">
              <button onClick={()=>setDeletingDoctor(null)} className="btn-outline-teal flex-1 py-2.5 text-xs font-bold">Cancel</button>
              <button onClick={handleConfirmDeleteDoctor} disabled={actionLoading}
                className="flex-1 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-black text-xs transition">
                {actionLoading ? "Deleting…" : "🗑️ Confirm Delete"}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* EDIT HOSPITAL MODAL */}
      {editingHospital && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass rounded-3xl p-6 border border-cyan-500/30 max-w-lg w-full space-y-4 fade-up">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-black text-white text-base">✏️ Edit Hospital & Capacity</h3>
                <p className="text-xs text-slate-400">Updating ID: <span className="text-cyan-400 mono">{editingHospital.id}</span></p>
              </div>
              <button onClick={()=>setEditingHospital(null)} className="text-slate-400 hover:text-white text-lg">✕</button>
            </div>

            <form onSubmit={handleSaveHospital} className="space-y-3 text-xs">
              <div>
                <Label required>Hospital Name</Label>
                <input className="inp" required value={editingHospital.name || ""}
                  onChange={e=>setEditingHospital({...editingHospital, name: e.target.value})}/>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <Label required>License / Accreditation</Label>
                  <input className="inp" required value={editingHospital.license_number || ""}
                    onChange={e=>setEditingHospital({...editingHospital, license_number: e.target.value})}/>
                </div>
                <div>
                  <Label>Emergency Status (ER)</Label>
                  <select className="inp" value={editingHospital.er_status || "READY"}
                    onChange={e=>setEditingHospital({...editingHospital, er_status: e.target.value})}>
                    <option value="READY">🟢 READY (Normal Operations)</option>
                    <option value="BUSY">🟡 BUSY (High Patient Volume)</option>
                    <option value="CRITICAL">🔴 CRITICAL (Trauma / Divert)</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <Label>ICU Beds: Available / Total</Label>
                  <div className="flex gap-2">
                    <input className="inp" type="number" min="0" placeholder="Avail"
                      value={editingHospital.icu_beds_avail || 0}
                      onChange={e=>setEditingHospital({...editingHospital, icu_beds_avail: e.target.value})}/>
                    <input className="inp" type="number" min="1" placeholder="Total"
                      value={editingHospital.icu_beds_total || 24}
                      onChange={e=>setEditingHospital({...editingHospital, icu_beds_total: e.target.value})}/>
                  </div>
                </div>
                <div>
                  <Label>General Beds: Available / Total</Label>
                  <div className="flex gap-2">
                    <input className="inp" type="number" min="0" placeholder="Avail"
                      value={editingHospital.gen_beds_avail || 0}
                      onChange={e=>setEditingHospital({...editingHospital, gen_beds_avail: e.target.value})}/>
                    <input className="inp" type="number" min="1" placeholder="Total"
                      value={editingHospital.gen_beds_total || 120}
                      onChange={e=>setEditingHospital({...editingHospital, gen_beds_total: e.target.value})}/>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <Label>Distance Metric</Label>
                  <input className="inp" value={editingHospital.distance || "1.0 km"}
                    onChange={e=>setEditingHospital({...editingHospital, distance: e.target.value})}/>
                </div>
                <div>
                  <Label>Rating (1.0 - 5.0)</Label>
                  <input className="inp" type="number" step="0.1" min="1" max="5"
                    value={editingHospital.rating || 4.8}
                    onChange={e=>setEditingHospital({...editingHospital, rating: e.target.value})}/>
                </div>
              </div>

              <div>
                <Label>Reset Password (Optional)</Label>
                <input className="inp" type="password" placeholder="Leave blank to keep unchanged"
                  value={editingHospital.password || ""}
                  onChange={e=>setEditingHospital({...editingHospital, password: e.target.value})}/>
              </div>

              <div className="flex gap-2 pt-3 border-t border-slate-800">
                <button type="button" onClick={()=>setEditingHospital(null)} className="btn-outline-teal flex-1 py-2.5 text-xs font-bold">Cancel</button>
                <button type="submit" disabled={actionLoading} className="btn-teal flex-1 py-2.5 text-xs font-black">
                  {actionLoading ? "Saving Changes…" : "💾 Save Changes to SQLite"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* DELETE HOSPITAL CONFIRMATION MODAL */}
      {deletingHospital && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass rounded-3xl p-6 border border-rose-500/40 max-w-md w-full space-y-4 fade-up">
            <div className="flex items-center gap-3 text-rose-400">
              <span className="text-3xl">⚠️</span>
              <div>
                <h3 className="font-black text-white text-base">Delete Hospital Permanently?</h3>
                <p className="text-xs text-rose-300">Action cannot be undone</p>
              </div>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed">
              Are you sure you want to delete <strong className="text-white">{deletingHospital.name}</strong> (<span className="mono text-cyan-400">{deletingHospital.id}</span>)?
              This will remove the hospital and all affiliated doctors from the DHANVI SQLite database.
            </p>

            <div className="flex gap-2 pt-3">
              <button onClick={()=>setDeletingHospital(null)} className="btn-outline-teal flex-1 py-2.5 text-xs font-bold">Cancel</button>
              <button onClick={handleConfirmDeleteHospital} disabled={actionLoading}
                className="flex-1 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-black text-xs transition">
                {actionLoading ? "Deleting…" : "🗑️ Confirm Delete Hospital"}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ADD STAFF MODAL */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass rounded-3xl p-6 border border-teal-500/30 max-w-md w-full space-y-4 fade-up">
            <div className="flex items-center justify-between">
              <h3 className="font-black text-white text-base">Add New Staff / Doctor</h3>
              <button onClick={()=>setShowAddModal(false)} className="text-slate-400 hover:text-white text-lg">✕</button>
            </div>

            {staffMsg && (
              <div className="p-3 rounded-xl bg-emerald-950/60 border border-emerald-500/40 text-emerald-300 text-xs font-bold">
                {staffMsg}
              </div>
            )}

            <form onSubmit={handleAddStaff} className="space-y-3">
              <div>
                <Label required>Role</Label>
                <select className="inp" value={newStaff.role} onChange={e=>setNewStaff({...newStaff, role: e.target.value})}>
                  <option value="doctor">Doctor</option>
                  <option value="hospital">Hospital Administrator</option>
                  <option value="admin">System Administrator</option>
                </select>
              </div>

              <div>
                <Label required>Staff Login ID</Label>
                <input className="inp" placeholder="e.g. DOC9850 or HOSP002" required
                  value={newStaff.id} onChange={e=>setNewStaff({...newStaff, id: e.target.value})}/>
              </div>

              <div>
                <Label required>Full Name</Label>
                <input className="inp" placeholder="e.g. Dr. Rajesh Verma" required
                  value={newStaff.name} onChange={e=>setNewStaff({...newStaff, name: e.target.value})}/>
              </div>

              <div>
                <Label required>Password (min 6 chars)</Label>
                <input className="inp" type="password" placeholder="Temporary password" required
                  value={newStaff.password} onChange={e=>setNewStaff({...newStaff, password: e.target.value})}/>
              </div>

              {newStaff.role==="doctor" && (
                <div>
                  <Label>Medical Specialty</Label>
                  <input className="inp" placeholder="e.g. Neurologist, Orthopedician"
                    value={newStaff.specialty} onChange={e=>setNewStaff({...newStaff, specialty: e.target.value})}/>
                </div>
              )}

              <div className="flex gap-2 pt-2">
                <button type="button" onClick={()=>setShowAddModal(false)} className="btn-outline-teal flex-1 py-2.5 text-xs">Cancel</button>
                <button type="submit" className="btn-teal flex-1 py-2.5 text-xs font-black">Save to SQLite</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
'''

# Verify brace matching of admin_code
stack = []
errors = []
for idx, ch in enumerate(admin_code):
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
    errors.append(f'Unclosed: {stack}')

print('Brace check on admin_code:', len(errors), errors)

with open('new_admin_dashboard.txt', 'w', encoding='utf-8') as f:
    f.write(admin_code)
print('Saved to new_admin_dashboard.txt')
