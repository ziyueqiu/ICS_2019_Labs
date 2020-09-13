import numpy as np
import struct
import sys
from tkinter import *
from tkinter import ttk

# initial
memory = np.zeros((65536),dtype=np.uint16)
memory_asm = ["NOP"]*65536
R = np.zeros((8),dtype=np.int16)
PC = 0
CC=[0]*3

# initial draw
root = Tk()
root.title("LC3 simulator")
root.geometry('700x600')
en = Entry(root, show=None)
en.pack()

# treeview for R0~7 and PC CC
treeshow = ttk.Treeview(root, columns = ["R0","R1","R2","R3","R4","R5","R6","R7","PC","CC"],show="headings",height=2)
treeshow.column("R0",width=60, anchor='center')
treeshow.column("R1",width=60, anchor='center')
treeshow.column("R2",width=60, anchor='center')
treeshow.column("R3",width=60, anchor='center')
treeshow.column("R4",width=60, anchor='center')
treeshow.column("R5",width=60, anchor='center')
treeshow.column("R6",width=60, anchor='center')
treeshow.column("R7",width=60, anchor='center')
treeshow.column("PC",width=60, anchor='center')
treeshow.column("CC",width=60, anchor='center')
treeshow.heading("R0",text="R0")
treeshow.heading("R1",text="R1")
treeshow.heading("R2",text="R2")
treeshow.heading("R3",text="R3")
treeshow.heading("R4",text="R4")
treeshow.heading("R5",text="R5")
treeshow.heading("R6",text="R6")
treeshow.heading("R7",text="R7")
treeshow.heading("PC",text="PC")
treeshow.heading("CC",text="CC")

# treeview
tree = ttk.Treeview(root,show="headings",height=10)
tree["columns"]=("address in hex","value in bin","value in hex","asm")
tree.column("address in hex",width=60, anchor='center')
tree.column("value in bin",width=100, anchor='center')
tree.column("value in hex",width=60, anchor='center')
tree.column("asm",width=100, anchor='center')

def jump():
    global en
    global tree
    var = int(en.get(),16)
    #PC = eval(var)
    x=tree.get_children()
    for item in x:
        tree.delete(item)
    for i in range(var,var+10):
        tree.insert('',i,values=(hex(i),bin(memory[i]),hex(memory[i]),memory_asm[i]))
    tree.pack()

button4 = Button(root, text="jump", command = jump).pack()

def exchange(low,high):
    return high+low*256

# PCoffset
def exchangeNeg(bit, unsh_get):
    if(bit==9):
        if(unsh_get & 0x100):
            return (unsh_get & 0x1ff)-2**9
        else:
            return unsh_get & 0x1ff
    elif(bit==5):
        if(unsh_get & 0x10):
            return (unsh_get & 0x1f)-2**5
        else:
            return unsh_get & 0x1f
    elif(bit==6):
        if(unsh_get & 0x20):
            return (unsh_get & 0x3f)-2**6
        else:
            return unsh_get & 0x3f
    elif(bit==11):
        if(unsh_get & 0x400):
            return (unsh_get & 0x7ff)-2**11
        else:
            return unsh_get & 0x7ff

