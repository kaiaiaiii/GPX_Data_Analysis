#######################################
### file to analyse my cadence data ###
#######################################
import matplotlib.pyplot as plt
datavector, time, cadence = [], [], []

def cadence_from_data(filename):
    with open(filename) as file:
        for line in file:
            datavector.append(line)
        pps = int(datavector[0]) #input frequency in pulses per second
        datavector.pop(0)

    counter = 0
    elapsed_time = 0 
    for number in map(int, datavector[0]):
        if number == 0:
            counter += 1
            elapsed_time += 1
        elif number == 1:
            elapsed_time += 1
            cadence.append(pps*(counter+1))
            time.append(pps*elapsed_time)
            counter = 0
    return cadence, time
        

plt.figure(figsize=(8, 5))
plt.plot(time, cadence, label="Test")
plt.xlabel("time")
plt.ylabel("cadence")
plt.title("Name")
plt.legend()
plt.savefig("cadenceplot")
plt.show()
plt.close()
