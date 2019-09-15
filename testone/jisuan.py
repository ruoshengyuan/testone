

def Night():
	result = []
	for i in range(1,10) :
		for m in range(1,10):
			c = i*m
			result.append((i,m,c))
	return result

NIGHT = Night() 

def Jia_9():
	result = []
	for i in range(len(NIGHT)) :
		for m in range (1,100):
			if m+NIGHT[i][2]<=100:
				shizi = str(m)+'+'+str(NIGHT[i][0])+'*'+str(NIGHT[i][1])+'='
				shizi2 = str(NIGHT[i][0])+'*'+str(NIGHT[i][1])+'+'+str(m)+'='
				daan = m+NIGHT[i][2]
				result.append((shizi,daan))
				result.append((shizi2,daan))
	return result

JIA_9 =  list(set(Jia_9()))

def Jian_9():
	result = []
	for i in range(len(NIGHT)) :
		for m in range (1,100):
			if m-NIGHT[i][2]>=0:
				shizi = str(m)+'-'+str(NIGHT[i][0])+'*'+str(NIGHT[i][1])+'='
				daan = m-NIGHT[i][2]
				result.append((shizi,daan))
	for i in range(len(NIGHT)) :
		for m in range (1,100):
			if NIGHT[i][2]-m>=0:
				shizi2 = str(NIGHT[i][0])+'*'+str(NIGHT[i][1])+'-'+str(m)+'='
				daan2 = NIGHT[i][2]-m
				result.append((shizi2,daan2))
	return result

JIAN_9 =  list(set(Jian_9()))


def Jia_qian():
	result = []
	for i in range (1,100):
		for m in range (1,100):
			for n in range (1,100):
				if i+m+n<=100 and i+m+n>=20:
					shizi = str(i)+'+'+str(m)+'+'+str(n)+'='
					daan = i+m+n
					result.append((shizi,daan))

	for i in range (1,100):
		for m in range (1,100):
			if i+m>=0 and i+m<=100  :
				for n in range (1,100):
					if i+m-n>=0 :
						shizi3 = str(i)+'+'+str(m)+'-'+str(n)+'='
						daan3 = i+m-n
						result.append((shizi3,daan3))
	return result

JIA_QIAN = list(set(Jia_qian()))

