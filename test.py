import time

#create a set with 1000000 elements
setElements = set()
setSum = 0
for i in range(100000000):
    setElements.add(i)


#create a list with 1000000 elements
listElements = []
listSum = 0
for i in range(100000000):
    listElements.append(i)


timeSet = time.time()

for i in setElements:
    setSum += i

timeSet = time.time() - timeSet
print("Time to sum a set of 1000000 elements: " + str(timeSet))

timeList = time.time()

for i in listElements:
    listSum += i

timeList = time.time() - timeList
print("Time to sum a list of 1000000 elements: " + str(timeList))