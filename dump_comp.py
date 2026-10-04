with open('auth.html', 'r', encoding='utf-8') as f:
    text = f.read()

def show_around(title, target, num_lines=40):
    pos = text.find(target)
    if pos == -1:
        print(f"Not found: {target}")
        return
    sub = text[pos:pos+4000]
    lines = sub.splitlines()[:num_lines]
    print(f"=== {title} ===")
    for l in lines:
        print(l)

with open('components_dump.txt', 'w', encoding='utf-8') as out:
    for comp in ['function RoleSelect', 'function PatientLogin', 'function StaffLogin']:
        pos = text.find(comp)
        out.write(f"\n\n==================== {comp} ====================\n")
        out.write(text[pos:pos+3000])

print("Written to components_dump.txt")
