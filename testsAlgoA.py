from navcase import NavCase
from aismessage import AISMessage


n = NavCase(2,4)

n.tabMsg.append(AISMessage(1515682140,1,270123456,48.0,-4.1,170,120,0,0))
n.tabMsg.append(AISMessage(1515682146,1,270123456,48.0,-4.1,170,120,0,0))
#n.tabMsg.append(AISMessage(1515682152,1,270123456,48.0,-4.1,170,120,0,0))
n.tabMsg.append(AISMessage(1515682158,1,270123456,48.0,-4.1,170,120,0,0))
n.tabMsg.append(AISMessage(1515682164,1,270123456,48.0,-4.1,170,120,0,0))

n.tabMsg.append(AISMessage(1515682170,1,270123456,48.0,-4.1,170,180,0,127))
n.tabMsg.append(AISMessage(1515682172,1,270123456,48.0,-4.1,170,180,0,127))
n.tabMsg.append(AISMessage(1515682174,1,270123456,48.0,-4.1,170,180,0,127))
n.tabMsg.append(AISMessage(1515682176,1,270123456,48.0,-4.1,170,180,0,127))

n.tabMsg.append(AISMessage(1515682176,1,270123456,48.0,-4.1,170,180,0,127))

n.tabMsg[8].intercalaire = True


for i in n.tabMsg :
    print(str(i))

rep = n.calculRecep()

print(len(n.tabMsg))
print(rep)
