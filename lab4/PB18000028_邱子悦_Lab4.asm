.ORIG x3000
_START  LD  R6, BASE
        JSR MAIN
        HALT

MAIN    ADD R6, R6, #-1
        STR R7, R6, #0
        ADD R6, R6, #-1
        JSR OVERFLOW
        STR R0, R6, #0 ; push R0
        AND R0, R0, #0 ; clean R0
        AND R2, R2, #0
        ADD R2, R2, #6
L0      ADD R6, R6, #-1
        JSR OVERFLOW
        STR R0, R6, #0
        ADD R2, R2, #-1
        BRp L0
        GETC
        LD  R2, ASC
        ADD R0, R0, R2
        ADD R6, R6, #-1
        JSR OVERFLOW
        STR R0, R6, #0
        JSR FUNC
        LDR R0, R6, #0
        ADD R6, R6, #1
        JSR EMPTY
        LDR R7, R6, #0
        RET

EMPTY   LD  R5, BASE
        NOT R5, R5
        ADD R5, R5, #1
        ADD R5, R5, R6
        BRn END
        LD  R0, EM
        PUTS
        HALT
OVERFLOW    LD  R5, TOP
            NOT R5, R5
            ADD R5, R5, #1
            ADD R5, R5, R6
            BRp END
            LD  R0, OVER
            PUTS
            HALT

BASE .FILL xF000 ; assume the stack is over there
TOP  .FILL xE000 ; the highest
EM   .STRINGZ "stack empty"
OVER .STRINGZ "stack overflow"


; stack save--R7 R0
; changing--R6(SP)
; save up to down: R7,n,a,b,c,d,e,f,R0

; R0 use as t == should be stored
; R1 changing at first
; R6 stack pointers
; R7 RET == should be stored
FUNC    ADD R6, R6, #-1
        STR R7, R6, #0  ; push R7
        JSR OVERFLOW
        GETC
        LD  R1, ASC    ;-'0'
        ADD R0, R0, R1
        LDR R1, R6, #2 ; a
        ADD R0, R0, R1
        LDR R1, R6, #3 ; b
        ADD R0, R0, R1
        LDR R1, R6, #4 ; c
        ADD R0, R0, R1
        LDR R1, R6, #5 ; d
        ADD R0, R0, R1
        LDR R1, R6, #6 ; e
        ADD R0, R0, R1
        LDR R1, R6, #7 ; f
        ADD R0, R0, R1
        LDR R1, R6, #1 ; n
        ADD R1, R1, #-1 ; n-1
        BRnz FINAL

        ADD R6, R6, #-1
        JSR OVERFLOW
        STR R0, R6, #0 ; push R0 = t
        AND R2, R2, #0 ; counter
        ADD R2, R2, #6 ; abcdef
L1      ADD R6, R6, #-1
        JSR OVERFLOW
        LDR R0, R6, #9 ; f-e-d-c-b-a
        STR R0, R6, #0
        ADD R2, R2, #-1
        BRp L1
        ADD R6, R6, #-1
        JSR OVERFLOW
        STR R1, R6, #0 ; push n-1
        JSR FUNC ; x

        LDR R1, R6, #2  ; n back caller
        ADD R1, R1, #-2 ; n-2
        ADD R6, R6, #-1
        JSR OVERFLOW
        STR R0, R6, #0 ; push R0 = t  callee
        AND R2, R2, #0 ; counter
        ADD R2, R2, #6 ; abcdef
L2      ADD R6, R6, #-1
        JSR OVERFLOW
        LDR R0, R6, #10 ; f-e-d-c-b-a
        STR R0, R6, #0
        ADD R2, R2, #-1
        BRp L2
        ADD R6, R6, #-1
        JSR OVERFLOW
        STR R1, R6, #0 ; n-2
        JSR FUNC ; y
        ADD R0, R0, #-1 ; t-1
        LDR R2, R6, #0
        ADD R0, R0, R2  ; t+y-1
        ADD R6, R6, #1
        JSR EMPTY
        LDR R2, R6, #0
        ADD R0, R0, R2  ; t+x+y-1
        ADD R6, R6, #1
        JSR EMPTY
        
FINAL   ADD R6, R6, #8 ; point to R0 now
        JSR EMPTY
        LDR R7, R6, #-8 ; R7 back
        LDR R2, R6, #0 ; save the return R0
        STR	R0, R6, #0 ; push t
        ADD R0, R2, #0 ; R0 back
END     RET

ASC     .FILL x-30  ; -'0'

.END