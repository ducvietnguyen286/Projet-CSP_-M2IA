from pycsp3 import *

#-----------------------------------------------------DATA
nMachine, nRes, tests = data

nbrTest = len(tests)

#matrix of resource
resource = [] #deduire size
for i in range(nRes):
    resource.append([])

for i in range(nbrTest): #deduire test use resource
    for r in tests[i][2]:
        resource[r].append(i)

#number of resource constraint
lenRes = [len(res) for res in resource]

#number of machine constraint
lenMachine = [len(test[1]) for test in tests]

#domain of debut and fin
maxtime = 0
for test in tests:
    maxtime = maxtime + test[0]

#-------------------------------------------------------VAR
# m[i] is name of machine for tests[i]
m = VarArray(size = nbrTest, dom = range(nMachine))

# plan of testing by machine p[i][debut,fin] for tests[i]
p = VarArray(size = [nbrTest,2], dom = range(maxtime))


#-------------------------------------------------------CONSTRAINT
satisfy(

    #some tests can be tested by just some machine
    [m[i] in tests[i][1] for i in range(nbrTest) if lenMachine[i] > 0],

    #deduire time debut and fin for each test
    [p[i][1] == p[i][0] + tests[i][0] for i in range(nbrTest)],

    #deduire time debut and fin of test with each machine
    [((p[i][0] >= p[j][1]) | (p[i][1] <= p[j][0])) | (m[i] != m[j]) for i in range(nbrTest-1) for j in range(i+1,nbrTest)],
    
    #constraint of resource
    [(p[resource[h][i]][0] >= p[resource[h][j]][1]) | (p[resource[h][i]][1] <= p[resource[h][j]][0]) for h in range(nRes) for i in range(lenRes[h]-1) for j in range(i+1,lenRes[h]) if lenRes[h] > 1]
)

#--------------------------------------------------------OPTIMISE
minimize(
    Maximum([temp[1] for temp in p])
)
