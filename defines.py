
#Posiciones en memoria dentro del stack a transmitir

digi_outputs = {"DO1": 0, "DO2": 1, "DO3": 2, "DO4": 3}
digi_inputs =  {"DI1": 4, "DI2": 5, "DI3": 6, "DI4": 7,"DI5": 8, "DI6": 9, "DI7": 10, "DI8": 11}


io_positions =  {"DO1": 0, "DO2": 1, "DO3": 2, "DO4": 3, "DI1": 4, "DI2": 5, "DI3": 6, "DI4": 7,"DI5": 8, "DI6": 9, "DI7": 10, "DI8": 11}

#ID de cada instruccion

ldr_opcodes = {"SET"			:0x01,
				"NSET"			:0x02,
				"ADD_R"			:0x03,
				"CEIL"			:0x04,
				"CMP_G_R"		:0x05,
				"CMP_M_R"		:0x06,
				"CMP_GE_R"		:0x07,
				"CMP_ME_R"		:0x08,
				"CMP_E_R"		:0x09,
				"CMP_NE_R"		:0x0A,
				"DIV_R"			:0x0B,
				"FLOOR"			:0x0C,
				"JMP"			:0x0D,
				"JMPN"			:0x0E,	
				"MOD_R"			:0x0F,
				"MOVE_R"		:0x10,
				"MUL_R"			:0x11,
				"NEG"			:0x12,
				"POS"			:0x13,
				"RST_C"			:0x14,	
				"ROUND"			:0x15,
				"FF_RS"			:0x16,
				"SET_C"			:0x17,	
				"S_CD"			:0x18,	
				"S_CU"			:0x19,	
				"S_CUD"			:0x1A,
				"S_ODT"			:0x1B,
				"S_ODTS"		:0x1C,
				"S_OFFDT"		:0x1D,
				"S_PEXT"		:0x1E,
				"S_PULSE"		:0x1F,
				"FF_SR"			:0x20,
				"SUB_R"			:0x21,
				"TRUNC"			:0x22,	
				"AND"			:0x23,
				"OR"			:0x24,
				"NAND"			:0x25,
				"NOR"			:0x26,
				"XOR"			:0x27,
				"NOT"			:0x28,
				"SET_B"			:0x29,
				"SET_R"			:0x2A,
				"SET_I"			:0x2B,
				"ABS"			:0x2C,
				"MOVE_W"		:0x2D,
				"SET_F"			:0x2E,
				"NOP"			:0xFE,
				"PROGRAM_END"	:0xFF}		

timer_opcodes = {"S_CD"		:0x18,	
				"S_CU"			:0x19,	
				"S_CUD"			:0x1A,
				"S_ODT"			:0x1B,
				"S_ODTS"		:0x1C,
				"S_OFFDT"		:0x1D,
				"S_PEXT"		:0x1E,
				"S_PULSE"		:0x1F}