import sys
sys.path.append('./judger/')
sys.path.append('..')

from judge import *
from utils import dump
import json

code = r"""
#include <bits/stdc++.h>
using namespace std;

typedef unsigned long long ULL;

#define AC

#ifdef TLE
ULL fibo(int n)
{
	if(n == 0 || n == 1) return n;
	else
		return fibo(n-1) + fibo(n-2);
}
#endif

#ifdef AC
#define N 1000000
ULL a[N+5];
ULL fibo2(int n)
{
	if(n == 0 || n == 1) return n;
	else if(!a[n])
		return (a[n] = fibo2(n-1) + fibo2(n-2));
	else
		return a[n];
}
#endif

int n;
int main()
{
	#ifdef AC
	while(cin >> n)
		cout << fibo2(n) << '\n';
	#endif

	#ifdef TLE
	while(cin >> n)
		cout << fibo(n) << '\n';
	#endif
	return 0;
}
"""

code_2 = r"""int main()
{
    *((int *)0) = 1;
    return 0;
}"""

a = Judger()

CASE = 4

res, meta = a.judge(1, JUDGE_CPP, code_2, 3.0, 65536, CASE)

x = [result_type[i] for i in res]
print(x)

for i in range(CASE):
	a.debug_dump(i)
