import unittest
import population as p

class testPop(unittest.TestCase):

    def testPopExists(self):
        pop = p.Population(pop_size = 10, gene_count=4)
        self.assertIsNotNone(pop)

    def testPopHasIndis(self):
        pop = p.Population(pop_size=10, gene_count=4)
        self.assertEqual(len(pop.creatures), 10)

    def testFitmap(self):
        fits = [2.5, 1.2, 3.4]
        want = [2.5, 3.7, 7.1]
        fitmap = p.Population.get_fitness_map(fits)
        self.assertEqual(fitmap, want)

    def testSelPar(self):
        fits = [2.5, 1.2, 3.4]
        fitmap = p.Population.get_fitness_map(fits)
        pid = p.Population.select_parent(fitmap)
        self.assertLess(pid, 3)

unittest.main()