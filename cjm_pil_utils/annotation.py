# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_annotation.ipynb.

# %% auto 0
__all__ = ['draw_masks', 'draw_bboxes']

# %% ../nbs/01_annotation.ipynb 3
# Import necessary modules from the standard library
from pathlib import Path  # For working with file paths
import hashlib
from glob import glob
import numpy as np  # For working with arrays
from PIL import Image, ImageColor, ImageDraw, ImageFont  # For working with images

# %% ../nbs/01_annotation.ipynb 5
def draw_masks(image:Image, # The input image on which annotations will be drawn.
               masks:np.ndarray, # A 3D numpy array of shape (n_masks, height, width) representing segmentation masks.
               labels:list, # A list of labels corresponding to each segmentation mask.
               colors:list, # A list of RGB tuples for each segmentation mask and its corresponding label.
               conf_threshold:float, # The threshold value to convert mask to binary.
               alpha:float=0.3 # The alpha value for mask transparency.
              ) -> Image:  # The image annotated with segmentation masks and labels.
    """
    Annotates an image with segmentation masks, labels, and optional alpha blending.

    This function draws segmentation masks on the provided image using the given mask arrays, 
    colors, labels, and alpha values for transparency.
    """
    
    # Create a copy of the image
    annotated_image = image.copy()
    annotated_image.convert('RGBA')

    # Create an ImageDraw object for drawing on the image
    draw = ImageDraw.Draw(annotated_image)

    # Loop through the bounding boxes and labels in the 'annotation' DataFrame
    for i in range(len(labels)):
        
        # Get the segmentation mask
        mask = masks[i][0, :, :]
        mask_color = [*colors[i], alpha*255]

        # Create an empty 3D array with shape (height, width, 3)
        rgb_mask = np.zeros((mask.shape[0], mask.shape[1], 4), dtype=np.uint8)
        
        # Use broadcasting to populate it with the mask color where the mask is 1
        rgb_mask[mask > conf_threshold] = mask_color
        
        # Convert the numpy array to a PIL Image
        mask_img = Image.fromarray(rgb_mask)
        
        # Draw segmentation mask on sample image
        annotated_image.paste(mask_img, (0,0), mask=mask_img)
        
    return annotated_image

# %% ../nbs/01_annotation.ipynb 6
def draw_bboxes(image:Image, # The input image on which annotations will be drawn.
                    boxes:list, # A list of bounding box coordinates. The format is determined by `box_format`.
                    labels:list, # A list of labels corresponding to each bounding box.
                    colors:list, # A list of colors for each bounding box and its corresponding label.
                    font:str, # Path to the font file to be used for displaying the labels.
                    box_format:str="xywh", # The format of the bounding boxes ("xywh" for [x, y, w, h], "xyxy" for [x1, y1, x2, y2],or "cxywh" for [center-x, center-y, width, height]). Defaults to "xywh".
                    width:int=2, # Width of the bounding box lines.
                    font_size:int=18, # Size of the font for the labels.
                    probs:int=None # A list of probability scores corresponding to each label.
                   ) -> Image: # The image annotated with bounding boxes, labels, and optional probability scores.
    """
    Annotates an image with bounding boxes, labels, and optional probability scores.

    This function draws bounding boxes on the provided image using the given box coordinates,
    colors, and labels. If probabilities are provided, they will be added to the labels.
    """

    # Define a reference diagonal
    REFERENCE_DIAGONAL = 1000

    # Scale the font size using the hypotenuse of the image
    font_size_scaled = int(font_size * (np.hypot(*image.size) / REFERENCE_DIAGONAL))

    # Add probability scores to labels
    if probs is not None:
        labels = [f"{label}: {prob*100:.2f}%" for label, prob in zip(labels, probs)]

    # Create a copy of the image
    annotated_image = image.copy()

    # Create an ImageDraw object for drawing on the image
    draw = ImageDraw.Draw(annotated_image)

    # Load the font file
    fnt = ImageFont.truetype(font, font_size_scaled)

    for i, box in enumerate(boxes):
        if box_format == "xywh":
            x, y, w, h = box
            shape = (x, y, x + w, y + h)
        elif box_format == "xyxy":
            shape = tuple(box)
        elif box_format == "cxywh":
            cx, cy, w, h = box
            x = cx - w / 2
            y = cy - h / 2
            shape = (x, y, x + w, y + h)
        else:
            raise ValueError("Invalid box_format. Choose between 'xywh', 'xyxy', or 'cxywh'.")

        # Draw the bounding box on the image
        draw.rectangle(shape, outline=colors[i], width=width)

        # Draw the label box on the image
        label_w, label_h = draw.textbbox(xy=(0, 0), text=labels[i], font=fnt)[2:]
        text_x, text_y = shape[0], shape[1] - label_h
        draw.rectangle((text_x, text_y, text_x + label_w, text_y + label_h), outline=colors[i], fill=colors[i], width=width)

        # Determine text color based on bounding box color brightness
        text_color = 'black' if np.mean(colors[i]) > 127.5 else 'white'
        
        # Draw the label on the image
        draw.multiline_text((text_x, text_y), labels[i], font=fnt, fill=text_color)

    return annotated_image
