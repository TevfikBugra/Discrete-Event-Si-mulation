import random

custdict = {}
for i in range(0,1000):
    custdict[i]=[0,0,0,0,0,0,0,0]
# {customer number:[0]=interarrival time, [1]=arrival time, [2]=service beginning time, [3]=service time, 
# [4]=departure time, [5]=server number, [6]=time in the system, [7]= time in the queue]}

current = {"Ls1":0, "Ls2":0, "Lq":0} # {"Ls1": number of customers in server 1, "Ls2": number of customers in server 2, "Lq": number of customers queue
future_event = {"A":0, "D1":999, "D2":999} # {"A": the nearest arrival, "D1": the nearest departure from server 1, "D2": the nearest departure from server 2}
future_event_id = {"A":0, "D1":0, "D2":0} # {keys of the nearest events}
queue_dict = {} # order and the arrival times of the customers that are in the queue

def arrival(i):   
    if current["Ls1"] == 0:                                         #if server 1 is idle         
        custdict[i+1][0] = random.random()*10+6                     #decide the next interarrival time
        custdict[i+1][1] = custdict[i][1] + custdict[i+1][0]        #schedule the next arrival time
        future_event["A"] = custdict[i+1][1]                        #mark it as next arrival time
        future_event_id["A"] = i+1                                  #mark also its order
        custdict[i][3] = random.random()*7+14                       #assign a service time for server 1
        custdict[i][2] = custdict[i][1]                             #mark the service beginning time as the arrival time (since server 1 is idle)
        custdict[i][4] = custdict[i][2] + custdict[i][3]            #mark the departure time
        future_event["D1"] = custdict[i][4]                         #mark it as the next departure time for server 1
        future_event_id["D1"] = i                                   #mark also its order
        current["Ls1"] = 1                                          #since the server is not idle anymore, increase the current customer in server1 to 1
        custdict[i][5] = 1                                          #mark the serviced server as 1
        custdict[i][6] = custdict[i][4] - custdict[i][1]            #calculate time spent in the system
        custdict[i][7] = custdict[i][2] - custdict[i][1]            #calculate time spent in the queue
  
    elif current["Ls2"] == 0:                                       #if server 2 is idle 
        custdict[i+1][0] = random.random()*10+6                     #decide the next interarrival time
        custdict[i+1][1] = custdict[i][1] + custdict[i+1][0]        #schedule the next arrival time    
        future_event["A"] = custdict[i+1][1]                        #mark it as next arrival time
        future_event_id["A"] = i+1                                  #mark also its order
        a = random.random()                                         #find the service time for server 1
        if a <= 0.18:
            custdict[i][3] = 8
        elif a <= 0.48:
            custdict[i][3] = 12
        elif a <= 0.78:
            custdict[i][3] = 22
        else:
            custdict[i][3] = 33
        custdict[i][2] = custdict[i][1]                             #mark the service beginning time as the arrival time (since server 2 is idle) 
        custdict[i][4] = custdict[i][2] + custdict[i][3]            #mark the departure time 
        future_event["D2"] = custdict[i][4]                         #mark it as the next departure time for server 2
        future_event_id["D2"] = i                                   #mark also its order
        current["Ls2"] = 1                                          #since the server is not idle anymore, increase the current customer in server2 to 1
        custdict[i][5] = 2                                          #mark the serviced server as 2
        custdict[i][6] = custdict[i][4] - custdict[i][1]            #calculate time spent in the system
        custdict[i][7] = custdict[i][2] - custdict[i][1]            #calculate time spent in the queue
    
    else:                                                           #if all the servers are full
        current["Lq"] += 1                                          #increase the current number of customers in the queue by 1
        custdict[i+1][0] = random.random()*10+6                     #decide the next interarrival time
        custdict[i+1][1] = custdict[i][1] + custdict[i+1][0]        #schedule the next arrival time
        future_event["A"] = custdict[i+1][1]                        #mark it as next arrival time
        future_event_id["A"] = i+1                                  #mark also its order
        queue_dict[i] = custdict[i][1]                              #add the order and arrival time of the customer into the queue_dict


