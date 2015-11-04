;;; Data definitions go here
.section .data

;;; Code definition goes here
.section .text
	.global asm_function

asm_function:
	LDI R16, 9
	LDI R17, 12
	LDI R18, 15
	MUL R16, R16
	;;ROR R18
	MOV R16, R0 ;;result of mul in R16
	MUL R17, R17
	MOV R17, R0 ;;result of mul in R17
	MUL R18, R18
	MOV R18, R0 ;;result of mul in R18
	ADD R16, R17 ;;result in R16
	CP R18, R16
	
	BREQ true
	BRNE false
	true:	
		LDI R16, 1
		MOV R24, R16
		CLR R25
		call print_integer
		ret
	false:	
		LDI R16, 0
		MOV R24, R16
		CLR R25
		call print_integer
		ret
	ret
.end
