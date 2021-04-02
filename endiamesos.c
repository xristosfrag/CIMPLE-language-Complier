int main()
{
	L_1: e = A;	//[':=', 'A', '', 'e']
	L_2: x = Y;	//[':=', 'Y', '', 'x']
	L_3: f = b;	//[':=', 'b', '', 'f']
	L_4: retv e  
	L_5: end_block P11  
	L_6: begin_block P1  
	L_7: b = X;	//[':=', 'X', '', 'b']
	L_8: par X REF 
	L_9: par T_0 RET 
	L_10: call P11  
	L_11: e = T_0;	//[':=', 'T_0', '', 'e']
	L_12: par X CV 
	L_13: par Y REF 
	L_14: par T_1 RET 
	L_15: call P1  
	L_16: e = T_1;	//[':=', 'T_1', '', 'e']
	L_17: X = b;	//[':=', 'b', '', 'X']
	L_18: retv e  
	L_19: end_block P1  
	L_20: begin_block small  
	L_21: > b 1 23
	L_22: jump   25
	L_23: < f 2 29
	L_24: jump   25
	L_25: + g 1 T_2
	L_26: + f b T_3
	L_27: < T_2 T_3 29
	L_28: jump   34
	L_29: par g CV 
	L_30: par T_4 RET 
	L_31: call P1  
	L_32: f = T_4;	//[':=', 'T_4', '', 'f']
	L_33: jump   35
	L_34: f = 1;	//[':=', '1', '', 'f']
	L_35: halt   
	L_36: end_block small  
}