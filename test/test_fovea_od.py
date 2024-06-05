import unittest
import os
import numpy as np
import torch
from PIL import Image
from torchvision.transforms import Compose, ToTensor, Resize, CenterCrop
from fundus_fovea_od_localization import ODFoveaLoader, ODFoveaModel, load_fovea_od_model, DEFAULT_CONFIG

DIR = os.path.join(os.path.dirname(__file__))
fundus1_path = os.path.join(DIR, '..', 'fundus1.jpg')
DEVICE = 'cpu'

class TestFoveaODModel(unittest.TestCase):
    def setUp(self):
        self.image = Image.open(fundus1_path)
        transform = Compose([Resize(350, antialias=True), CenterCrop(350), ToTensor()])
        self.image_batch = torch.stack([transform(self.image) for _ in range(2)])
        self.device = DEVICE

    def test_load_fovea_od_model(self):
        model, checkpoint_path = load_fovea_od_model("default", device=self.device, return_test_dataloader=False)
        self.assertIsInstance(model, ODFoveaModel)

        fovea_x, fovea_y, od_x, od_y = model.predict(self.image)
        self.assertIsInstance(float(fovea_x), float)
        self.assertIsInstance(float(fovea_y), float)
        self.assertIsInstance(float(od_x), float)
        self.assertIsInstance(float(od_y), float)

        labels = model.predict(self.image_batch)
        self.assertIsInstance(labels, list)
        self.assertEqual(len(labels), 2)
        self.assertIsInstance(labels[0], np.ndarray)
        self.assertEqual(len(labels[0]), 4)
        self.assertIsInstance(float(labels[0][0]), float)

        self.assertEqual(self.device, str(model.device))
        
    def test_load_with_dataloader(self):
        model, checkpoint_path, test_dataloader = load_fovea_od_model("default", device=self.device, return_test_dataloader=True)
        self.assertIsInstance(test_dataloader, ODFoveaLoader)

if __name__ == '__main__':
    unittest.main()