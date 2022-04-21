import sys

from numpy import str0
sys.setrecursionlimit(10**5)
#read in funct from a file
#convert each func to CNF form
#write each CNF equation to the file CNF.txt

def or_CNF(vars, y_string):
    #print("CNF METHOD VARS: ", vars)
    #print("CNF METHOD Y_STRING: ", y_string)
    ret_lst = []
    for x in vars:
        num = x.strip()
        #print(num)
        str = ''
        if(num[0] == '~'):
            str = num[1:] + ' + '
        else:
            str = '~' + num + ' + '
        str += y_string
        ret_lst.append(str)
    str = ''
    for x in vars:
        str += x.strip() + ' + '
    str += '~' + y_string
    ret_lst.append(str)

    print("RETURN LIST OR: ", ret_lst)

    return ret_lst
        

def and_CNF(vars, y_string):
    #print("CNF METHOD VARS AND: ", vars)
    #print("CNF METHOD Y_STRING: ", y_string)
    ret_lst = []
    for x in vars:
        num = x.strip()
        ynum = y_string.strip()
        #print(num)
        str = num + ' + '
        if(ynum[0] == '~'):
            str += ynum[1:]
        else:
            str += '~' + ynum 
        ret_lst.append(str)
    str = ''
    for x in vars:
        num = x.strip()
        #print(num)
        if(num[0] == '~'):
            str += num[1:] + ' + '
        else:
            str += '~' + num + ' + '
    str +=  y_string
    ret_lst.append(str)

    print("RETURN LIST AND: ", ret_lst)

    return ret_lst

def not_CNF(vars, y_string):
    ret_lst = []
    num = vars.strip()
    str = num + ' + ' + y_string
    ret_lst.append(str)
    str = ''
    if(num[0] == '~'):
        num = num[1:]
        str += num
    else:
        str += '~' + num
    str += ' + ~' + y_string
    ret_lst.append(str)

    print("RETURN LIST NOT: ", ret_lst)
    return ret_lst

def xor_CNF(vars, out):
    ret_lst = []
    str0 = '~' + vars[0] + ' + ' + vars[1] + ' + ' + out #~x + y + z
    str1 = vars[0] + ' + ~' + vars[1] + ' + '+ out #x + ~y + z
    str2 = '~' + vars[0] + ' + ~' + vars[1] + ' + ~' + out #~x + ~y + ~z 
    str3 = vars[0] + ' + ' + vars[1] + '+ ~' + out # x + y + ~z
    str4 = out

    ########    Possibly remove str4 and always include that in CNF, regardless of XOR

    #print(str0)
    #print(str1)
    #print(str2)
    #print(str3)
    ret_lst.append(str0)
    ret_lst.append(str1)
    ret_lst.append(str2)
    ret_lst.append(str3)
    ret_lst.append(str4)
    return ret_lst

#need to add a '.' between clauses

def main():

    filename = sys.argv[1]
    datalst = []
    datafile = open(filename, "r") 
    for line in datafile:
        datalst.append(line.strip())
    datafile.close() # close data fp

    #print(datalst[0])
    #print(datalst[1])

    lstWrite = []

    for xyz in datalst:
        print(xyz)
        funNames = []
        clauses = []
        terms1 = []
        terms2 = []

        funNames.append(xyz.split('=')[0])
        clauses.append(xyz.split('=')[1])
        
        for x in range(len(clauses)):
            if x == 0:
                terms1 = clauses[x].split('+')
            elif x == 1:
                terms2 = clauses[x].split('+')
            else:
                pass


        print("function names: ", funNames)
        print("clauses: ", clauses)
        print("eq1 terms: ", terms1)
        print('eq2 terms: ', terms2)

        litterals1 = []
        for x in terms1:
            litterals1.append(x.split("."))


        print("litterals1: ", litterals1)

        #need to change the notted vars to y version

        #get all the negated values in the equation, append them to a list, non-repeating
        negVals = []
        for x in range(len(litterals1)):
            num = litterals1[x]
            for y in range(len(num)):
                check = num[y].strip()
                if(check[0] == '~'):
                    if(check not in negVals):
                        negVals.append(litterals1[x][y].strip())
        print(negVals)

        #for all the negative values, we will assign add it to a dictionary with corresponding yx value
        diction = {}           
        for x in range(len(negVals)):
            diction.update({ str(negVals[x]).strip() : "y" + str(x)})
        print("Diction: ", diction)

        or_lst = []
        for x in litterals1:
            if (len(x) == 1):
                strr = str(x[0]).strip()
                #strr = 'p'
                print(strr)
                if(strr in diction):#in dictionary
                    #print("TEST", diction[strr])
                    or_lst.append(str(diction[strr]))
                else:
                    or_lst.append(x[0])


        #now we will updated the litterals like using the newly created dictionary
        for x in range(len(litterals1)):
            #print("outlit: ",litterals1[x])
            for y in range(len(litterals1[x])):
                currentLit = str(litterals1[x][y]).strip()
                #print("CHECK lit: ", currentLit)
                #print("CHECK keys: ", diction.keys())
                if(str(currentLit).strip() in diction):
                    #print("CHECK2: ", diction[currentLit])
                    litterals1[x][y] = diction[currentLit]
                
        print("litterals1 updated: ", litterals1)


        #here we want to call the CNF AND functino for all of these litterals

        y_outs = []

        #first thing to append to the final output are the nots
        for x in diction:
            if(x[0] == '~'):
                y_outs.append((not_CNF(x[1:], diction[x]))[0])
                y_outs.append((not_CNF(x[1:], diction[x]))[1])
            else:
                y_outs.append((not_CNF(x, diction[x]))[0])
                y_outs.append((not_CNF(x, diction[x]))[1])

        print("Y OUTS: ", y_outs)


        print("lit len: ", len(litterals1))
        for x in range(len(litterals1)):
            ystr = 'y' + str(x + len(diction))
            print("TESTING Y STRING: ", ystr)
            if(len(litterals1[x]) > 1):
                result = and_CNF(litterals1[x], ystr)
                or_lst.append(ystr)
                for y in result:
                    y_outs.append(y)
        
        print(y_outs)
        print(or_lst)
        print()
        zStr = 'z' + str(datalst.index(xyz))
        print("ZSTR: ", zStr)
        or_out_CNF = (or_CNF(or_lst, zStr))

        for x in or_out_CNF:
            y_outs.append(x)

        print("Final CNF")


    
        #saveString = 'CNF = '

        saveString = ''
        for x in y_outs:
            saveString += '[' + str(x) + '].'
        
        lstWrite.append(saveString)

        #print(saveString)
    
    xorLst = []
    if(len(lstWrite) == 2):
        #call xor with z0 and z1
        print("XORing")
        xorLst = xor_CNF(['z0', 'z1'], 'z2')
        saveString = ''
        for x in xorLst:
            saveString += '[' + str(x) + '].'
        
        lstWrite.append(saveString)
    
    #print(lstWrite)

    for p in lstWrite:
        print((p))
    
    lastElem = lstWrite[-1]
    print(lastElem)
    if (lastElem[-1] == '.'):
        print("here")
        tempstr = lstWrite[-1][:len(lstWrite[-1])-1]
        lstWrite[-1] = tempstr

    print(lstWrite)     
    with open('CNF.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('CNF = ')
        myfile.write(''.join(lstWrite))


if __name__ == '__main__':
    main()