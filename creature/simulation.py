import pybullet as p
from multiprocessing import Pool

class Simulation:

    def __init__(self, sim_id=0):
        self.physicsClientId = p.connect(p.DIRECT)
        self.sim_id = sim_id


    def run_creature(self, c, iterations=10):
        pid = self.physicsClientId
        p.resetSimulation(physicsClientId=pid)
        p.setGravity(0, 0, -10, physicsClientId=pid)
        p.setPhysicsEngineParameter(enableFileCaching=0, physicsClientId=pid)
        plane_shape = p.createCollisionShape(p.GEOM_PLANE, physicsClientId=pid)
        floor = p.createMultiBody(plane_shape, plane_shape, physicsClientId=pid)

        xml_file = 'temp' + str(self.sim_id) + '.urdf'
        xml_str = c.to_xml()

        with open(xml_file, 'w') as f:
            f.write(xml_str)

        cid = p.loadURDF(xml_file, physicsClientId=pid)

        p.resetBasePositionAndOrientation(cid, [0, 0, 3], [0, 0, 0, 1], physicsClientId=pid)

        for step in range(iterations):
            p.stepSimulation(physicsClientId=pid)
            if step % 24 == 0:
                self.update_motors(cid=cid, c=c)

            pos, orn = p.getBasePositionAndOrientation(cid, physicsClientId=pid)
            c.update_position(pos)
            # if step > 0:
            #     print(c.last_position[2])

    def update_motors(self, cid, c):
        pid = self.physicsClientId
        for jid in range(p.getNumJoints(cid, physicsClientId=pid)):
            m = c.get_motors()[jid]
            p.setJointMotorControl2(cid, jid,
                                    controlMode=p.VELOCITY_CONTROL,
                                    targetVelocity=m.get_output(),
                                    physicsClientId=pid)


class ThreadedSim:
    def __init__(self, pool_size):
        self.sims = [Simulation(i) for i in range(pool_size)]

    @staticmethod
    def static_run_creature(sim, c, iterations):
        sim.run_creature(c, iterations)
        return c

    def eval_population(self, pop, iterations):
        pool_args = []
        start_ind = 0
        pool_size = len(self.sims)
        while start_ind < len(pop.creatures):
            this_pool_args = []
            for i in range(start_ind, start_ind + pool_size):
                # check that this is the end and break
                if i == len(pop.creatures):
                    break

                sim_ind = i % len(self.sims)
                # print("eval_pop: c ind ", start_ind, "sim_ind", sim_ind)

                this_pool_args.append([self.sims, pop.creatures[i], iterations])

                pool_args.append(this_pool_args)

                start_ind = start_ind + pool_size

            new_creatures = []
            for pool_argset in pool_args:
                with Pool(pool_size) as p:
                    creatures = p.starmap(ThreadedSim.static_run_creature, pool_argset)
                    new_creatures.extend(creatures)

            # for c in new_creatures:
            #     print(c.get_distance_travelled())
            pop.creatures = new_creatures
