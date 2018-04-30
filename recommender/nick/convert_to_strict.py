import json
import gzip
def parse(path):
	g = gzip.open(path, 'r')
	for l in g:
		yield json.dumps(eval(l))

f = open("meta_s.json", 'w')
for l in parse("hk.json.gz"):
	f.write(l + '\n')
	