;初判断，利用R2：R1>R0跳转函数3；R1=R0，HALT；<则顺序执行
;SPACE申请16个连续地址存减数，R5LEA存SPACE的第一个地址

;函数0：初始化计数器R3=0，R1取反加一的结果放进R4,顺序执行
;函数1：R4存进地址，R5地址++，计数器R3++，R4左移，是n就跳转函数1，存完往下执行
;函数2：
;计数器--，BRn 函数3，地址--，R2取出地址的内容，R2加R0
;   z:跳转函数4
;   n:跳回函数2
;   p:R0<-R2,跳回函数2
;函数3：交换R0和R1,利用R2，结束后跳回函数0
;函数4：R0<-R1，HALT
;HALT

.ORIG	x3000
;first, specify R1 and R0
NOT R4,R1
ADD R4,R4,#1
ADD R2,R4,R0
BRz THEEND
BRn F3
;save the address of the SPACE in R5
LEA R5,SPACE

F0  AND R3,R3,#0
    ;R4 = -R1 in order to save the minus
    NOT R4,R1
    ADD R4,R4,#1
F1  STR R4,R5,#0
    ADD R5,R5,#1
    ADD R3,R3,#1
    ADD R4,R4,R4
    BRn F1
F2  ADD R3,R3,#-1
    BRn F3
    ADD R5,R5,#-1
    LDR R2,R5,#0
    ADD R2,R2,R0
    BRz F4
    BRn F2
    AND R0,R0,#0
    ADD R0,R0,R2
    BR  F2
F3  AND R2,R2,#0
    ADD R2,R2,R0 ;R2=R0
    AND R0,R0,#0
    ADD R0,R0,R1 ;R0=R1
    AND R1,R1,#0
    ADD R1,R1,R2 ;R1=R0
    BR  F0
F4  AND R0,R0,#1
    ADD R0,R1,#0
THEEND  HALT
SPACE   .BLKW	16

.END