import re
import sys

with open(r'C:\Users\admin\.gemini\antigravity\scratch\dhanvi\auth.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', html, re.DOTALL)
print(f"Total Babel scripts found: {len(scripts)}")
if not scripts:
    print("No script type=text/babel found!")
    sys.exit(0)

code = scripts[0]
print(f"Code length: {len(code)} characters, {len(code.splitlines())} lines")

# Check brace balancing
stack = []
line_no = 1
errors = []

for idx, ch in enumerate(code):
    if ch == '\n':
        line_no += 1
    if ch in '({[':
        stack.append((ch, line_no, idx))
    elif ch in ')}]':
        if not stack:
            errors.append(f"Unmatched closing '{ch}' at line {line_no}")
        else:
            last_ch, last_line, _ = stack.pop()
            matches = {')': '(', '}': '{', ']': '['}
            if matches[ch] != last_ch:
                errors.append(f"Mismatched '{ch}' at line {line_no}, expected closing for '{last_ch}' from line {last_line}")

if stack:
    for ch, l, _ in stack[-10:]:
        errors.append(f"Unclosed '{ch}' opened at line {l}")

print(f"Brace check errors: {len(errors)}")
for e in errors[:20]:
    print("  ", e)
