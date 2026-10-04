with open('auth.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = "/* ═══════════════════════════════════════════════════════════════════════════\n   ADMIN DASHBOARD — System Analytics, Staff Management & Security Audit\n═══════════════════════════════════════════════════════════════════════════ */\nfunction AdminDashboard({user, onLogout}){"

end_marker = "/* ═══════════════════════════════════════════════════════════════════════════\n   HOSPITAL DASHBOARD — Bed Capacity & Emergency Monitor"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

print(f"Start index: {start_idx}, End index: {end_idx}")

if start_idx == -1 or end_idx == -1:
    print("Markers not found!")
else:
    with open('new_admin_dashboard.txt', 'r', encoding='utf-8') as f:
        new_admin = f.read()

    new_text = text[:start_idx] + new_admin.strip() + "\n\n" + text[end_idx:]
    with open('auth.html', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("auth.html updated successfully!")
