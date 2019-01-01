; *********************************************************************************
; *********************************************************************************
;
;		File:		divide.asm
;		Purpose:	16 bit unsigned divide
;		Date : 		1st January 2019
;		Author:		paul@robsons.org.uk
;
; *********************************************************************************
; *********************************************************************************

;	Actually calculates HL / BC

@word 	sys.divide()
	push 	bc
	push 	de
	ex 		de,hl
	ld 		l,c
	ld 		h,b
	call 	DIVDivideMod16
	ex 		de,hl
	pop 	de
	pop 	bc
	ret

;	Actually calculates HL % BC

@word 	sys.modulus()
	push 	bc
	push 	de
	ex 		de,hl
	ld 		l,c
	ld 		h,b
	call 	DIVDivideMod16
	pop 	de
	pop 	bc
	ret

; *********************************************************************************
;
;			Calculates DE / HL. On exit DE = result, HL = remainder
;
; *********************************************************************************

DIVDivideMod16:

	push 	bc
	ld 		b,d 				; DE 
	ld 		c,e
	ex 		de,hl
	ld 		hl,0
	ld 		a,b
	ld 		b,8
Div16_Loop1:
	rla
	adc 	hl,hl
	sbc 	hl,de
	jr 		nc,Div16_NoAdd1
	add 	hl,de
Div16_NoAdd1:
	djnz 	Div16_Loop1
	rla
	cpl
	ld 		b,a
	ld 		a,c
	ld 		c,b
	ld 		b,8
Div16_Loop2:
	rla
	adc 	hl,hl
	sbc 	hl,de
	jr 		nc,Div16_NoAdd2
	add 	hl,de
Div16_NoAdd2:
	djnz 	Div16_Loop2
	rla
	cpl
	ld 		d,c
	ld 		e,a
	pop 	bc
	ret
		
		