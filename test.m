state = zeros(1,6);
vrep = remApi('remoteApi');
vrep.simxFinish(-1);
clientID = vrep.simxStart('127.0.0.1',19997,true,true,5000,5);
[~,jointHandles,~,~,~] = vrep.simxGetObjectGroupData(clientID,vrep.sim_object_joint_type,15,vrep.simx_opmode_blocking);
vrep.simxLoadScene(clientID,'furuta1.ttt',1,vrep.simx_opmode_blocking);
vrep.simxStartSimulation(clientID,vrep.simx_opmode_blocking);
i = 0;
tic;
while toc < 5
    [~,~,~,jointData,~] = vrep.simxGetObjectGroupData(clientID,vrep.sim_object_joint_type,15,vrep.simx_opmode_blocking);
    state(1) = jointData(1);
    state(2) = jointData(3);
    state(3) = jointData(6);
    [~,state(4)] = vrep.simxGetObjectFloatParameter(clientID,jointHandles(1),2012,vrep.simx_opmode_blocking);
    [~,state(5)] = vrep.simxGetObjectFloatParameter(clientID,jointHandles(2),2012,vrep.simx_opmode_blocking);
    [~,state(6)] = vrep.simxGetObjectFloatParameter(clientID,jointHandles(3),2012,vrep.simx_opmode_blocking);
    %disp(state)
    i = i + 1;
end
vrep.simxStopSimulation(clientID,vrep.simx_opmode_blocking);
disp(i)
vrep.simxFinish(clientID);