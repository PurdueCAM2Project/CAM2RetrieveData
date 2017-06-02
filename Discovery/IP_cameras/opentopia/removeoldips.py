with open('../listofcamerasafterclife', 'r') as f2:
	oldips = f2.read().splitlines()

with open('ips', 'r') as f1:
	ips = f1.read().splitlines()

with open('ipslocations', 'r') as f3:
	ipslocations = f3.read().splitlines()

newips = []
newipslocations = []

for index, ip in enumerate(ips):
	if ip not in oldips:
		newips.append(ips[index])
		newipslocations.append(ipslocations[index])

with open('newips', 'w') as f4:
	for line in newips: f4.write(line + '\n')

with open('newipslocations', 'w') as f5:
	for line in newipslocations: f5.write(line + '\n')

print len(ips), '>', len(newips)




