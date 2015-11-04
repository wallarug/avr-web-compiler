;;; Data definitions go here
.section .data

;;; Code definition goes here
.section .text
	.global asm_function

asm_function:
	
	LDI R16,1
	LDI R17,2
	LDI R18,3
	LDI R19,4
	LDI R20,5
	
	ADD R16,R17
	ADD R16,R18
	ADD R16,R19
	ADD R16,R20
	
	MOV R24, R16
	CLR R25
	ret
.end
