import unittest
import simulation as s
import creature as cr
import os
import population

class TestSim(unittest.TestCase):

    def testSimExists(self):
        sim = s.Simulation()
        self.assertIsNotNone(sim)

    def testSimId(self):
        sim = s.Simulation()
        self.assertIsNotNone(sim.physicsClientId)

    def testRun(self):
        sim = s.Simulation()
        self.assertIsNotNone(sim.run_creature)

    def testRun(self):
        sim = s.Simulation()
        c = cr.Creature(gene_count=3)
        sim.run_creature(c)
        self.assertTrue(os.path.exists('temp.urdf'))

    def testRun(self):
        sim = s.Simulation()
        c = cr.Creature(gene_count=3)
        sim.run_creature(c)
        self.assertNotEqual(c.start_position, c.last_position)

    def testDist(self):
        sim = s.Simulation()
        c = cr.Creature(gene_count=3)
        sim.run_creature(c)
        dist = c.get_distance_travelled()
        print(dist)
        self.assertGreater(dist, 0)

    def testPop(self):
        pop = population.Population(pop_size=10, gene_count=3)
        sim = s.Simulation()
        for c in pop.creatures:
            sim.run_creature(c)

        dists = [c.get_distance_travelled() for c in pop.creatures]
        print(dists)
        self.assertIsNotNone(dists)

    def testProc(self):
        pop = population.Population(pop_size=10, gene_count=3)
        tsim = s.ThreadedSim(pool_size=4)
        tsim.eval_population(pop, 2400)


unittest.main()