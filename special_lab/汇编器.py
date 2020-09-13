import re
import sys

# read the file
# list1 should be used later
f1 = open("try.asm","r",encoding='utf-8')
list1=f1.readlines()
f1.close()

# strip the notes and '\n' and the ' '
# list3 should be used later
# use count
count = 0
list2=[]
list3=[]
for line1 in list1:
    if(line1.isspace()):
        continue
    line1=line1.replace('\t'," ").replace('\n',"")
    line1=line1.strip(' ')
    # there can be ';' in the .STRINGZ, so use re to find it
    # test: "euwhd;iw\"ss" "sos" ;wkdw"dfo
    if(len(re.findall('.*.STRINGZ.*\"',line1))!=0):
        line1=re.findall('.*.STRINGZ.*\"',line1)[0]
        if(';' not in line1): # still need to find some error
            flag_yinhao=0
            for nu in range(len(line1)):
                if(flag_yinhao == 2):
                    count=count+1
                    print("Unrecognized opcode or syntax error after .STRINGZ")
                    break
                if(line1[nu]=='\"' and flag_yinhao == 0): # first yinhao
                    flag_yinhao=1
                elif(line1[nu]=='\"' and line1[nu-1]!='\\' and flag_yinhao == 1):
                    flag_yinhao=2
            list3.append(line1)
        else:
            flag_yinhao=0
            for nu in range(len(line1)):
                if(flag_yinhao == 2):
                    count=count+1
                    print("Unrecognized opcode or syntax error after .STRINGZ")
                    break
                if(line1[nu]=='\"' and flag_yinhao == 0): # first yinhao
                    flag_yinhao=1
                elif(line1[nu]==';' and flag_yinhao == 1): # ignore
                    continue
                elif(line1[nu]=='\"' and line1[nu-1]!='\\' and flag_yinhao == 1):
                    flag_yinhao=2
            line1=line1[0:nu+1]
            list3.append(line1)
    else:
        list2=line1.split(';')
        if(len(list2[0])!=0):
            list3.append(list2[0])

# list4 should be used later
list2=[]
list4=[]
for line1 in list3:
    list2=line1.split(' ',1)
    list4.append(list2)

# use re
# find out the notations and build up a dictionary for them
Instruction=["ADD","AND","BR","BRn","BRz","BRp",
             "BRnz","BRzn","BRnp","BRpn","BRpz",
             "BRzp","BRnzp","BRzpn","BRznp","BRnpz",
             "BRpzn","BRpnz","JMP","JSR","JSRR",
             "LD","LDI","LDR","LEA","NOT","RET",
             "RTI","ST","STI","STR","TRAP","HALT",
             "GETC","OUT","PUTS","IN","PUTSP"]
Pseudo_ops=[".ORIG",".FILL",".BLKW",".STRINGZ",".END"]
Total_Words=Instruction + Pseudo_ops

nota_dict={}
for i in range(len(list4)):
    for word in Total_Words:
        if(word==list4[i][0]):
            break
    else:
        # start with '_' or alpha
        # all alpha/_/number
        stri=list4[i][0]
        if(stri.replace('_','').isalnum() and (stri[0].isalpha() or stri[0]=='_')):
            nota_dict[list4[i][0]]=i
        else:
            count=count+1
            print("Invalid label",stri)

# remember list4
# split more using replace()
# list5 should be used later
list5=[]
for i in range(len(list4)):
    line2=list4[i]
    if(line2[0]==".STRINGZ"):
        list5.append(line2)
        continue
    list2=[]
    list2.append(line2[0])
    if(len(line2)>1):
        list2=list2+line2[1].replace(','," ").split()
    list5.append(list2)
#for list2 in list5:
#    print(list2)

# remember list5
# change the notation into the numbers
# take care about notation in ".FILL"
f2=open(r'try.obj',mode='wb')
def IMM(num):
    if(num[0]=='#'):
        return eval(num[1:])
    elif(num[0]=='x'):
        return int(num[1:],16)
    elif(num.isdigit()):
        return eval(num)
    else:
        return num

def write_array(array):
    byte_arr=[int(array/256),array%256]
    f2.write(bytearray(byte_arr))

