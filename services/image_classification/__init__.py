import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import numpy as np
import json
import io


def image_classification(image_encoded):
    imStream = io.BytesIO(image_encoded)
    img = Image.open(imStream)

    model = models.resnet18(pretrained=True)

    model.eval()
    img_tensor = transforms.ToTensor()(img).unsqueeze_(0)
    outputs = model(img_tensor)
    _, predicted = torch.max(outputs.data, 1)

    with open('./services/image_classification/imagenet-labels.json') as f:
        labels = json.load(f)
    result = labels[np.array(predicted)[0]]

    return result