import json
import cv2
import numpy as np

from torch.utils.data import Dataset


class MyDataset(Dataset):
    def __init__(self):
        self.data = []
        with open('datasets/VITON-HD-png-512/test_10/test_pairs_low_10.txt', 'rt') as f:
            for line in f:
                self.data.append(json.loads(line))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]

        source_person = item['source_person']
        source_mask = item['source_mask']
        target_cloth = item['target_cloth']
        prompt = item['prompt']


        source_person = cv2.imread('datasets/VITON-HD-png-512/test_10/' + source_person)
        source_mask = cv2.imread('datasets/VITON-HD-png-512/test_10/' + source_mask)
        target_cloth = cv2.imread('datasets/VITON-HD-png-512/test_10/' + target_cloth)

        # Do not forget that OpenCV read images in BGR order.
        source_person = cv2.cvtColor(source_person, cv2.COLOR_BGR2RGB)
        source_mask = cv2.cvtColor(source_mask, cv2.COLOR_BGR2RGB)
        target_cloth = cv2.cvtColor(target_cloth, cv2.COLOR_BGR2RGB)

        # Normalize source images to [0, 1].
        source_person = source_person.astype(np.float32) / 255.0
        source_mask = source_mask.astype(np.float32) / 255.0

        # Normalize target images to [-1, 1].
        target_cloth = (target_cloth.astype(np.float32) / 127.5) - 1.0
        # hint为condition jpg为target
        return dict(hint=source_person, hint2=source_mask, jpg=target_cloth, txt=prompt)