# find out the error
# use count to remember the times
BRlist= ["BR","BRn","BRz","BRp","BRnz","BRzn","BRnp",
        "BRpn","BRpz","BRzp","BRnzp","BRzpn","BRznp",
        "BRnpz","BRpzn","BRpnz"]
if(len(list5)==0):
    sys.exit(0)
elif(len(list5)>=1):
    if(list5[0][0]!=".ORIG"):
        count=count+1
        print("line 0 Expected .ORIG, but found",list5[0][0],"instead")
    elif(len(list5[0])==1):
        count=count+1
        print("line 0 Expected 16 bit value")
    if(len(list5)>=2):
        for list2 in list5:
            if(".END" in list2):
                break
        else:
            count=count+1
            print("Expected .END")
for i in range(len(list5)):
    list2=list5[i] #pick one line
    # take out the notation
    if(list2[0] in nota_dict):
        list2=list2[1:]
    # start
    # 16 instructions
    if(list2[0]=="ADD" or list2[0]=="AND"):
        if(len(list2)>=4):
            if(len(list2)>4):
                count=count+1
                print("line",i,"Unrecognized opcode or syntax error")
            if(list2[1][0]!='R'):
                count=count+1
                print("line",i,"Expected register operand, but found",list2[1],"instead")
            elif(list2[1][1:] not in ['0','1','2','3','4','5','6','7']):
                count=count+1
                print("line",i,"Expected register operand, but found",list2[1],"instead")
            if(list2[2][0]!='R'):
                count=count+1
                print("line",i,"Expected register operand, but found",list2[2],"instead")
            elif(list2[2][1:] not in ['0','1','2','3','4','5','6','7']):
                count=count+1
                print("line",i,"Expected register operand, but found",list2[2],"instead")
            # register or IMM5
            if(list2[3][0]=='R' and list2[3][1:] not in ['0','1','2','3','4','5','6','7']):
                count=count+1
                print("line",i,"Expected register or immediate value, but found",list2[3],"instead")
            elif(list2[3][0]!='R' and IMM(list2[3]) not in range(-32,32)):
                count=count+1
                print("line",i,"Expected register or 5 bit immediate value, but found",list2[3],"instead")
        else:
            count=count+1
            print("line",i,"Lack of operand")

    elif(list2[0] in BRlist):
        if(len(list2)>=2):
            if(len(list2)>2):
                count=count+1
                print("line",i,"Unrecognized opcode or syntax error")
            if(list2[1] not in nota_dict and IMM(list2[1]) not in range(-512,512)):
                count=count+1
                print("line",i,"Expected label or 9 bit immediate value, but found",list2[1],"instead")
        else:
            count=count+1
            print("line",i,"Lack of operand")

    elif(list2[0]=="JMP" or list2[0]=="JSRR"):
        if(len(list2)==1):
            count=count+1
            print("line",i,"Lack of operand")
        elif(list2[1][0]!='R' or list2[1][1:] not in ['0','1','2','3','4','5','6','7']):
            count=count+1
            print("line",i,"Expected register operand, but found",list2[1],"instead")
        if(len(list2)>2):
            count=count+1
            print("line",i,"Unrecognized opcode or syntax error")

    elif(list2[0] in ["RET", "RTI","HALT","GETC","OUT","PUTS","IN","PUTSP"]):
        if(len(list2)>1):
            count=count+1
            print("line",i,"Unrecognized opcode or syntax error")

    elif(list2[0]=="JSR"):
        if(len(list2)>=2):
            if(len(list2)>2):
                count=count+1
                print("line",i,"Unrecognized opcode or syntax error")
            if(list2[1] not in nota_dict and IMM(list2[1]) not in range(-2048,2048)):
                count=count+1
                print("line",i,"Expected label or 11 bit immediate value, but found",list2[1],"instead")
        else:
            count=count+1
            print("line",i,"Lack of operand")

    elif(list2[0] in ["LD","LDI","LEA","ST","STI"]):
        if(len(list2)>=3):
            if(len(list2)>3):
                count=count+1
                print("line",i,"Unrecognized opcode or syntax error")
            if(list2[1][0]!='R'):
                count=count+1
                print("line",i,"Expected register operand, but found",list2[1],"instead")
            elif(list2[1][1:] not in ['0','1','2','3','4','5','6','7']):
                count=count+1
                print("line",i,"Expected register operand, but found",list2[1],"instead")
            if(list2[2] not in nota_dict and IMM(list2[2]) not in range(-512,512)):
                count=count+1
                print("line",i,"Expected label or 9 bit immediate value, but found",list2[2],"instead")
        else:
            count=count+1
            print("line",i,"Lack of operand")

    elif(list2[0]=="LDR" or list2[0]=="STR"):
        if(len(list2)>=4):
            if(len(list2)>4):
                count=count+1
                print("line",i,"Unrecognized opcode or syntax error")
            if(list2[1][0]!='R'):
                count=count+1
                print("line",i,"Expected register operand, but found",list2[1],"instead")
            elif(list2[1][1:] not in ['0','1','2','3','4','5','6','7']):
                count=count+1
                print("line",i,"Expected register operand, but found",list2[1],"instead")
            if(list2[2][0]!='R'):
                count=count+1
                print("line",i,"Expected register operand, but found",list2[2],"instead")
            elif(list2[2][1:] not in ['0','1','2','3','4','5','6','7']):
                count=count+1
                print("line",i,"Expected register operand, but found",list2[2],"instead")
            # IMM6
            if(IMM(list2[3]) not in range(-64,64)):
                count=count+1
                print("line",i,"Expected register or 6 bit immediate value, but found",list2[3],"instead")
        else:
            count=count+1
            print("line",i,"Lack of operand")
    
    elif(list2[0]=="NOT"):
        if(len(list2)>=3):
            if(len(list2)>3):
                count=count+1
                print("line",i,"Unrecognized opcode or syntax error")
            if(list2[1][0]!='R'):
                count=count+1
                print("line",i,"Expected register operand, but found",list2[1],"instead")
            elif(list2[1][1:] not in ['0','1','2','3','4','5','6','7']):
                count=count+1
                print("line",i,"Expected register operand, but found",list2[1],"instead")
            if(list2[2][0]!='R'):
                count=count+1
                print("line",i,"Expected register operand, but found",list2[2],"instead")
            elif(list2[2][1:] not in ['0','1','2','3','4','5','6','7']):
                count=count+1
                print("line",i,"Expected register operand, but found",list2[2],"instead")
        else:
            count=count+1
            print("line",i,"Lack of operand")

    elif(list2[0]=="TRAP"):
        if(len(list2)>=2):
            if(len(list2)>2):
                count=count+1
                print("line",i,"Unrecognized opcode or syntax error")
            if(IMM(list2[1]) not in range(256)):
                count=count+1
                print("line",i,"Expected 8 bit value, but found",list2[1],"instead")
        else:
            count=count+1
            print("line",i,"Lack of operand")

    # 2 Pseudo_ops=[".FILL",".BLKW"]
    elif(list2[0]==".FILL"):
        if(len(list2)>=2):
            if(len(list2)>2):
                count=count+1
                print("line",i,"Unrecognized opcode or syntax error")
            if(list2[1] not in nota_dict and IMM(list2[1]) not in range(-65536,65536)):
                count=count+1
                print("line",i,"Expected label or 11 bit immediate value, but found",list2[1],"instead")
        else:
            count=count+1
            print("line",i,"Lack of operand")
         
    elif(list2[0]==".BLKW"):
        if(len(list2)>=2):
            if(len(list2)>2):
                count=count+1
                print("line",i,"Unrecognized opcode or syntax error")
            if(IMM(list2[1]) not in range(-65536,65536)): # there may be some error
                count=count+1
                print("line",i,"Expected value, but found",list2[1],"instead")
        else:
            count=count+1
            print("line",i,"Lack of operand")
            
