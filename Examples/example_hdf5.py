import h5py
import numpy as np


with h5py.File('test.h5', 'w') as f:
    f.create_dataset('Dataset', (10, 10), dtype=np.uint8, data=np.zeros((10, 10)))


with h5py.File('test.h5', 'r') as f:
    dset = f['Dataset']
    print(dset[2:4, 4:6])
    # dset[2:4, 4:6] = 1  # This does not work!


with h5py.File('test.h5', 'a') as f:
    dset = f['Dataset']
    print(dset[2:4, 4:6])
    dset[2:4, 4:6] = 1
    f.flush()

with h5py.File('test.h5', 'r') as f:
    dset = f['Dataset']
    print(dset[2:4, 4:6])

with h5py.File('variable_size.h5', 'w') as f:
    dset = f.create_dataset('Variable', (10, 10, 1),
                            maxshape=(10, 10, None))
    dset[:, :, 0] = 1
    dset.resize((10, 10, 2))
    dset[:, :, 1] = 2


with h5py.File('compressed.h5', 'w') as f:
    f.create_dataset('Dataset', (10, 10),
                     dtype=np.uint8,
                     data=np.zeros((10, 10)),
                     compression='gzip',
                     compression_opts=5
                     )