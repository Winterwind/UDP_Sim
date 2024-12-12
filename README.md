# UDP_Sim
Simulations of the Stop-and-Wait &amp; Go-Back-N UDP protocols as a part of my Computer Networks class' first project. Both parts use the [UDP_Constants.py](UDP_Constants.py) file to access shared things, such as the ```simulate_error``` function. You can also change the probability of bit errors and packet losses from this file, and those changes will reflect when you actually run the simulation. This repo also includes [the report](CSC424_Project_Part_1.pdf) I had to submit along with [the LaTeX file](main.tex) that produced it.

## Stop-and-Wait
To run this simulation, first run the [Stop_n'_Wait_Server.py](Stop_n'_Wait_Server.py) file in one terminal window and then run the [Stop_n'_Wait_Client.py](Stop_n'_Wait_Client.py) in another; the results will then print in that window.

## Go-Back-N
To run this simulation, first run the [Go_Back_N_Server.py](Go_Back_N_Server.py) file in one terminal window and then run the [Go_Back_N_Client.py](Go_Back_N_Client.py) in another; the results will then print in that window.
