import os
_TEST_ROOT = os.path.dirname(__file__)  # root of test folder

ANNOTATIONS = f'{_TEST_ROOT}/data/test_annotations.json'
IMG_DIR = f'{_TEST_ROOT}/data/'
INDICES = f'{_TEST_ROOT}/data/indices.json'

TRAIN_CLASS = f'{_TEST_ROOT}/data/train_class.pkl'
VAL_CLASS = f'{_TEST_ROOT}/data/val_class.pkl'