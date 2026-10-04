with open('auth.html', 'r', encoding='utf-8') as f:
    text = f.read()

components = ['RoleSelect', 'PatientLogin', 'PatientRegister', 'StaffLogin']
for c in components:
    pos = text.find(f'function {c}')
    print(f"{c}: found at {pos}")
