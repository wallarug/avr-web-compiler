;;; Data definitions go here
.section .data
	pair11: .byte 12   ; First number of first pair 12
	pair12: .byte 23   ; Second number of first pair 23
	pair21: .byte 55   ; First number of second pair 55
	pair22: .byte 123  ; Second number of second pair 122
;;; Code definition goes here
.section .text
	.global asm_function

asm_function:
	LDS R28,pair11
	LDS R29,pair12
	LDS R30,pair21
	LDS R31,pair22
	
	ADD R28,R29
	ADD R30,R31
	
	CP R28,R30
	BREQ equals
	
	LDI R24,0
	CLR R25
	CALL print_integer
	ret
equals:
	LDI R24,1
	CLR R25
	CALL print_integer
	ret
.end
