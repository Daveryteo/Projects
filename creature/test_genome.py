import unittest
import genome as g
import numpy as np
from xml.dom.minidom import getDOMImplementation

class Genometest(unittest.TestCase):

    def testClassExist(self):
        self.assertIsNotNone(g.Genome)

    def testRandomGene(self):
        self.assertIsNotNone(g.Genome.get_random_gene)

    def testRandomGeneNotNone(self):
        self.assertIsNotNone(g.Genome.get_random_gene(5))

    def testRandomGeneHasValues(self):
        gene = g.Genome.get_random_gene(5)
        self.assertIsNotNone(gene[0])

    def testRandomGeneLength(self):
        gene = g.Genome.get_random_gene(20)
        self.assertEqual(len(gene), 20)

    def testRandomGeneIsNumpyArrays(self):
        gene = g.Genome.get_random_gene(20)
        self.assertEqual(type(gene), np.ndarray)

    def testRandomGenomeExists(self):
        genome = g.Genome.get_random_genome(20, 5)
        self.assertIsNotNone(genome)

    def testGeneSpecExists(self):
        spec = g.Genome.get_gene_spec()
        self.assertIsNotNone(spec)

    def testGeneSpecHasLinkLength(self):
        spec = g.Genome.get_gene_spec()
        self.assertIsNotNone(spec['link-length'])

    def testGeneSpecHasLinkLength(self):
        spec = g.Genome.get_gene_spec()
        self.assertIsNotNone(spec['link-length']["ind"])

    def testGeneSpecScale(self):
        spec = g.Genome.get_gene_spec()
        gene = g.Genome.get_random_gene(20)
        self.assertGreater(gene[spec['link-length']["ind"]], 0)

    def testFlatLinks(self):
        links = [
            g.URDFLink(name="A", parent_name=None, recur=1),
            g.URDFLink(name="B", parent_name="A", recur=1),
            g.URDFLink(name="C", parent_name="B", recur=2),
            g.URDFLink(name="D", parent_name="C", recur=1)
        ]
        self.assertIsNotNone(links)

    def testExpandLinks(self):
        links = [
            g.URDFLink(name="A", parent_name=None, recur=1),
            g.URDFLink(name="B", parent_name="A", recur=1),
            g.URDFLink(name="C", parent_name="B", recur=2),
            g.URDFLink(name="D", parent_name="C", recur=1)
        ]
        exp_links = [links[0]]
        g.Genome.expandLinks(links[0], links[0].name, links, exp_links)
        self.assertEqual(len(exp_links), 6)

    def testGenetoGeneDict(self):
        spec = g.Genome.get_gene_spec()
        gene = g.Genome.get_random_gene(len(spec))
        gene_dict = g.Genome.get_gene_dict(gene, spec)
        self.assertIn("link-length", gene_dict)

    def testGenomeToDict(self):
        spec = g.Genome.get_gene_spec()
        dna = g.Genome.get_random_genome(len(spec), 3)
        genome_dicts = g.Genome.get_genome_dicts(dna, spec)
        self.assertEqual(len(genome_dicts), 3)

    def testGetLinks(self):
        spec = g.Genome.get_gene_spec()
        dna = g.Genome.get_random_genome(len(spec), 3)
        gdicts = g.Genome.get_genome_dicts(dna, spec)
        links = g.Genome.genome_to_links(gdicts)
        self.assertEqual(len(links), 3)

    def testLinkToXML(self):
        link = g.URDFLink(name="A", parent_name=None, recur=1)
        domimpl = getDOMImplementation()
        adom = domimpl.createDocument(None, "robot", None)
        xml_str = link.to_link_xml(adom)
        print(xml_str)
        self.assertIsNotNone(xml_str)

    def testXO(self):
        g1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        g2 = np.array([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
        g3 = g.Genome.crossover(g1, g2)
        self.assertEqual(len(g3), len(g1))

    def test_point(self):
        g1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        g.Genome.point_mutate(g1, rate=0.5, amount=0.25)

    def test_shrink(self):
        g1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        g2 = g.Genome.shrink_mutate(g1, rate=0.5)
        self.assertNotEqual(len(g1), len(g2))

    def test_Grow(self):
        g1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        g2 = g.Genome.grow_mutate(g1, rate=0.5)
        self.assertGreater(len(g2), len(g1))

    def test_to_csv(self):
        g1 = [[1, 2, 3]]
        g.Genome.to_csv(g1, 'test.csv')
        self.assertTrue(os.path.exists('test.csv'))



unittest.main()