def ExchangeToAsm(unsh_address, unsh_get):
    # global
    global memory
    global memory_asm
    # unsh_get is a unsigned 16 bit int
    LABEL = (unsh_get & 0xf000)>>12
    # NOP
    if(unsh_get & 0xfe00 == 0):
        sys.exit(0)
    else:
        memory_asm[unsh_address] = ""
    # ADD AND
    if(LABEL==int('0001',2) or LABEL==int('0101',2)):
        if(LABEL==int('0001',2)):
            memory_asm[unsh_address]+="ADD "
        else:
            memory_asm[unsh_address]+="AND "
        DR = (unsh_get & 0xe00)>>9
        memory_asm[unsh_address]+="R"+"{:}, ".format(DR)
        SR1 = (unsh_get & 0x1c0)>>6
        memory_asm[unsh_address]+="R"+"{:}, ".format(SR1)
        if((unsh_get & 0x20)>>5):
            IMM5 = exchangeNeg(5, unsh_get)
            memory_asm[unsh_address]+="#{:}".format(IMM5)
        else:
            SR2 = unsh_get & 0x7
            memory_asm[unsh_address]+="R"+"{:}".format(SR2)
        #print(memory_asm[unsh_address])
    # BR
    elif(LABEL==int('0000',2) and (unsh_get & 0xe00)):
        memory_asm[unsh_address]+="BR"
        if((unsh_get & 0x800)>>11):
            memory_asm[unsh_address]+="N"
        if((unsh_get & 0x400)>>10):
            memory_asm[unsh_address]+="Z"
        if((unsh_get & 0x200)>>9):
            memory_asm[unsh_address]+="P"

        PCoffset9 = unsh_address+1+exchangeNeg(9,unsh_get)
        memory_asm[unsh_address]+=" {:}".format(hex(PCoffset9))
        #print(memory_asm[unsh_address])
    # JMP JSRR
    elif((LABEL==int('0100',2) and (unsh_get & 0x800)==0) or LABEL==int('1100',2)):
        if(LABEL==int('1100',2)):
            memory_asm[unsh_address]+="JMP "
        else:
            memory_asm[unsh_address]+="JSRR "
        BaseR = (unsh_get & 0x1c0)>>6
        memory_asm[unsh_address]+="R"+"{:}".format(BaseR)
        #print(memory_asm[unsh_address])
    # JSR
    elif((LABEL==int('0100',2) and (unsh_get & 0x800)==0)):
        memory_asm[unsh_address]+="JSR "
        PCoffset11 = unsh_address+1+exchangeNeg(11,unsh_get)
        memory_asm[unsh_address]+=" {:}".format(hex(PCoffset11))
        #print(memory_asm[unsh_address])
    # LD LDI LEA ST STI
    elif(LABEL in [int('0010',2),int('1010',2),int('1110',2),int('0011',2),int('1011',2)]):
        if(LABEL == int('0010',2)):
            memory_asm[unsh_address]+="LD "
        elif(LABEL == int('1010',2)):
            memory_asm[unsh_address]+="LDI "
        elif(LABEL == int('1110',2)):
            memory_asm[unsh_address]+="LEA "
        elif(LABEL == int('0011',2)):
            memory_asm[unsh_address]+="ST "
        elif(LABEL == int('1011',2)):
            memory_asm[unsh_address]+="STI "
        DR = (unsh_get & 0xe00)>>9
        memory_asm[unsh_address]+="R"+"{:}".format(DR)
        PCoffset9 = unsh_address+1+exchangeNeg(9,unsh_get)
        memory_asm[unsh_address]+=" {:}".format(hex(PCoffset9))
        #print(memory_asm[unsh_address])
    # LDR STR
    elif(LABEL==int('0110',2) or LABEL==int('0111',2)):
        if(LABEL==int('0110',2)):
            memory_asm[unsh_address]+="LDR "
        else:
            memory_asm[unsh_address]+="STR "
        DR = (unsh_get & 0xe00)>>9
        memory_asm[unsh_address]+="R"+"{:}, ".format(DR)
        BaseR = (unsh_get & 0x1c0)>>6
        memory_asm[unsh_address]+="R"+"{:}, ".format(BaseR)
        offset6 = exchangeNeg(6, unsh_get)
        memory_asm[unsh_address]+="#{:}".format(offset6)
        #print(memory_asm[unsh_address])
    # NOT
    elif(LABEL==int('1001',2)):
        memory_asm[unsh_address]+="NOT "
        DR = (unsh_get & 0xe00)>>9
        memory_asm[unsh_address]+="R"+"{:}, ".format(DR)
        SR = (unsh_get & 0x1c0)>>6
        memory_asm[unsh_address]+="R"+"{:}".format(SR)
        #print(memory_asm[unsh_address])
    # RTI
    elif(LABEL==int('1000',2)):
        memory_asm[unsh_address]+="RTI"
        #print(memory_asm[unsh_address])
    # TRAP
    elif(LABEL==int('1111',2)):
        trapvect8 = unsh_get & 0xff
        memory_asm[unsh_address]+="TRAP "+"{:}".format(hex(trapvect8))
        #print(memory_asm[unsh_address])

def loadprogram():
    # global
    global memory
    global PC
    # read the file, save in string, to get the length
    datastr = input("please insert the .obj program : ")
    f1 = open(datastr,"rb")
    strf = f1.read()
    test_len = len(strf)
    f1.close()

    # read the file two bits by two bits
    f1 = open(datastr,"rb")
    (unsh_addresslow,unsh_addresshigh,) = struct.unpack("BB",f1.read(2))
    unsh_address = exchange(unsh_addresslow,unsh_addresshigh)
    PC = unsh_address
    for i in range(int(test_len/2)-1):
        (unsh_getlow,unsh_gethigh,) = struct.unpack("BB",f1.read(2))
        unsh_get=exchange(unsh_getlow,unsh_gethigh)
        memory[unsh_address]=unsh_get
        ExchangeToAsm(unsh_address, unsh_get)
        unsh_address+=1
    f1.close()

    newit()

def SetCC(data):
    global CC
    if(data==0):
        CC=[0,1,0]
    elif(data>0):
        CC=[0,0,1]
    else:
        CC=[1,0,0]

def newit():
    global tree
    global treeshow
    global R
    global PC
    global CC
    x=tree.get_children()
    for item in x:
        tree.delete(item)
    for i in range(PC,PC+10):
        tree.insert('',i,values=(hex(i),bin(memory[i]),hex(memory[i]),memory_asm[i]))
        """
        if(i == PC):
            tree.item(tree.get_children()[0],tags='PC')
            tree.tag_configure('PC',background='yellow')"""
    tree.pack()
    y=treeshow.get_children()
    for item in y:
        treeshow.delete(item)
    treeshow.insert('',0,values=(hex(R[0]),hex(R[1]),hex(R[2]),hex(R[3]),hex(R[4]),hex(R[5]),hex(R[6]),hex(R[7]),hex(PC),'N'*CC[0]+'Z'*CC[1]+'P'*CC[2]))
    treeshow.pack()

