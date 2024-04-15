import pybullet as p
import pybullet_data as pd
import creature
import time
import genome as genlib

p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching=0)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)
p.setGravity(0, 0, -10)
p.setRealTimeSimulation(1)

c = creature.Creature(gene_count=3)
dna = genlib.Genome.from_csv('3_elite.csv')
c.set_dna(dna)

with open('test.urdf', 'w') as f:
    c.get_expanded_links()
    f.write(c.to_xml())

rob1 = p.loadURDF('test.urdf')
c.update_position([0, 0, 0])

p.resetBasePositionAndOrientation(rob1, [0, 0, 3], [0, 0, 0, 1])


while True:
    for jid in range(p.getNumJoints(rob1)):
        m = c.get_motors()[jid]
        p.setJointMotorControl2(rob1, jid, controlMode=p.VELOCITY_CONTROL, targetVelocity = m.get_output(), force = 5)
        pos, orn = p.getBasePositionAndOrientation(rob1)
        c.update_position(pos)

    time.sleep(0.1)

input("press enter to exit\n")