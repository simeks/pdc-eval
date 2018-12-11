import os
import SimpleITK as sitk
import numpy as np

if 'PDC_EVAL_DATA_PATH' in os.environ:
    data_path = os.environ['PDC_EVAL_DATA_PATH']
else:
    data_path = 'data'

# Scales:
# 0 | 1/8x |  22 x  24 x  20 |
# 1 | 1/4x |  45 x  49 x  41 |
# 2 | 1/2x |  90 x  99 x  82 |
# 3 |   1x | 180 x 198 x 165 |
# 4 |   2x | 360 x 396 x 330 |

scales = [
    1/8,
    1/4,
    1/2,
    1,
    2
]

img_path = os.path.join(data_path, 'images')
resampled_path = os.path.join(data_path, 'resampled')

for f in os.listdir(img_path):
    src = sitk.ReadImage(os.path.join(img_path, f))
    src.SetOrigin((0,0,0))
    src.SetSpacing((1,1,1))

    for i in range(0,5):
        s = scales[i]
        am = (
            1/s, 0,   0,
            0,   1/s, 0,
            0,   0,   1/s
        )

        t = sitk.AffineTransform(am, (0,0,0))
        out = sitk.Resample(src, [int(s*x) for x in src.GetSize()], t, sitk.sitkLinear)
        out.SetSpacing((1/s,1/s,1/s))
        
        sitk.WriteImage(out, os.path.join(resampled_path, '{}_{}.vtk'.format(f[:-4], i)))