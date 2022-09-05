import torch
import tensorflow as tf

# device = torch.device('cuda:1')
# x = torch.tensor([1., 2.]).to(device) # GPU 1에 할당

from tensorflow.python.client import device_lib

device_lib.list_local_devices()
print(tf.test.is_gpu_available())

USE_CUDA = torch.cuda.is_available()
print(USE_CUDA)

with torch.cuda.device(0):
    # GPU 0 에 할당 
    x = torch.tensor([1., 2.]).to("cuda")
    print(x)