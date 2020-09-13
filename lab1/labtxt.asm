.ORIG x3000
LD R2,INPUT   ;x3200 as a pointer
LD R3,OOVER
AND R5,R5,#0  ;
ADD R5,R5,#-1 ;R5<-#-1 as a set
LEA R1,SZ     ;R1<-address of SZ
LD R6,NUM

CHECK   LDR R4,R2,#0
	ADD R4,R4,R1
        STR R5,R4,#0  ;set -1
        ADD R2,R2,#1  ;pointer++
        ADD R6,R6,#-1 ;counter--
        BRp CHECK
        AND R2,R2,#0  ;?
        ADD R2,R2,#-1
	AND R0,R0,#0
	ADD R0,R0,#-1
	ADD R2,R2,R1 ;point to SZ-1
        BR SAVE

SAVE    ADD R2,R2,#1 ;R2 as a pointer
	ADD R0,R0,#1 ;R0~number
        LDR R4,R2,#0
        BRz COUNT
        BRp SAVE
        ;BRn
        STR R0,R3,#0 ;number is stored in output backwards
        ADD R3,R3,#-1
        BR SAVE
;85-100 A
;84-75  B
;60-74  C
;0-59   D

COUNT   LD R1,OUTPUT ;pointer
	AND R2,R2,#0 ;R2 as a counter
        LD R4,N85
        BR A

A   LDR R3,R1,#0
    ADD R3,R3,R4
    BRn B
    ADD R2,R2,#1
    ADD R1,R1,#1
    BR A

B   LD R5,SCORES
    STR R2,R5,#0
    AND R2,R2,#0
    ADD R5,R5,#1
    LD R4,N75
    BR BB

BB  LDR R3,R1,#0
    ADD R3,R3,R4
    BRn C
    ADD R2,R2,#1
    ADD R1,R1,#1
    BR BB

C   STR R2,R5,#0
    AND R2,R2,#0
    ADD R5,R5,#1
    LD R4,N60
    BR CC

CC  LDR R3,R1,#0
    ADD R3,R3,R4
    BRn D
    ADD R2,R2,#1
    ADD R1,R1,#1
    BR CC

D   STR R2,R5,#0
    ADD R5,R5,#-1
    LDR R6,R5,#0
    ADD R2,R2,R6
    ADD R5,R5,#-1
    LDR R6,R5,#0
    ADD R2,R2,R6
    LD R6,N60
    ADD R2,R2,R6
    NOT R2,R2
    ADD R2,R2,#1
    STR R2,R5,#3
    HALT

ORI     .FILL x3000
INPUT   .FILL x3200
NUM     .FILL #60
OOVER   .FILL x403B
OUTPUT  .FILL x4000
N85     .FILL #-85
N75     .FILL #-75
N60     .FILL #-60
SCORES  .FILL x4100
SZ      .STRINGZ	"00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

.END