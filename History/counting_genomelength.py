f = open("AACI02.fasta")
count = 0
count_total = 0
for line in f:
    line = line.strip()
    if line[0] == ">":
        count_total += count
        count = 0
    else:
        count += len(line)
f.close()
print count_total

