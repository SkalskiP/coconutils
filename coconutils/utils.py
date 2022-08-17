import os
import json
import random
import shutil

from coconutils.dataclasses import COCO, COCOAnnotation, COCOImage
from typing import List, Union


def load_json_file(json_file: str) -> dict:
    with open(json_file, 'r') as f:
        return json.load(f)


def save_json_file(json_file: str, data: dict) -> None:
    with open(json_file, 'w') as f:
        json.dump(data, f)


def extract_image_annotations(images: List[COCOImage], annotations: List[COCOAnnotation]) -> List[COCOAnnotation]:
    image_ids = [image.id for image in images]
    return [
        annotation 
        for annotation 
        in annotations 
        if annotation.image_id in image_ids
    ]


def train_test_split_coco(source_coco: COCO, train_ratio: float, shuffle: bool = True) -> Union[COCO, COCO]:
    source_images = sorted(source_coco.images, key=lambda k: random.random()) if shuffle else source_coco.images
    train_size = int(len(source_images) * train_ratio)
    train_images = source_images[:train_size]
    test_images = source_images[train_size:]
    train_annotations = extract_image_annotations(images=train_images, annotations=source_coco.annotations)
    test_annotations = extract_image_annotations(images=test_images, annotations=source_coco.annotations)
    train_coco = COCO(info=source_coco.info, images=train_images, annotations=train_annotations, categories=source_coco.categories)
    test_coco = COCO(info=source_coco.info, images=test_images, annotations=test_annotations, categories=source_coco.categories)
    return train_coco, test_coco


def copy_image_files(source_image_root: str, target_image_root: str, images: List[COCOImage]) -> None:
    os.makedirs(target_image_root, exist_ok=True)
    for image in images:
        sorce_file = os.path.join(source_image_root, image.file_name)
        target_file = os.path.join(target_image_root, image.file_name)
        shutil.copyfile(sorce_file, target_file)


def train_test_split(
    image_root: str, 
    json_file: str, 
    target_root: str, 
    train_ratio: float = 0.8, 
    shuffle: bool = True
) -> None:
    source_coco = COCO.from_dict(load_json_file(json_file=json_file))
    train_coco, test_coco = train_test_split_coco(
        source_coco=source_coco, 
        train_ratio=train_ratio, 
        shuffle=shuffle
    )
    os.makedirs(target_root, exist_ok=True)

    train_target_images_root = os.path.join(target_root, 'train', 'images')
    test_target_images_root = os.path.join(target_root, 'test', 'images')
    train_target_json_file = os.path.join(target_root, 'train', 'labels.json')
    test_target_json_file = os.path.join(target_root, 'test', 'labels.json')

    copy_image_files(
        source_image_root=image_root, 
        target_image_root=train_target_images_root, 
        images=train_coco.images
    )
    copy_image_files(
        source_image_root=image_root, 
        target_image_root=test_target_images_root, 
        images=test_coco.images
    )

    save_json_file(train_target_json_file, train_coco.to_dict())
    save_json_file(test_target_json_file, test_coco.to_dict())
    

if __name__ == '__main__':
    train_test_split(
        image_root="/Users/piotrskalski/Documents/private/coconutils/data/pitch-segmentation-dataset-20220817/images", 
        json_file="/Users/piotrskalski/Documents/private/coconutils/data/pitch-segmentation-dataset-20220817/labels.json", 
        target_root="/Users/piotrskalski/Documents/private/coconutils/data/"
    )