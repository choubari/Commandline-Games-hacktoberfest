initiative_list = []

print ("D&D initiative tracker")
print ("Usage: [player name] [roll]")
print ('Type "stop" when you are done!')

#Adding initiative
while True:

	line = input().split()

	if (line[0]=='stop'):
		break 

	try:
		player_name = str(line[0])
		player_initiative = int(line[1])
		initiative_list.append([player_name,player_initiative])
		
	except:
		print ('Make sure to enter a number after the name!')
		

#Sort
initiative_list.sort(key=lambda initiative: initiative[1], reverse=True)

print ("The combat order will be the following:")

#Print list
for i in range(len(initiative_list)):

	if i==len(initiative_list)-1:
		print (initiative_list[i][0])
	else:
		print (initiative_list[i][0] + " -> ", end='')
