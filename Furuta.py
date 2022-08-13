import time
import vrep
import numpy as np
import math

class Furuta:
	def __init__(self,vrep_file,initial_angle1,initial_angle2):
		print ('Program started')
		self.sim = vrep
		self.sim.simxFinish(-1) # just in case, close all opened connections
		self.clientID = self.sim.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP
		self.sim.simxLoadScene(self.clientID,vrep_file,0,self.sim.simx_opmode_blocking)
		self.sim.simxSynchronous(self.clientID,True)
		self.file = vrep_file
		self.jointHandles = self.sim.simxGetObjectGroupData(self.clientID,self.sim.sim_object_joint_type,15,self.sim.simx_opmode_blocking)[1]
		self.state = np.zeros(3)
		self.input_size = self.state.size
		self.vrep_time = self.sim.simxGetLastCmdTime(self.clientID)
		self.vrep_time_sec = self.sim.simxGetLastCmdTime(self.clientID)/1000
		# self.action_space = np.arange(-0.4,0.4,0.01)
		self.action_space = np.array([-8,8])
		self.action_size = self.action_space.size
		self.sim.simxSetJointPosition(self.clientID,self.jointHandles[1],initial_angle1,self.sim.simx_opmode_blocking)
		self.sim.simxSetJointPosition(self.clientID,self.jointHandles[2],initial_angle2,self.sim.simx_opmode_blocking)
		self.sim.simxStartSimulation(self.clientID,self.sim.simx_opmode_blocking)
	
	def step(self,u):
		if u == 0:
			sign = 0
		else:
			sign = u/abs(u)
		self.sim.simxSetJointForce(self.clientID,self.jointHandles[0],abs(u),self.sim.simx_opmode_blocking)
		self.sim.simxSetJointTargetVelocity(self.clientID,self.jointHandles[0],sign*100,self.sim.simx_opmode_blocking)
		self.sim.simxSynchronousTrigger(self.clientID)
		
		jointPositions = self.sim.simxGetObjectGroupData(self.clientID,self.sim.sim_object_joint_type,15,self.sim.simx_opmode_blocking)[3]
		# self.state[0] = jointPositions[0]
		self.state[0] = -jointPositions[2]
		#self.state[2] = -jointPositions[4]
		self.state[1] = self.sim.simxGetObjectFloatParameter(self.clientID,self.jointHandles[0],2012,self.sim.simx_opmode_blocking)[1]
		self.state[2] = -self.sim.simxGetObjectFloatParameter(self.clientID,self.jointHandles[1],2012,self.sim.simx_opmode_blocking)[1]
		#self.state[5] = -self.sim.simxGetObjectFloatParameter(self.clientID,self.jointHandles[2],2012,self.sim.simx_opmode_blocking)[1]
		
		# review the reward function
		#reward = -(1.5*(abs(self.state[1]) + abs(self.state[2])) + abs(self.state[2] - self.state[1]))
		# reward = 0.8388e-1 * math.cos(self.state[1]) + 0.2519e-1 * math.cos(self.state[1]) * math.cos(self.state[2]) - 0.2519e-1 * math.sin(self.state[1]) * math.sin(self.state[2])
		# reward = math.exp(abs(self.state[0]))
		reward = 10*math.tan(-2*abs(self.state[0]))
		
		self.vrep_time = self.sim.simxGetLastCmdTime(self.clientID)
		self.vrep_time_sec = self.sim.simxGetLastCmdTime(self.clientID)/1000
		
		done = False
		
		if abs(self.state[0]) >= (math.pi/4):
			done = True
		
		return self.state, reward, done
	
	def reset(self,angle1,angle2):
		returnCode = self.sim.simxStopSimulation(self.clientID,self.sim.simx_opmode_blocking)
		if not returnCode:
			self.sim.simxStopSimulation(self.clientID,self.sim.simx_opmode_blocking)
		self.sim.simxLoadScene(self.clientID,self.file,0,self.sim.simx_opmode_blocking)
		self.sim.simxSynchronous(self.clientID,True)
		self.sim.simxSetJointPosition(self.clientID,self.jointHandles[1],angle1,self.sim.simx_opmode_blocking)
		self.sim.simxSetJointPosition(self.clientID,self.jointHandles[2],angle2,self.sim.simx_opmode_blocking)
		self.sim.simxStartSimulation(self.clientID,self.sim.simx_opmode_blocking)
	
	def stop(self):
		returnCode = self.sim.simxStopSimulation(self.clientID,self.sim.simx_opmode_blocking)
		if not returnCode:
			self.sim.simxStopSimulation(self.clientID,self.sim.simx_opmode_blocking)
		self.sim.simxCloseScene(self.clientID,self.sim.simx_opmode_blocking)