cjm-pil-utils
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

## Install

``` sh
pip install cjm_pil_utils
```

## How to use

### get_img_files

``` python
from cjm_pil_utils.core import get_img_files
from pathlib import Path
```

``` python
img_dir = Path('../images/')
img_paths = get_img_files(img_dir)
img_paths
```

    [PosixPath('../images/cat.jpg'), PosixPath('../images/depth-cat.png')]

### resize_img

``` python
from cjm_pil_utils.core import resize_img
from PIL import Image  # For working with images
```

``` python
img_path = img_paths[0]
src_img = Image.open(img_path).convert('RGB')
print(f"Image Size: {src_img.size}")

resized_img = resize_img(src_img, target_sz=384, divisor=32)
print(f"New Image Size: {resized_img.size}")
```

    Image Size: (768, 512)
    New Image Size: (576, 384)

### stack_imgs

``` python
from cjm_pil_utils.core import stack_imgs
```

``` python
stacked_imgs = stack_imgs([resized_img, resized_img])
print(f"Stacked Image Size: {stacked_imgs.size}")
```

    Stacked Image Size: (576, 768)

### avg_images

``` python
from cjm_pil_utils.core import avg_images
```

``` python
img_1, img_2 = (Image.open(path) for path in img_paths)
avg_img = avg_images(img_1, img_2, 0.5)
```
