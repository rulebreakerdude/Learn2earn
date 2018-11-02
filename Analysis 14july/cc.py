import json
import snap

f_loc='C:\\Users\\ruleBreakerDude\\Desktop\\cc.json'
f=open(f_loc,'r')
b=json.load(f)
n1 = snap.TNEANet.New()

count=1
proxy={}
rev_proxy={}
for item in b:
	if item not in proxy:
		proxy[item]=count
		rev_proxy[count]=item
		count=count+1
	if b[item] not in proxy:
		proxy[b[item]]=count
		rev_proxy[count]=b[item]
		count=count+1

for item in proxy:
	n1.AddNode(proxy[item])

for item in b:
	if b[item] != 0:
		n1.AddEdge(proxy[b[item]],proxy[item])
		
NIdColorH = snap.TIntStrH()
OutDegV = snap.TIntPrV()
snap.GetNodeOutDegV(n1, OutDegV)

for item in OutDegV:
	if item.GetVal2()>=3:
		NIdColorH[item.GetVal1()]="green"
		print rev_proxy[item.GetVal1()], item.GetVal2()
	if item.GetVal2()==0:
		NIdColorH[item.GetVal1()]="black"

snap.DrawGViz(n1, snap.gvlDot, "graph3.png", "graph 1",False,NIdColorH)		
snap.DrawGViz(n1, snap.gvlNeato, "graph1.png", "graph 1",False,NIdColorH)
snap.DrawGViz(n1, snap.gvlCirco, "graph2.png", "graph 2",False,NIdColorH)