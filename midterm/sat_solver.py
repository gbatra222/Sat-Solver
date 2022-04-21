from copy import deepcopy
import copy
import sys

#Global Variables. 
SAT_MAIN = []
CNF_MAIN = []
CNF_DUP = []

def main():

    #get filename from command line and append data to datalst
    filename = sys.argv[1]
    datalst = []
    datafile = open(filename, "r")
    for line in datafile:
        datalst.append(line.strip())
    datafile.close() # close data fp

    
    datastr = ''
    #split datalst at '=', save the right side (all the clauses) to a datastr
    datastr += (datalst[0].split('=')[1]).strip()
    #split the datastr at each '.' so that lstCNF is a list of lists 
    lstCNF = datastr.split('.')[:]


    #here is where the '[' and ']' are removed from each clause by removing first and last element.
    for x in range(len(lstCNF)): 
        lstCNF[x] =(lstCNF[x][1:len(lstCNF[x])-1])[:]

    print("lstCNF:\t\t", lstCNF)



    lstClauses = []

    lstUsed = [] #  vars that have been used.
    lstAvail = [] # vars available.
    lstSAT = [] # list of SAT lists.
    lstUNSAT = [] # list of UNSAT lists.

    temp = []
    for x in lstCNF:
        lstClauses.append(x.split('+'))
        temp.append(x.split('+'))

    #print("lstClauses:\t", lstClauses)
    totalLits = []
    for x in range(len(lstClauses)): #go through all the clauses and add them to list of available elements
        for y in range(len(lstClauses[x])):
            lstClauses[x][y] = lstClauses[x][y].strip()[:]
            if(lstClauses[x][y] not in lstAvail):
                lstAvail.append(lstClauses[x][y])
                totalLits.append(lstClauses[x][y])

    print("lstAvail:\t", lstAvail)


    for x in lstAvail: #now we remove the duplicates as a result of notted elements (e.g. if we have ~x1 and x1, then remove the ~x1 and just have x1)
        print(x)
        if('~' + (x.strip()) in lstAvail):
            print(x)
            lstAvail.remove('~'+x)
        if(x[0] == '~'):
            lstAvail.remove(x)
    
    print("lstClauses:\t", lstClauses)
    print("lstAvail:\t", lstAvail)

    binStr = (len(lstAvail)) * '0'
    #binStr += '1'
    print("Binary String = ", binStr)



    for x in lstClauses:
        CNF_MAIN.append(x)
        CNF_DUP.append(x)

    print(CNF_MAIN)
    print(CNF_DUP)

    #print("TOTAL LITS: ", totalLits)
    

    constantAvail = lstAvail.copy()
    algorithm(lstClauses, temp ,lstAvail, constantAvail, lstUsed, lstSAT, lstUNSAT, binStr, totalLits)

    #print(help(list.copy()))

    #print("printing sat from main:")
    #print(SAT_MAIN)

    print("SAT Combinations")
    for x in  range(len(SAT_MAIN)):
        print("Stage ", x+1)
        for y in range(len(SAT_MAIN[x])):
            print(constantAvail[y], " = ", SAT_MAIN[x][y])
        print()


def algorithm(c, cInts, a, ca,  u, sat, unsat, binary, tl):
    print()
    print("In algorithm method!")
    #print(bin(int(binary, 2)))
    if(a): #if the current variable is not in the list of used variables...
        if(a[0]not in u):
            currentVar = a[0] #current variable is the first availiable element
    else:
        #here is where we must check if there exists a one in each term
        checkVar = len(cInts)
        compVar = 0
        for x in cInts:
            if('1' in x):
                compVar += 1
        print("compVal: ", compVar)
        print("checkVar: ", checkVar)
        if(compVar == checkVar):
            sat.append(binary)
            print("sat after update: ", sat)
        else:
            unsat.append(binary)
            print("unsat after update: ", unsat)
        c.clear()

        #print ("************ ", c)
        #cInts = []
        for x in CNF_MAIN:
            c.append(x)
        cInts = copy.deepcopy(c)

        a = ca.copy()
        u = []
        currentVar = a[0]
        testingInt = int(binary,2) #convert binary string to int
        testingInt+=1 #increment number
        binary = (bin(testingInt)[2:].zfill(len(a) + len(u))) #update it to have correct length, save to string
        print("binary after update: ", binary)

    print(currentVar)
    print(binary[ca.index(currentVar)])
    updateStr = str(binary[ca.index(currentVar)])
    updateStrNOT = ''
    if(updateStr == '0'):
        updateStrNOT = '1'
    else:
        updateStrNOT = '0'
    #print("length of c: ", len(c))
    a.remove(currentVar) #remove the current variable from the list of available
    u.append(currentVar) #append the current variable to the list of used variables
    for x in range(len(c)): #for each clause
        #print("here")
        for y in range(len(c[x])): #for each element in the clause
            #print("here")
            if(c[x][y][0] == '~'): # if the element is notted
                if(c[x][y][1:] == currentVar):
                    cInts[x][y] = updateStrNOT
            elif(c[x][y] == currentVar):
                cInts[x][y] = updateStr

    #UNCOMMENT THESE TO VIEW LISTS AT EACH STEP
    #print(c)
    #print(cInts)

    if(('0' in binary)):
        for x in cInts: #for each clause
            templst = []
            #print(x)
            #print(tl)
            #print(set(x) & set(tl))
            #print(any(i.strip() in tl for i in x))
            if(not (any(i.strip() in tl for i in x))):
                print("Caught x: ", x)
                for y in x:
                    templst.append(y)
                if('1' not in templst):
                    if(not(currentVar == ca[len(ca)-1])):
                        unsat.append(binary)
                        print("updated unsat: ", unsat)
                        #we want to move to next bin value

                        #we want to see when index needs to be incremented (e.g. if x1, increment binary string at index 0, if x2 then incremnt index 1 ...)

                        #finding the value to incrment the bin number by

                        incVal = 2**(len(ca) -1 - ca.index(currentVar)-1)
                        print("INC VAL: ", incVal)

                        testingInt = int(binary,2) #convert binary string to int
                        testingInt+=incVal #increment number
                        binary = (bin(testingInt)[2:].zfill(len(a) + len(u))) #update it to have correct length, save to string
                        print("MOVING TO NEXT BIN VALUE: ", binary)
                        break
                else:
                    print("NOT CHANGING BIN VALUE: ", binary)
                    #SAT_MAIN.append(binary)



    if(len(binary) > len(ca)):
        print("basecase met!")
        for x in sat:
            SAT_MAIN.append(x) #update gloabl var
        return 0
    else:
        algorithm(c, cInts , a , ca,  u , sat, unsat, binary, tl)


if __name__ == '__main__':
    main()