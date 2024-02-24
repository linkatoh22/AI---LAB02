import numpy as np
def input_file(readfile):
    file=open(readfile,'r')
    size=file.readline()
    size_Q=int(size)
    query=[]
    for i in range(size_Q):
        data=file.readline()
        query.append(data)
        query[i]=query[i].replace("\n","") 
    size_KB=int(file.readline())
    KB=[]
    for i in range(size_KB):
        data=file.readline()
        KB.append(data)
        KB[i]=KB[i].replace("\n","") 
    KB = [element.strip().split(' OR ') for element in KB]
    return query,KB
def negate(alpha):
    Negatequery_temp=[]
    Negatequery=[]
    for index in range(len(alpha)):
        item = alpha[index].split()
        for i in range(len(item)):
                if(item[i]!="AND" and item[i]!="OR"):
                    if "-" in item[i]:
                        data=item[i].replace("-","")
                        Negatequery_temp.append(data)
                    else:
                        data="-"+item[i]
                        Negatequery_temp.append(data)
                elif (item[i]=="AND" ):
                    data="OR"
                    Negatequery_temp.append(data)
                elif(item[i]=="OR"):
                    data="AND"
                    Negatequery_temp.append(data)
        joinall= " ".join(Negatequery_temp)
        Negatequery.append(joinall)
        Negatequery_temp=[]
    Negatequery_off=[]
    for i in range(len(Negatequery)):
        item=Negatequery[i]
        if("AND" in item):
            sub_clauses = item.split("AND")
            sub_clauses = [sub.strip() for sub in sub_clauses]
            sub_clauses = [sub.split() for sub in sub_clauses]
            Negatequery_off.append(sub_clauses)
    flattened_list = []
    if(Negatequery_off!=[]):
        for sublist in Negatequery_off:
            flattened_list.extend(sublist)
        return flattened_list
    
    Negatequery= [element.strip().split(' OR ') for element in Negatequery]
    return Negatequery

def Resolvable(clause):
    for i in clause:
        for j in clause:
            if ('-'+i==j or '-'+j==i):
                return True
    return False

def PL_Resolution(KB,query,write_File):
    Negatequery=negate(query)
    clause=KB[:]
    for i in Negatequery:
        clause.append(i)
    while True:
        loop=0 
        new=[]
        pairs=[(clause[i],clause[j]) for i in range(len(clause)) for j in range(i+1,len(clause))]
        for (clause_i, clause_j) in pairs:
            if Resolvable(clause_i+clause_j):
                resolvent=PL_Resolve(clause_i, clause_j)
                if len(resolvent)==0: 
                        loop += 1
                        write_File.write(str(loop))
                        for i in range(len(new)):
                            write_File.write('\n')
                            result=new[i]
                            result.sort(key=lambda kv:kv[-1], reverse=False)
                            remain_clause=' OR '.join([str(elem) for elem in result])
                            write_File.write(remain_clause)
                        write_File.write("\n{}\nYES \n")
                        return True
                if  (resolvent not in clause and Resolvable(resolvent)==False and resolvent not in new):
                        new.append(resolvent)
                        loop+=1
        if len(new)==0: 
            write_File.write("0\nNO\n")
            return False
        write_File.write(str(loop)+'\n')
        for i in range(len(new)):
            result=new[i]
            listToStr=' OR '.join([str(elem) for elem in result])
            write_File.write(listToStr+"\n")
        clause+=new 
def PL_Resolve(clause_i, clause_j):
    valid = False
    merge_clause=clause_i + clause_j # merge two clause
    merge_clause = sorted(merge_clause, key=lambda x: (x.startswith('-'), x))
    for i in clause_i:
        for j in clause_j:
            if ('-'+i==j or '-'+j==i) and valid==False:
                valid=True # Kiểm tra xem xóa mấy lần 
                merge_clause.remove(i) # remove -A
                merge_clause.remove(j) # remove A
            elif i==j: 
                merge_clause.remove(i) # 2 cái giống nhau xóa bớt 1 cái
            elif merge_clause==None: 
                valid=True
    return merge_clause
def main():
    input_f=input("Enter input file:")
    output_f=input("Enter output file:")
    output=open(output_f, 'w')
    query,KB=input_file(input_f)
    PL_Resolution(KB,query,output)
main()