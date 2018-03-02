from navcase import NavCase
from aismessage import AISMessage


n = NavCase(2,4)

n.tabMsg.append(AISMessage(1515682140,18,270123456,48.0,-4.1,170,120,-1,0))
n.tabMsg.append(AISMessage(1515682155,18,270123456,48.0,-4.1,170,120,-1,0))
n.tabMsg.append(AISMessage(1515682170,18,270123456,48.0,-4.1,170,120,-1,0))
n.tabMsg.append(AISMessage(1515682185,18,270123456,48.0,-4.1,170,120,-1,0))
n.tabMsg.append(AISMessage(1515682200,18,270123456,48.0,-4.1,170,120,-1,0))

n.tabMsg.append(AISMessage(1515682215,18,270123456,48.0,-4.1,170,120,-1,0))
n.tabMsg.append(AISMessage(1515682215,18,270123456,48.0,-4.1,170,120,-1,0))
n.tabMsg[6].intercalaire = True


#n.tabMsg.append(AISMessage(1515682230,18,270123456,48.0,-4.1,120,120,-1,0))
#n.tabMsg.append(AISMessage(1515682260,18,270123456,48.0,-4.1,120,120,-1,0))
#n.tabMsg.append(AISMessage(1515682290,18,270123456,48.0,-4.1,120,120,-1,0))
#n.tabMsg.append(AISMessage(1515682320,18,270123456,48.0,-4.1,120,120,-1,0))

#n.tabMsg.append(AISMessage(1515682320,18,270123456,48.0,-4.1,120,120,-1,0))

#n.tabMsg[7].intercalaire = True


for i in n.tabMsg :
    print(str(i))

rep = n.calculRecep()

print(len(n.tabMsg))
print(rep)
