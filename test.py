# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 23:25:39 2017

@author: Samvrit
"""
import time
import vrep
import numpy as np

float_formatter = lambda x: "%.3f" % x
np.set_printoptions(formatter={'float_kind':float_formatter})
clamp = lambda n, minn, maxn: max(min(maxn, n), minn)

print ('Program started')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP
vrep.simxLoadScene(clientID,'C:/Users/Samvrit/Desktop/Python/furuta1.ttt',0,vrep.simx_opmode_blocking)
vrep.simxSynchronous(clientID,True)
jointHandles = vrep.simxGetObjectGroupData(clientID,vrep.sim_object_joint_type,15,vrep.simx_opmode_blocking)[1]
state = np.zeros((6))
K = np.array([1.00, -46.47, -219.20, 1.16, -14.69, -18.35])
vrep_time = vrep.simxGetLastCmdTime(clientID)/1000
u = 0
vrep.simxSetJointPosition(clientID,jointHandles[1],-0.05,vrep.simx_opmode_blocking)
vrep.simxStartSimulation(clientID,vrep.simx_opmode_blocking)
while vrep_time < 3:
	vrep.simxSynchronousTrigger(clientID)
	jointPositions = vrep.simxGetObjectGroupData(clientID,vrep.sim_object_joint_type,15,vrep.simx_opmode_blocking)[3]
	state[0] = jointPositions[0]
	state[1] = -jointPositions[2]
	state[2] = -jointPositions[4]
	state[3] = vrep.simxGetObjectFloatParameter(clientID,jointHandles[0],2012,vrep.simx_opmode_blocking)[1]
	state[4] = -vrep.simxGetObjectFloatParameter(clientID,jointHandles[1],2012,vrep.simx_opmode_blocking)[1]
	state[5] = -vrep.simxGetObjectFloatParameter(clientID,jointHandles[2],2012,vrep.simx_opmode_blocking)[1]
	#print(state)
	u = np.dot(K,state)
	if abs(state[1]) > 1.5708:
		break
	vrep.simxSetJointForce(clientID,jointHandles[0],abs(u),vrep.simx_opmode_blocking)
	vrep.simxSetJointTargetVelocity(clientID,jointHandles[0],(u/abs(u))*100,vrep.simx_opmode_blocking)
	print(vrep.simxGetJointForce(clientID,jointHandles[0],vrep.simx_opmode_blocking))
	vrep_time = vrep.simxGetLastCmdTime(clientID)/1000
vrep.simxStopSimulation(clientID,vrep.simx_opmode_blocking)
vrep.simxFinish(clientID)