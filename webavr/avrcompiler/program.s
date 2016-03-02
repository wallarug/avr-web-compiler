;;; Data definitions go here
.section .data

;;; Code definition goes here
.section .text
	.global asm_function

asm_function:
	LDI R24,55
	LDI R17,23
	
	LSL R24
	LSR R17
	
	ADD R24,R17
	CLR R25
	ret
.end