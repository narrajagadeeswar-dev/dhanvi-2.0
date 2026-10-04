with open('auth.html', 'r', encoding='utf-8') as f:
    text = f.read()

prefix = text[:text.find('<script type="text/babel">')]
babel_start_line = prefix.count('\n') + 1

lines = text.splitlines()
target_line = babel_start_line + 3665

with open('lines_out.txt', 'w', encoding='utf-8') as out:
    for i in range(max(0, target_line - 30), min(len(lines), target_line + 40)):
        out.write(f"{i+1:5d}: {lines[i]}\n")

print(f"Written lines {target_line-30} to {target_line+40} to lines_out.txt")
