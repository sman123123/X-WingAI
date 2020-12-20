from itertools import combinations

def P(n, r, p):
	c = len(list(combinations([x+1 for x in range(n)], r)))
	q = 1 - p
	return c * (p ** r) * (q ** (n - r))

def Probability(n, r, p):
	x = 0.0
	for _ in range(r, n+1):
		x += P(n, _, p)
	return f"{round(x*100)}%"