import sys
total = 0.00
count = 0
for line in sys.stdin:
    lines = line.strip().split()
    count += int(lines[0])
    total += float(lines[-1])

print(total)
print(count)

