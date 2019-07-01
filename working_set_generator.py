import random

window = 100
quantity_of_pages_most_use = 5
proportion = 0,75
lines = 10**6
trace = []
page_maximum_nunber = 250000

def generate_pages_numbers(quantity, maximum):
	pages = []
	
	for i in range(quantity):
		aux = random.randint(0, maximum)
		
		pages.append(aux)
	
	return pages


def generate_mode():
	aux = random.randint(0,1)
	if(aux == 0):
		return "w"
	else:
		return "r"


for i in range(lines/window):
	pages_numbers = generate_pages_numbers(5, page_maximum_nunber)
	
	for j in range(window):
		aux = random.randint(0, len(pages_numbers))
		
		mode =  generate_mode()
		
		trace.append((pages_numbers[aux - 1], mode))
		
def put_random_int_trace():
	aux = len(trace) * proportion
	inteiro = int(aux)
	
	for i in range(inteiro):
		index  = random.int(0, len(trace) - 1)
		page =  random.int(0, page_maximum_nunber)
		
		trace[index] = page
		 
			
		
for j in range(len(trace)):
	print trace[j][0], trace[j][1] 
