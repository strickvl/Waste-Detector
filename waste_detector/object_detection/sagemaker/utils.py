import os
import random
import importlib
from typing import Tuple

import icevision.tfms as tfms
import numpy as np
import torch
import json
from icevision.data.data_splitter import RandomSplitter, FixedSplitter
from icevision.data.record_collection import RecordCollection
from icevision.parsers.coco_parser import COCOBBoxParser


def get_object_from_str(s):
    """Get object from formatted string (loadable function or class)

    :param str s: formatted string like sklearn.metrics.r2_score
    :return: function or class
    :raise Exception: when string is not a valid python class
    """
    pm = s.rsplit(".", 1)
    if len(pm) < 2:
        raise Exception("'%s' does not exist as python class" % s)
    mod = importlib.import_module(pm[0])
    return getattr(mod, pm[1])

def fix_all_seeds(seed: int = 4496) -> None:
    """
    Fix the seeds to make the results reproducible.

    Args:
        seed (int): Desired seed number. Default is 4496.
    """
    np.random.seed(seed)
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)

    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True


def get_splits() -> Tuple[RecordCollection]:
    """
    Split the data given the annotations in COCO format.

    Args:
        annotations (str): Annotations filepath.
        img_dir (str): Images filepath.
        config (Config): Config object

    Returns:
        Tuple[RecordCollection]: Tuple containing:
            - (RecordCollection): Training record
            - (RecordCollection): Testing record
            - (RecordCollection): Validation record
    """
    with open('/opt/ml/input/data/training/data/indices.json', 'r') as file:
        indices_dict = json.load(file)
    
    parser = COCOBBoxParser(annotations_filepath='/opt/ml/input/data/training/data/mixed_annotations.json',
                            img_dir='/opt/ml/input/data/training/')
    splitter = FixedSplitter(splits=[indices_dict['train'], indices_dict['val']])

    train, val = parser.parse(data_splitter=splitter, autofix=True)

    return train, val

def get_transforms(config) -> Tuple[tfms.A.Adapter]:
    """
    Get the transformations for each set.

    Args:
        config (Config): Configuration object

    Returns:
        Tuple[tfms.A.Adapter]: Tuple containing:
            - (tfms.A.Adapter): Training transforms
            - (tfms.A.Adapter): Validation transforms
            - (tfms.A.Adapter): Testing transforms
    """
    img_size = int(config['img_size'])

    train_tfms = tfms.A.Adapter(
        [
            #*tfms.A.aug_tfms(size=config.IMG_SIZE, presize=config.PRESIZE),
            tfms.A.Resize(img_size, img_size),
            tfms.A.Normalize(),
        ]
    )

    valid_tfms = tfms.A.Adapter(
        [#*tfms.A.resize_and_pad(config.IMG_SIZE), 
             tfms.A.Resize(img_size, img_size),
             tfms.A.Normalize()
        ]
    )

    test_tfms = tfms.A.Adapter(
        [#*tfms.A.resize_and_pad(config.IMG_SIZE), 
             tfms.A.Resize(img_size, img_size),
             tfms.A.Normalize()
        ]
    )

    return train_tfms, valid_tfms, test_tfms

def get_metrics(trainer, class_to_check):
    for callback in trainer.callbacks:
        if isinstance(callback, class_to_check):
            return callback.metrics
        
def get_best_metric(metrics):
    loss, coco = metrics['valid/loss'], metrics['COCOMetric']
    loss = np.array(loss)
    coco = np.array(coco)
    
    indice = np.argmin(loss)
    
    return coco[indice]