from Furuta import Furuta
import numpy as np

float_formatter = lambda x: "%.3f" % x
np.set_printoptions(formatter={'float_kind':float_formatter})

furuta = Furuta('C:/Users/Samvrit/Desktop/Python/furuta1.ttt',0,0)

print(furuta.input_size)
print(furuta.action_size)
start_time = 0
curr_time = 0
for i in range(1):
	curr_time = furuta.vrep_time
	while (curr_time - start_time) < 100:
		state, reward, _ = furuta.step(0.02)
		print(reward)
		curr_time = furuta.vrep_time
	furuta.reset(0.0,0.0)
	start_time = curr_time
furuta.stop()