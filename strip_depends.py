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
        if line.startswith('      ') or line.strip() == '':
            continue
        else:
            skip = False
    if not skip:
        new_lines.append(line)

with open('/home/levi/Documents/cmlre-platform/docker-compose.yml', 'w') as f:
    f.writelines(new_lines)

print("Done")
