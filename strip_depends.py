import re

with open('/home/levi/Documents/cmlre-platform/docker-compose.yml', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.strip().startswith('depends_on:'):
        skip = True
        continue
    if skip:
        # If the line is empty or starts with at least 6 spaces (which is more than the 4 spaces of 'depends_on:'), skip it
        # Actually depends_on is indented 4 spaces. So anything indented 6+ spaces is a child.
        if line.startswith('      ') or line.strip() == '':
            continue
        else:
            skip = False
    if not skip:
        new_lines.append(line)

with open('/home/levi/Documents/cmlre-platform/docker-compose.yml', 'w') as f:
    f.writelines(new_lines)

print("Done")
