import h5py
import numpy as np

with h5py.File('/Users/aquiles/Data/2024-04-10/movie_8.h5', 'r') as f:
    dset = f['Movie'][:50, :50, :50, 10:20]
    print(np.min(dset), np.max(dset))