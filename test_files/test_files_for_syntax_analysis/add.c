#include <stdio.h>

int main()
{
	int x,sum,T_0,T_1;
	L_0:
	L_1: scanf("%d", &x);	//['inp', 'x', '', '']
	L_2: sum = 5;	//[':=', '5', '', 'sum']
	L_3: if(x > 0) goto L_5;	//['>', 'x', '0', 5]
	L_4: goto L_12;	//['jump', '', '', 12]
	L_5: T_0 = sum + sum;	//['+', 'sum', 'sum', 'T_0']
	L_6: sum = T_0;	//[':=', 'T_0', '', 'sum']
	L_7: printf("%d\n",sum);	//['out', 'sum', '', '']
	L_8: return (sum);	//['retv', 'sum', '', '']
	L_9: T_1 = x - 1;	//['-', 'x', '1', 'T_1']
	L_10: x = T_1;	//[':=', 'T_1', '', 'x']
	L_11: goto L_3;	//['jump', '', '', 3]
	L_12: printf("%d\n",sum);	//['out', 'sum', '', '']
	L_13: {} 
}