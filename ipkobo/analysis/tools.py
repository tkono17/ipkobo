#------------------------------------------------------------------------
# model/analysis/tools.py
#------------------------------------------------------------------------
import logging
import numpy as np
from numpy.lib.stride_tricks import as_strided

logger = logging.getLogger(__name__)

def conv2d(m, k):
    """Calculates the 2d convolution in a valid region."""
    if not (m.ndim == 2 and k.ndim == 2):
        logger.warning('conv2d takes two arrays with dimension 2')
        logger.warning(f'  dimension of m={m.ndim}, k={k.ndim}')
        return

    shape1 = k.shape + np.subtract(m.shape, k.shape) + 1
    strides1 = np.array(m.strides*2)*m.itemsize

    logger.info(f'conv2d: m itemsize: {m.itemsize}')
    logger.info(f'conv2d: m={m.shape}, k={k.shape}')
    logger.info(f'  shape1={shape1}, strides1={strides1}')
    km = as_strided(m, shape=shape1, strides=strides1, writeable=False)
    y = np.einsum('ij,ijkl->kl', k, km)
    return y
    
        
        