def next():
    # global
    global memory
    global PC
    global CC
    global R
    # PC
    PC+=1
    # unsh_get is a unsigned 16 bit int
    unsh_get=memory[PC-1]
    LABEL = (unsh_get & 0xf000)>>12
    # ADD AND
    if(LABEL==int('0001',2) or LABEL==int('0101',2)):
        DR = (unsh_get & 0xe00)>>9
        SR1 = (unsh_get & 0x1c0)>>6
        if(LABEL==int('0001',2)):
            if((unsh_get & 0x20)>>5):
                IMM5 = exchangeNeg(5, unsh_get)
                R[DR]=R[SR1]+IMM5
            else:
                SR2 = unsh_get & 0x7
                R[DR]=R[SR1]+R[SR2]
        else:
            if((unsh_get & 0x20)>>5):
                IMM5 = exchangeNeg(5, unsh_get)
                R[DR]=R[SR1] & IMM5
            else:
                SR2 = unsh_get & 0x7
                R[DR]=R[SR1] & R[SR2]
        SetCC(R[DR])

    # BR
    elif(LABEL==int('0000',2) and (unsh_get & 0xe00)):
        if((CC[0] and (unsh_get & 0x800)>>11) or (CC[1] and (unsh_get & 0x400)>>10) or (CC[2] and (unsh_get & 0x200)>>9)):
            PC+=exchangeNeg(9,unsh_get)
    # JMP JSRR
    elif((LABEL==int('0100',2) and (unsh_get & 0x800)==0) or LABEL==int('1100',2)):
        BaseR = (unsh_get & 0x1c0)>>6
        # JMP
        if(LABEL==int('1100',2)):
            PC=R[BaseR]
        # JSRR
        else:
            R[7]=PC
            PC=R[BaseR]
    # JSR
    elif((LABEL==int('0100',2) and (unsh_get & 0x800)==0)):
        P[7]=PC
        PC += exchangeNeg(11,unsh_get)
    # LD LDI LEA ST STI
    elif(LABEL in [int('0010',2),int('1010',2),int('1110',2),int('0011',2),int('1011',2)]):
        DR = (unsh_get & 0xe00)>>9
        PCoffset9 = exchangeNeg(9,unsh_get)+PC
        if(LABEL == int('0010',2)):
            R[DR]=memory[PCoffset9]
            SetCC(R[DR])
        elif(LABEL == int('1010',2)):
            R[DR]=memory[memory[PCoffset9]]
            SetCC(R[DR])
        elif(LABEL == int('1110',2)):
            R[DR]=PCoffset9
            SetCC(R[DR])
        elif(LABEL == int('0011',2)):
            memory[PCoffset9]=R[DR]
        elif(LABEL == int('1011',2)):
            memory[memory[PCoffset9]]=R[DR]
    # LDR STR
    elif(LABEL==int('0110',2) or LABEL==int('0111',2)):
        DR = (unsh_get & 0xe00)>>9
        BaseR = (unsh_get & 0x1c0)>>6
        offset6 = exchangeNeg(6, unsh_get)
        if(LABEL==int('0110',2)):
            R[DR]=memory[R[BaseR]+offset6]
            SetCC(R[DR])
        else:
            memory[R[BaseR]+offset6]=R[DR]
    # NOT
    elif(LABEL==int('1001',2)):
        DR = (unsh_get & 0xe00)>>9
        SR = (unsh_get & 0x1c0)>>6
        R[DR]= ~R[SR]
        SetCC(R[DR])
    # RTI
    # TRAP only HALT
    elif(LABEL==int('1111',2)):
        newit()
        return 0
    newit()
    return 1

ent=Entry(root, show=None)
ent.pack()

def Set(event):
    global tree
    global ent
    global memory
    var = int(ent.get(),16)
    item_text = tree.item(tree.selection()[0],"values")
    ExchangeToAsm(eval(item_text[0]), var)
    memory[eval(item_text[0])]=var
    newit()

def SetValue(event):
    global tree
    # Double-Button-1
    if(len(tree.selection())>1):
        print("select more than 1 row")
        return
    else:
        Set(event)

tree.bind('<Double-Button-1>',SetValue)

def Show(event):
    global treeshow
    global ent
    global R
    l = ent.get().split()
    R[eval(l[0][1:])]=int(l[1],16)
    newit()

def SetShow(event):
    global treeshow
    # Double-Button-1
    if(len(treeshow.selection())>1):
        print("select more than 1 row")
        return
    else:
        Show(event)

treeshow.bind('<Double-3>',SetShow)

def runover():
    global R
    global PC
    i=0
    while(next()!=0):
        i+=1
    newit()

# arrange the looking
button3 = Button(root, text="load program", command = loadprogram).pack()
button1 = Button(root, text="runover", command = runover).pack()
button2 = Button(root, text="next", command = next).pack()

newit()

root.mainloop() # 进入消息循环
