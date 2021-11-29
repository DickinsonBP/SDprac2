
```c
unsigned char x = 0;		// valor actual de l'angle
unsigned char pulse_state;	// estat actual del pols
unsigned short y_mic;		// número de microsegons en 1

main () {
    inicializaciones();
	fijar_divfrectim0();
    inicializacion_timer0();

    do {
		tareas_independientes();
		swiWaitForVBlank();

		scanKeys();

		manegar_botons(keysDown());
    } while (1);

	void manegar_botons (int botons) {
		if ((keysDown() & KEY_L) && x >= 10) {
			x -= 10;
		} else if ((keysDown() & KEY_R) && x <= 170) {
			x += 10;
		} else if ((keysDown() & KEY_LEFT) && x > 0) {
			x -= 1;
		} else if ((keysDown() & KEY_RIGHT) && x < 180) {
			x += 1;
		}

		y_mic = 1000 * (180 + x) / 180;
		fijar_divfrectimer0(y_mic);
	}
}
```

```gas
RSI_timer0:
	push {r0-r6, lr}
	ldr r0, =pulse_state
	ldrb r1, [r0]
	ldr r2, =REG_SERVO
	ldrb r3, [r2]
	ldr r4, =y_mic
	ldrh r5, [r4]
	cmp r1, #0
	bne .LpulseNot0
	mov r1, #1
	orr r3, #0b1000
.LpulseNot0:
	mov r1, #0
	bic r3, #0b1000
	ldr r6, =20000
	rsb r5, r6

.LRsi_Fin: 
	strb r1, [r0]
	strb r3, [r2]
	mov r0, r5
	bl fijar_divfreqtim0

	pop {r0-r6, pc}

RSI_timer0:
push {r0-r5, lr}
	mov r1, =y_mic
	ldrh r0, [r1]			@; num_mic@r0 = y_mic
	mov r4, =REG_SERVO		@; reg_servo@r4 = &REG_SERVO
	ldrh r3, [r4]			@; servo_original@r3 = REG_SERVO
	orr r5, r3, #0x04		@; servo@r5 = servo_original@r3 | 0x04
	strh r5, [r4]			@; REG_SERVO = servo@r5

	mul r1, r0, #13			@; num_iteracions@r1 = num_mic@r0 * (13 = (40 OPS/µs / 3 OPS))
	mov r2, #0				@; iteracio@r2 = 0
.LRSI_timer0_loop:			@; do {
	add r2, #1				@;		iteracio@r2++
	tst r1, r2
	bne .LRSI_timer0_loop	@; } while (iteracio@r2 < num_iteracions@r1)

	strh r3, [r4]			@; REG_SERVO = servo_original@r3

pop {r0-r5, pc}


@; retorna un valor entre 1000 i 2000 µs
fijar_divfrectim0():
push {r1-r3, lr}
	
    bl iniciar_RTC		@; iniciar_RTC()

    mov r1, #100
    mov r2, #18000
    mla r0, r1, r2, r0  @; numerador@r0 = 18000 + 100 * micros@r0
    mov r1, #18         @; divisor@r1 = 18
    swi 9               @; quocient@r0 = numerador@r0 / divisor@r1
						@; COMPTE, TAMBÉ MODIFICA r3

    bl parar_RTC		@; parar_RTC()
pop {r1-r3, pc}
```