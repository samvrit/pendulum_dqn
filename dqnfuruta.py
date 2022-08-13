# reference: https://keon.io/deep-q-learning/
import random
import gym
import numpy as np
from DQNAgent import DQNAgent
from Furuta import Furuta
import xlsxwriter

EPISODES = 2000

float_formatter = lambda x: "%.3f" % x
np.set_printoptions(formatter={'float_kind':float_formatter})

if __name__ == "__main__":
	furuta = Furuta('C:/Users/Samvrit/Desktop/Python/furuta2.ttt',0,0)
	agent = DQNAgent(furuta.input_size, furuta.action_size)
	#agent.load("./save/furuta-dqn.h5")
	done = False
	batch_size = 100
	workbook = xlsxwriter.Workbook('dqnfuruta.xlsx')
	worksheet = workbook.add_worksheet('Single Furuta')
	worksheet.write_string(0, 0, 'Episode')
	worksheet.write_string(0, 1, 'Timesteps')
	
	for e in range(EPISODES):
		print('New episode')
		state = np.zeros(3)
		state = np.reshape(state,[1,3])
		for time in range(450):
			action_index = agent.act(state)
			action = furuta.action_space[action_index]
			next_state, reward, done = furuta.step(action)
			reward = reward + time if not done else -1e6
			next_state = np.reshape(next_state, [1, furuta.input_size])
			agent.remember(state, action_index, reward, next_state, done)
			state = next_state
			print("reward: {:.2} | action index: {} | action: {}".format(reward,action_index,action))
			if done:
				break
		print("episode: {}/{}, score: {}, e: {:.2}".format(e, EPISODES, time, agent.epsilon))
		worksheet.write_number(e+1, 0, e)
		worksheet.write_number(e+1, 1, time)
		
		if len(agent.memory) > min(time,batch_size):
			agent.replay(min(time,batch_size))
		if e % 10 == 0:
			agent.save("./save/furuta-dqn.h5")
		
		furuta.reset(random.uniform(-0.02,0.02) , 0.0)
		
	workbook.close()
	furuta.stop()