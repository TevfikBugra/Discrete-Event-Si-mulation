# Discrete-Event-Simulation 
This repository includes an assignment from the IE306 Systems Simulation course.  
  
IE 306 – Fall 2022  
1- There are two parallel servers and a single waiting line. Customers are eventually serviced by the 
first free server. If a customer arrives while both servers are idle, she/he then prefers 
server 1 (who happens to work faster). The interarrival times of customers are known 
to be distributed Uniform(6,16) minutes. The service time for the first server is 
Uniform(14,21) minutes, and for the second server it is given as:
Service time (minutes) : 8 12 22 33
Probability : .18 .30 .30 .22
Prepare a formal “event-scheduling” hand-simulation table and hand-simulate the 
system for 35 minutes only. Assume that the first server is busy and the second one is 
idle initially. Use the following sequence of random numbers as necessary:
0.380 0.496 0.832 0.391 0.020 0.480 0.975 0.759 0.905 0.593 0.560 …
(When an arrival and a departure must be simultaneously scheduled, use the 
convention of scheduling the arrival first).  
  
2- Using event-scheduling algorithm, write a computer program to simulate the 
system described above. Organize your program using typical simulation variables 
and structures discussed in class and in your texts.
a) First run your simulation for 35 minutes only and by inputting and using the 
random numbers given in Question 1, as needed. Have your program print out the 
important variables line by line, producing a brief table that allows you to make a 
verification of your program, by comparing it against your results obtained in Q.1.
b) Next run for 7000 minutes, and 4 times with 4 different random seeds and estimate 
the following statistics:
i) Average time spent in the queue
ii) Average number of customers in the system
iii) The average utilization of each server
iv) Probability of a customer not waiting in the queue
Also verify if Little’s law holds (approximately) for your answers above. 
NOTE:
Your program must have some minimum documentation (with comment lines)
