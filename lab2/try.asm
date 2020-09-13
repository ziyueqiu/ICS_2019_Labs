.ORIG x3000
AND R1,R1,#0 ; initialization
ADD R1,R1,#2 ; start from 2
AND R2,R2,#0 ; follow
ADD R2,R2,#1
AND R3,R3,#0 ; R3 store the result

LOOP AND R4,R1,R0 ; R4 check the bit
     BRz ADDD
     ADD R3,R3,R2
ADDD ADD R2,R2,R2
     ADD R1,R1,R1
     BRnp LOOP
     AND R4,R2,R0
     BRz SAVE
     ADD R3,R3,R2

SAVE AND R0,R0,#0
     ADD R0,R0,R3
     HALT
.END