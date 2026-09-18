import unittest
from wireproto.pipeline import image_to_layout
from wireproto.e2e import quality_report


class PipelineTest(unittest.TestCase):
    def test_detection_to_graph(self):
        detections = [
            {"id":"hero","type":"section","bbox":[0,0,800,400]},
            {"id":"title","type":"heading","bbox":[40,40,300,80]},
            {"id":"visual","type":"image","bbox":[420,40,320,300]},
        ]
        graph = image_to_layout(detections, 800, 600)
        self.assertEqual(len(graph.nodes), 3)
        title = next(n for n in graph.nodes if n.id == "title")
        self.assertEqual(title.parent, "hero")
        self.assertIn("left-of:visual", title.relations)
        self.assertEqual(quality_report(graph)["nodes"], 3)


if __name__ == "__main__":
    unittest.main()
