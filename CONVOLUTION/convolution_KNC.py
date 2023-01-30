"""
    This is an implementation for convolution for a NxCxHxW input and K kernels.
    See my article on substack "Vectorized convolutions"
    https://aiandbrains.substack.com/p/vectorized-convolutions
"""
import numpy as np
from dask.array import einsum, asarray
from scipy.signal import convolve2d
import time

def timeit(prec=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"{func.__name__} took {end-start:.{prec}f} seconds")
            return result
        return wrapper
    return decorator

@timeit()
def convolution(x, kernels, stride=1, einsumfunc=np.einsum, return_coords=False, coords = None):
    '''
    The forward pass
    :param x: input matrix, with N*C*(H,W) images (C colours)
    :param kernel: K*(kn,kn) kernels
    :param st: stride
    :return: resulting convolution between x and k
    '''

    N,C,H,W = x.shape 
    K, _, kn, _ = kernels.shape
    pd = kn//2  # padding
    h, w = (H - kn) // stride + 1, (W - kn) // stride + 1
    # N,C,h,w is the size of the output

    if coords is not None:
        micro_images_coords = coords
        
    else:

        # we pad only the last 2 dimensions
        dx = np.pad(x, ((0,0),(0,0),(pd,pd),(pd,pd)))  

        nn, cc, hh, ww = np.meshgrid(
                np.arange(N), np.arange(C), 
                np.arange(0, H, stride),
                np.arange(0, W, stride), indexing='ij')

        kh, kw = np.meshgrid(np.arange(kn), np.arange(kn),  indexing='ij')

        npatches = nn[:, :, :, :, None, None]
        cpatches = cc[:, :, :, :, None, None]
        hpatches = hh[:, :, :, :, None, None] + kh
        wpatches = ww[:, :, :, :, None, None] + kw

        micro_images_coords = dx[npatches, cpatches, hpatches, wpatches] 
        
        if return_coords:
            return micro_images_coords
        
    cnn = einsumfunc('NChwij,KCij -> NKhw', micro_images_coords, kernels, optimize=True)
    # C is present on both sides, so it is summed up

    return cnn  
    
print("="*80)
SEED = 123
    
np.random.seed(SEED)
N,C,H,W = 5,1,15,15 # 1 channel because CNN add up the convolution of each channel of every image, and scipy can't do that
stride = 1  # because scipy convolve2d does not have a stride arg
K,kn = 4,3
x = np.random.rand(N,C,H,W)
kernels = np.random.randn(K,C,kn,kn)

cnn = convolution(x, kernels, stride)

# convolve2d transposes the kernel along both diagonals... so we flip it
# to be able to compare with the result of convolution
cnn_sci = convolve2d(x[0,0], np.flipud(np.fliplr(kernels[0,0])), mode='same')
assert cnn_sci.shape == (H,W), f"Error in shape: {cnn_sci.shape} != {(H,W)}"
print(f"Shape test passed: cnn_sci has shape {cnn_sci.shape} == {(H,W)}")

assert np.all(cnn[0,0] == asarray(cnn[0,0])), "Error in array"
print("Array test passed")

# print('allclose', np.all(np.isclose(np.array(cnn[0,0]), cnn_sci, atol=1e-6)))
assert np.all(np.isclose(cnn[0,0], cnn_sci, atol=1e-6)), "Error for n,c,k = 0,0,0"
print("First test passed with first image, first colour, first kernel")
print("="*80)

for n in range(N):
        for k in range(K):
            xstr = x[n,0]  # scipy has no stride arg
            cnn_sci = convolve2d(xstr, np.flipud(np.fliplr(kernels[k,0])), mode='same')
            assert np.allclose(cnn[n,k], cnn_sci, rtol=1e-05), f"Error for n,k = {n,k}"

print("All tests passed")
print("="*80)

# ================================================================================
# Shape test passed: cnn_sci has shape (15, 15) == (15, 15)
# Array test passed
# First test passed with first image, first colour, first kernel
# ================================================================================
# All tests passed
# ================================================================================

# let's test the time gained with Dask
np.random.seed(SEED)
N,C,H,W = 15,3,1000,1000 
stride = 3  
K,kn = 5,15
x = np.random.rand(N,C,H,W)
kernels = np.random.randn(K,C,kn,kn)

# lets time the creation of the coordinates separately because 
# it's the same for both, so we'l have the real difference by using Dask 
coords = convolution(x, kernels, stride, return_coords=True) # 55s

cnn = convolution(x, kernels, stride, coords=coords)  # 37s

cnn2 = convolution(x, kernels, stride, einsumfunc=einsum, coords=coords)   # 21s
del(coords)

# convolution took 55.555 seconds  (creation of the coordinates)
# convolution took 36.873 seconds  # Numpy
# convolution took 21.247 seconds  # Dask 

# ================================================================================
# comparison Dask - Scipy
# here we have to take N=C=K=stride=1 again
print("="*80)
SEED = 123
    
np.random.seed(SEED)
N,C,H,W = 1,1,1000,1000 # 1 channel because CNN add up the convolution of each channel of every image, and scipy can't do that
stride = 1  # because scipy convolve2d does not have a stride arg
K,kn = 1,15 # scipy can't process more than 1 kernel anyway
x = np.random.rand(N,C,H,W)
kernels = np.random.randn(K,C,kn,kn)

coords = convolution(x, kernels, stride, return_coords=True) # 9.5s

cnn = convolution(x, kernels, stride, einsumfunc=einsum, coords=coords) # 4.1s
del(coords)

start = time.time()
cnn_sci = convolve2d(x[0,0], np.flipud(np.fliplr(kernels[0,0])), mode='same')
print(f"Scipy took {time.time()-start:.1f} seconds")  # 0.9s

# convolution took 9.469 seconds (creation of the coordinates)
# convolution took 4.088 seconds
# Scipy took 0.9 seconds