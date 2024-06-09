# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 16:33:29 2017
	
@author: selim
"""
import random
#distance between city matrix 
table_way = [[0, 3, 4, 5,10],
			[3, 0, 3, 5, 8 ],
			[4, 3, 0, 4, 6],
			[5, 5, 4, 0, 6],
			[10,8, 6, 6, 0]]

nb_city = len(table_way[0])

#https://fr.wikipedia.org/wiki/Algorithme_de_Dijkstra

##################################################
#minimum local

def compute_travel_distance(t):
		c = 0
		for i in range(0, len(t)):
			 c = c + table_way[t[i]][t[(i + 1) % (len(t))]]
		return c

def travel_salesman_prob():
        way =[]

        # start with random value
        s = random.randint(0,nb_city -1)

		#create fist travel
		for c in range(s, s + nb_city):
			 way.append(c % (nb_city))
		 
		#for each element from list swap two concecutive element and test impact
		l = len(way)
		minimal = compute_travel_distance(way)
		i = 0
		j = 0
		while i < len(way):
			 t = way[j % l]
			 way[j % l] = way[(j + 1) % l]
			 way[(j + 1) % l] = t
			 current = compute_travel_distance(way)
			 i = i + 1

			 if current > minimal:
				  t = way[j % l]
				  way[j % l] = way[(j + 1) % l]
				  way[(j + 1) % l] = t
			 else:
				  i = 0
				  minimal = current
			 j = j + 1

		return (way,minimal)


#############################################################################
def debug_population(p):
		for a in p:
			 print(a, "->",compute_travel_distance(a)) 

def create_population(p_nb):
		p=[]
		for i in range(0,p_nb):
			 s = random.randint(0,nb_city -1)
			 invers = random.randint(0,2*(nb_city -1))
			 signe = random.randint(0,1)
			 a = []
			 for j in range(s ,s + nb_city):
				  a.append( (j * ((-1)**signe)) % (nb_city))
			 if invers < nb_city - 1:
				  t = a[invers % nb_city]
				  a[invers % nb_city] = a[(invers + 1) % nb_city]
				  a[(invers + 1) % nb_city] = t	  
			 p.append(a)
		return p

def select_genitor(p, nb_genitor):
		#select the smaller genitor with Stochastic universal sampling
		genitor = []
		#sort from smaller to bigger  
		for a in p:
			 smallest = True
			 c = compute_travel_distance(a)
			 i = 0
			 for b in genitor:
				  g = compute_travel_distance(b)
				  if g > c:
						genitor.insert(i,a)
						smallest = False
						break
				  i = i + 1
			 if smallest :
				  genitor.append(a)
		s = len(genitor)

		#reduce the pressure h(f(x)), f(x) compute_travel_distance, h monotonic
		#compute statistic
		#select with SUS (stochastic universal sampling)
		for i in range(s,nb_genitor,-1):
			 genitor.pop()

		return genitor

def is_inside(value, start, size, parent):
		r = False
		for j in range(start,start + size):
			 r = r | (value == parent[j])
		
		return r

def crossover(aparent,bparent):
		
		#select segment to copy from first parent
		start = random.randint(0, len(aparent) - 1)
		size = random.randint(0, len(aparent) - start - 1)

		children = aparent.copy()
		#copy remaining at the same order

		j = 0
		#full fill before selected genome segment
		for i  in range(0, start):
			 for k in range(j, len(bparent)):
				  value = bparent[j]
				  if not(is_inside(value,start, size, aparent)):
						children[i] = value
						j = j + 1
						break
				  else:
						j = j + 1
		#full fill after selected genome segment		  
		for i  in range(start + size, len(aparent)):
			 for k in range(j,len(bparent)):
				  value = bparent[k]
				  if not(is_inside(value,start, size, aparent)):
						children[i] = value
						j = j + 1
						break
				  else:
						j = j + 1
						
		return children
	
def mutation(aparent):
		# switch two gen randomly
		l = len(aparent)
		#probabily of mutation is very low
		start = random.randint(0, 2*l)
	
		if start < ((l - 1)/2):
			 t = aparent[start % l]
			 aparent[start % l] = aparent[(l - start - 1) % l]
			 aparent[(l - start - 1) % l] = t
		
		return aparent

def travel_salesman_pgen():
		#population randomly created
		p_nb = 6
		nb_genitor = 3

		p = create_population(p_nb)
		for i in range(0,22):
			 np =[]
			 genitor = select_genitor(p, nb_genitor)
			 np.extend(genitor)
			 children = crossover(genitor[0],genitor[1])
			 np.append(mutation(children))
			 children = crossover(genitor[0],genitor[2])
			 np.append(mutation(children))
			 children = crossover(genitor[1],genitor[2])
			 np.append(mutation(children))
			 p = np
		debug_population(p)	

def main():
		print(travel_salesman_prob())
		travel_salesman_pgen()

if __name__ == '__main__':
		main()