def departure(i):
    if current["Lq"] == 0:                                          #if there is no one in the queue
        if custdict[i][5] == 1:                                     #if arrival is in server 1
            current["Ls1"] = 0                                      #set server 1 as idle
            future_event["D1"] = 90000000                           #set the future departure time of server 1 to a sufficiently big number 

        elif custdict[i][5] == 2:                                   #if arrival is in server 2
            current["Ls2"] = 0                                      #set server 2 as idle
            future_event["D2"] = 90000000                           #set the future departure time of server 2 to a sufficiently big number 

    elif current["Lq"] > 0:                                                 #if there are customer(s) in the queue
        current["Lq"] -= 1                                                  #decrease queue length by 1
        index = list(queue_dict.keys())[0]                                  #get the key of the first element of the queue_dict
        del queue_dict[index]                                               #then discard that customer from the queue_dict
        if future_event["D1"] < future_event["D2"]:                         #if the departure of server 1 is closer
            custdict[index][2] = future_event["D1"]                         #the service beginning time of the immeadiate waiting customer is the departure time of the previous customer
            custdict[index][3] = random.random()*7+14                       #assign a service time for server 1
            custdict[index][4] = custdict[index][2] + custdict[index][3]    #mark the departure time
            future_event["D1"] = custdict[index][4]                         #mark it as the next departure time for server 1
            future_event_id["D1"] = index                                   #mark also its order
            custdict[index][5] = 1                                          #mark the serviced server as 1
            custdict[index][6] = custdict[index][4] - custdict[index][1]    #calculate time spent in the system
            custdict[index][7] = custdict[index][2] - custdict[index][1]    #calculate time spent in the queue

        elif future_event["D1"] >= future_event["D2"]:                      #if the departure of server 2 is closer
            custdict[index][2] = future_event["D2"]                         #the service beginning time of the immeadiate waiting customer is the departure time of the previous customer
            a = random.random()                                             #assign a service time for server 2
            if a <= 0.18:
                custdict[index][3] = 8
            elif a <= 0.48:
                custdict[index][3] = 12
            elif a <= 0.78:
                custdict[index][3] = 22
            else:
                custdict[index][3] = 33
            custdict[index][4] = custdict[index][2] + custdict[index][3]    #mark the departure time
            future_event["D2"] = custdict[index][4]                         #mark it as the next departure time for server 2
            future_event_id["D2"] = index                                   #mark also its order
            custdict[index][5] = 2                                          #mark the serviced server as 1
            custdict[index][6] = custdict[index][4] - custdict[index][1]    #calculate time spent in the system
            custdict[index][7] = custdict[index][2] - custdict[index][1]    #calculate time spent in the queue
        
n=0
while n<999:
    if future_event["A"] < future_event["D1"] and future_event["A"] < future_event["D2"]:       #if the nearest event is an arrival
        arrival(future_event_id["A"])
        n +=1
         
    elif future_event["D1"] < future_event["A"] and future_event["D1"] < future_event["D2"]:    #if the nearest event is a departure from server 1
        departure(future_event_id["D1"])
        
    elif future_event["D2"] < future_event["A"] and future_event["D2"] < future_event["D1"]:    #if the nearest event is a departure from server 2
        departure(future_event_id["D2"]) 
         
print(custdict)

"""
#Average time spent in the queue

for y in range(0,1000):
    if custdict[y][1] > 7000:
        del custdict[y]

sum_of_queue_times = 0
for m in range(0,len(custdict)):
    sum_of_queue_times += custdict[m][7]

print(sum_of_queue_times/len(custdict))
"""
'''
#Average number of customers in the system

for y in range(0,1000):
    if custdict[y][1] > 7000:
        del custdict[y]

sum_of_system_times = 0
for m in range(0,len(custdict)):
    sum_of_system_times += custdict[m][6]

print(sum_of_system_times/7000)
'''
'''
#The average utilization of each server

for y in range(0,1000):
    if custdict[y][1] > 7000:
        del custdict[y]

sum_of_server1_times = 0
for m in range(0,len(custdict)):
    if custdict[m][5] == 1:
        sum_of_server1_times += custdict[m][3]

print(sum_of_server1_times/7000)

sum_of_server2_times = 0
for m in range(0,len(custdict)):
    if custdict[m][5] == 2:
        sum_of_server2_times += custdict[m][3]

print(sum_of_server2_times/7000)
'''
'''
#Probability of a customer not waiting in the queue

for y in range(0,1000):
    if custdict[y][1] > 7000:
        del custdict[y]

count_of_queue = 0
for m in range(0,len(custdict)):
    if custdict[m][7] == 0:
        count_of_queue +=1

print(count_of_queue/len(custdict))
'''
'''
#Average time spent in the system

for y in range(0,1000):
    if custdict[y][1] > 7000:
        del custdict[y]

sum_of_system_times = 0
for m in range(0,len(custdict)):
    sum_of_system_times += custdict[m][6]

print( sum_of_system_times/len(custdict))
'''