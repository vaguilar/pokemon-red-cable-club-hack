.MEMORYMAP
SLOTSIZE $10000
DEFAULTSLOT 0
SLOT 0 $0
.ENDME

.ROMBANKSIZE $10000
.ROMBANKS 2

.BANK 0 SLOT 0

.ORG $c5d6

	ld a, $63 ;$80

Start:

; save a
	push af

; write with random byte
    ld hl, $c3a0    ; dst  $c3a0  OAM buffer
    ld bc, $188     ; len (16 * 20)
    call $36e0      ; memset

; write string to screen
    ld de, Hello 	; src
    ld hl, $c457    ; dst, middle of OAM buffer
    call $1955      ; PlaceString

; delay
	halt
	halt
	halt
	halt
	halt
	halt
	halt

; next tile
	pop af
	inc a

; at last tile?
	ld c, $6c
	cp c

; no, back to start
	jp nz, Start

; yes, reset to tile $63 and back to start
	ld a, $63
	jp Start

; Hello World!
Hello:
    .db $7f
    .db $87
    .db $84
    .db $8b
    .db $8b
    .db $8e
    .db $7f
    .db $96
    .db $8e
    .db $91
    .db $8b
    .db $83
    .db $e7
    .db $7f
    .db $50
