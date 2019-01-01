; *********************************************************************************
; *********************************************************************************
;
;		File:		bitwise.asm
;		Purpose:	16 bit bitwise operations
;		Date : 		1st January 2019
;		Author:		paul@robsons.org.uk
;
; *********************************************************************************
; *********************************************************************************

@word 	sys.and()
		ld 		a,h
		and 	b
		ld 		h,a
		ld 		a,l
		and 	c
		ld 		l,a
		ret

@word 	sys.xor()
		ld 		a,h
		xor 	b
		ld 		h,a
		ld 		a,l
		xor 	c
		ld 		l,a
		ret
		
@word 	sys.or()
		ld 		a,h
		or 		b
		ld 		h,a
		ld 		a,l
		or 		c
		ld 		l,a
		ret
		
