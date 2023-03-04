custdict = {}
for i in range(0,5):
    custdict[i]=[0,0,0,0,0,0,0,0]
# {customer number:[0]=interarrival time, [1]=arrival time, [2]=service beginning time, [3]=service time, 
# [4]=departure time, [5]=server number, [6]=time in the system, [7]= time in the queue]}

rand_numb_list=[0.380,0.496,0.832,0.391,0.020,0.480,0.975,0.759,0.905,0.593,0.560]

current = {"Ls1":0, "Ls2":0, "Lq":0}
future_event = {"A":0, "D1":999, "D2":999}
future_event_id = {"A":0, "D1":0, "D2":0}
queue_dict = {}

def arrival(i):
    if current["Ls1"] == 0:
        custdict[i+1][0] = rand_numb_list[0]*10+6
        rand_numb_list.remove(rand_numb_list[0])
        custdict[i+1][1] = custdict[i][1] + custdict[i+1][0]
        future_event["A"] = custdict[i+1][1]
        future_event_id["A"] = i+1
        custdict[i][3] = rand_numb_list[0]*7+14
        rand_numb_list.remove(rand_numb_list[0])
        custdict[i][2] = custdict[i][1]
        custdict[i][4] = custdict[i][2] + custdict[i][3]
        future_event["D1"] = custdict[i][4]
        future_event_id["D1"] = i
        current["Ls1"] = 1
        custdict[i][5] = 1
        custdict[i][6] = custdict[i][4] - custdict[i][1]
        custdict[i][7] = custdict[i][2] - custdict[i][1]
  
    elif current["Ls2"] == 0:
        custdict[i+1][0] = rand_numb_list[0]*10+6
        rand_numb_list.remove(rand_numb_list[0])
        custdict[i+1][1] = custdict[i][1] + custdict[i+1][0]
        future_event["A"] = custdict[i+1][1]
        future_event_id["A"] = i+1
        a = rand_numb_list[0]
        rand_numb_list.remove(rand_numb_list[0])
        if a <= 0.18:
            custdict[i][3] = 8
        elif a <= 0.48:
            custdict[i][3] = 12
        elif a <= 0.78:
            custdict[i][3] = 22
        else:
            custdict[i][3] = 33
        custdict[i][2] = custdict[i][1]
        custdict[i][4] = custdict[i][2] + custdict[i][3]
        future_event["D2"] = custdict[i][4]
        future_event_id["D2"] = i
        current["Ls2"] = 1
        custdict[i][5] = 2
        custdict[i][6] = custdict[i][4] - custdict[i][1]
        custdict[i][7] = custdict[i][2] - custdict[i][1]
    
    else:
        current["Lq"] += 1
        custdict[i+1][0] = rand_numb_list[0]*10+6
        rand_numb_list.remove(rand_numb_list[0])
        custdict[i+1][1] = custdict[i][1] + custdict[i+1][0]
        future_event["A"] = custdict[i+1][1]
        future_event_id["A"] = i+1
        queue_dict[i] = custdict[i][1]

def departure(i):
    if current["Lq"] == 0:
        if custdict[i][5] == 1:
            current["Ls1"] = 0
            future_event["D1"] = 90000000

        elif custdict[i][5] == 2:
            current["Ls2"] = 0
            future_event["D2"] = 90000000

    elif current["Lq"] > 0:
        current["Lq"] -= 1
        index = list(queue_dict.keys())[0]  #key of the first element of the queue_dict
        del queue_dict[index]
        if future_event["D1"] < future_event["D2"]:
            custdict[index][2] = future_event["D1"]
            custdict[index][3] = rand_numb_list[0]*7+14
            rand_numb_list.remove(rand_numb_list[0])
            custdict[index][4] = custdict[index][2] + custdict[index][3]
            future_event["D1"] = custdict[index][4]
            future_event_id["D1"] = index
            custdict[index][5] = 1
            custdict[index][6] = custdict[index][4] - custdict[index][1]
            custdict[index][7] = custdict[index][2] - custdict[index][1]

        elif future_event["D1"] >= future_event["D2"]:
            custdict[index][2] = future_event["D2"]
            a = rand_numb_list[0]
            rand_numb_list.remove(rand_numb_list[0])
            if a <= 0.18:
                custdict[index][3] = 8
            elif a <= 0.48:
                custdict[index][3] = 12
            elif a <= 0.78:
                custdict[index][3] = 22
            else:
                custdict[index][3] = 33
            custdict[index][4] = custdict[index][2] + custdict[index][3]
            future_event["D2"] = custdict[index][4]
            future_event_id["D2"] = index
            custdict[index][5] = 2
            custdict[index][6] = custdict[index][4] - custdict[index][1]
            custdict[index][7] = custdict[index][2] - custdict[index][1]
        
n=0
while n<4:
    if future_event["A"] < future_event["D1"] and future_event["A"] < future_event["D2"]:
        arrival(future_event_id["A"])
        n +=1 
        
    elif future_event["D1"] < future_event["A"] and future_event["D1"] < future_event["D2"]:
        departure(future_event_id["D1"])
    
    elif future_event["D2"] < future_event["A"] and future_event["D2"] < future_event["D1"]:
        departure(future_event_id["D2"])         

print(custdict)