if(count>0):
    print(count,"error(s)")
    sys.exit(0)

for i in range(len(list5)):
    list2=list5[i] #pick one line
    # take out the notation
    if(list2[0] in nota_dict):
        list2=list2[1:]
    # start
    # 16 instructions
    if(list2[0]=="ADD"):
        array=1<<3
        array=((array+eval(list2[1][1:]))<<3)+eval(list2[2][1:])
        if(list2[3][0]=='R'):
            array=(array<<6)+eval(list2[3][1:])
        else:
            array=(array<<1)+1
            array=(array<<5)+(IMM(list2[3])&0x1f)
        print(i,array)
        write_array(array)
    elif(list2[0]=="AND"):
        array=int('101',2)<<3
        array=((array+eval(list2[1][1:]))<<3)+eval(list2[2][1:])
        if(list2[3][0]=='R'):
            array=(array<<6)+eval(list2[3][1:])
        else:
            array=(array<<1)+1
            array=(array<<5)+(IMM(list2[3])&0x1f)
        print(i,array)
        write_array(array)
    elif(list2[0] in BRlist):
        array=0
        if(len(list2[0])==2):
            array=array+int('111',2)
        if('n' in list2[0]):
            array=array+int('100',2)
        if('z' in list2[0]):
            array=array+int('10',2)
        if('p' in list2[0]):
            array=array+int('1',2)
        array=array<<9
        if(list2[1][0]=='#' or list2[1][0]=='x' or list2[1].isdigit()):
            array=array+(IMM(list2[1])&0x1ff)
        else:
            array=array+((nota_dict[list2[1]]-i-1)&0x1ff)
        print(i,array)
        write_array(array)
    elif(list2[0]=="JMP"):
        array=int('1100',2)<<6
        array=array+eval(list2[1][1:])
        array=array<<6
        print(i,array)
        write_array(array)
    elif(list2[0]=="RET"):
        array=int('1100',2)<<6
        array=array+7
        array=array<<6
        print(i,array)
        write_array(array)
    elif(list2[0]=="JSRR"):
        array=int('0100',2)<<6
        array=array+eval(list2[1][1:])
        array=array<<6
        print(i,array)
        write_array(array)
    elif(list2[0]=="JSR"):
        array=((int('0100',2)<<1)+1)<<11
        if(list2[1] in nota_dict):
            array=array+((nota_dict[list2[1]]-i-1)&0x7ff)
        else:
            array=array+(IMM(list2[1])&0x7ff)
        print(i,array)
        write_array(array)
    elif(list2[0]=="LD"):
        array=int('0010',2)<<3
        array=array+eval(list2[1][1:])
        array=array<<9
        if(list2[2] in nota_dict):
            array=array+((nota_dict[list2[2]]-i-1)&0x1ff)
        else:
            array=array+(IMM(list2[2])&0x1ff)
        print(i,array)
        write_array(array)
    elif(list2[0]=="LDI"):
        array=int('1010',2)<<3
        array=array+eval(list2[1][1:])
        array=array<<9
        if(list2[2] in nota_dict):
            array=array+((nota_dict[list2[2]]-i-1)&0x1ff)
        else:
            array=array+(IMM(list2[2])&0x1ff)
        print(i,array)
        write_array(array)
    elif(list2[0]=="LDR"):
        array=int('0110',2)<<3
        array=array+eval(list2[1][1:])
        array=array<<3
        array=array+eval(list2[2][1:])
        array=array<<6
        array=array+(IMM(list2[3])&0x3f)
        print(i,array)
        write_array(array)
    elif(list2[0]=="LEA"):
        array=int('1110',2)<<3
        array=array+eval(list2[1][1:])
        array=array<<9
        if(list2[2] in nota_dict):
            array=array+((nota_dict[list2[2]]-i-1)&0x1ff)
        else:
            array=array+(IMM(list2[2])&0x1ff)
        print(i,array)
        write_array(array)
    elif(list2[0]=="NOT"):
        array=int('1001',2)<<3
        array=array+eval(list2[1][1:])
        array=array<<3
        array=array+eval(list2[2][1:])
        array=array<<6
        array=array+int('111111',2)
        print(i,array)
        write_array(array)
    elif(list2[0]=="RTI"):
        array=int('1000000000000000',2)
        print(i,array)
        write_array(array)
    elif(list2[0]=="ST"):
        array=int('0011',2)<<3
        array=array+eval(list2[1][1:])
        array=array<<9
        if(list2[2] in nota_dict):
            array=array+((nota_dict[list2[2]]-i-1)&0x1ff)
        else:
            array=array+(IMM(list2[2])&0x1ff)
        print(i,array)
        write_array(array)
    elif(list2[0]=="STI"):
        array=int('1011',2)<<3
        array=array+eval(list2[1][1:])
        array=array<<9
        if(list2[2] in nota_dict):
            array=array+((nota_dict[list2[2]]-i-1)&0x1ff)
        else:
            array=array+(IMM(list2[2])&0x1ff)
        print(i,array)
        write_array(array)
    elif(list2[0]=="STR"):
        array=int('0111',2)<<3
        array=array+eval(list2[1][1:])
        array=array<<3
        array=array+eval(list2[2][1:])
        array=array<<6
        array=array+(IMM(list2[3])&0x3f)
        print(i,array)
        write_array(array)
    elif(list2[0]=="TRAP"):
        array=int('1111',2)<<12
        array=array+IMM(list2[1])
        print(i,array)
        write_array(array)
    elif(list2[0]=="GETC"):
        array=int('1111',2)<<12
        array=array+IMM("x20")
        print(i,array)
        write_array(array)
    elif(list2[0]=="OUT"):
        array=int('1111',2)<<12
        array=array+IMM("x21")
        print(i,array)
        write_array(array)
    elif(list2[0]=="PUTS"):
        array=int('1111',2)<<12
        array=array+IMM("x22")
        print(i,array)
        write_array(array)
    elif(list2[0]=="IN"):
        array=int('1111',2)<<12
        array=array+IMM("x23")
        print(i,array)
        write_array(array)
    elif(list2[0]=="PUTSP"):
        array=int('1111',2)<<12
        array=array+IMM("x24")
        print(i,array)
        write_array(array)
    elif(list2[0]=="HALT"):
        array=int('1111',2)<<12
        array=array+IMM("x25")
        print(i,array)
        write_array(array)
    # 5 Pseudo_ops=[".ORIG",".FILL",".BLKW",".STRINGZ",".END"]
    elif(list2[0]==".ORIG"):
        array=IMM(list2[1])
        save_orig=array # for later notaion
        print(i,array)
        write_array(array)
    elif(list2[0]==".FILL"):
        if(list2[1] in nota_dict):
            array=save_orig+((nota_dict[list2[1]]-1)&0xffff)
        else:
            array=(IMM(list2[1])&0xffff)
        print(i,array)
        write_array(array)
    elif(list2[0]==".BLKW"):
        array=0
        for n in range(IMM(list2[1])):
            write_array(array)
        
    elif(list2[0]=='.STRINGZ'):
        list2[1]=list2[1][1:-1]
        for k in range(len(list2[1])):
            # ignore the situation '\' using at the end of the line
            if(list2[1][k:k+2]=="\\n"):
                if(k==0):
                    list2[1]='\n'+list2[1][2:]
                else:
                    list2[1]=list2[1][0:k]+'\n'+list2[1][(k+2):]
            elif(list2[1][k:k+2]=="\\r"):
                if(k==0):
                    list2[1]='\r'+list2[1][2:]
                else:
                    list2[1]=list2[1][0:k]+'\r'+list2[1][(k+2):]
            elif(list2[1][k:k+2]=="\\t"):
                if(k==0):
                    list2[1]='\t'+list2[1][2:]
                else:
                    list2[1]=list2[1][0:k]+'\t'+list2[1][(k+2):]
            elif(list2[1][k:k+2]=="\\\'"):
                if(k==0):
                    list2[1]='\''+list2[1][2:]
                else:
                    list2[1]=list2[1][0:k]+'\''+list2[1][(k+2):]
            elif(list2[1][k:k+2]=='\\\"'):
                if(k==0):
                    list2[1]='\"'+list2[1][2:]
                else:
                    list2[1]=list2[1][0:k]+'\"'+list2[1][(k+2):]
            elif(list2[1][k:k+2]=="\\\\"):
                if(k==0):
                    list2[1]="\\"+list2[1][2:]
                else:
                    list2[1]=list2[1][0:k]+"\\"+list2[1][(k+2):]
            elif(list2[1][k:k+2]=="\\0"):
                if(k==0):
                    list2[1]="\0"+list2[1][2:]
                else:
                    list2[1]=list2[1][0:k]+"\0"+list2[1][(k+2):]
        for ch in list2[1]:
            f2.write(bytearray([0]))
            f2.write(bytearray(ch,'utf-8'))
        array=0
        write_array(array)
    elif(list2[0]==".END"):
        f2.close()
        sys.exit(0)
