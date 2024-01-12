# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_annotation.ipynb.

# %% auto 0
__all__ = ['draw_masks', 'draw_bboxes']

# %% ../nbs/01_annotation.ipynb 3
# Import necessary modules from the standard library
from pathlib import Path  # For working with file paths
import hashlib
from glob import glob
import numpy as np  # For working with arrays
from PIL import Image, ImageDraw  # For working with images

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
                boxes:list, # A list of bounding box coordinates where each tuple is (x, y, w, h).
                labels:list, # A list of labels corresponding to each bounding box.
                colors:list, # A list of colors for each bounding box and its corresponding label.
                font:str, # Path to the font file to be used for displaying the labels.
                width:int=2, # Width of the bounding box lines.
                font_size:int=18, # Size of the font for the labels.
                probs:list=None # A list of probability scores corresponding to each label.
               ) -> Image: # The image annotated with bounding boxes, labels, and optional probability scores.
    """
    Annotates an image with bounding boxes, labels, and optional probability scores.

    This function draws bounding boxes on the provided image using the given box coordinates, 
    colors, and labels. If probabilities are provided, they will be added to the labels.
    """
    
    # Define a reference diagonal
    REFERENCE_DIAGONAL = 1000
    
    # Scale the font size using the hypotenuse of the image
    font_size = int(font_size * (np.hypot(*image.size) / REFERENCE_DIAGONAL))
    
    # Add probability scores to labels
    if probs is not None:
        labels = [f"{label}: {prob*100:.2f}%" for label, prob in zip(labels, probs)]
    
    # Create a copy of the image
    annotated_image = image.copy()

    # Create an ImageDraw object for drawing on the image
    draw = ImageDraw.Draw(annotated_image)

    # Loop through the bounding boxes and labels in the 'annotation' DataFrame
    for i in range(len(labels)):
        # Get the bounding box coordinates
        x, y, x2, y2 = boxes[i]

        # Create a tuple of coordinates for the bounding box
        shape = (x, y, x2, y2)

        # Draw the bounding box on the image
        draw.rectangle(shape, outline=colors[i], width=width)
        
        # Load the font file
        fnt = ImageFont.truetype(font, font_size)
        
        # Draw the label box on the image
        label_w, label_h = draw.textbbox(xy=(0,0), text=labels[i], font=fnt)[2:]
        draw.rectangle((x, y-label_h, x+label_w, y), outline=colors[i], fill=colors[i], width=width)

        # Draw the label on the image
        draw.multiline_text((x, y-label_h), labels[i], font=fnt, fill='black' if np.mean(colors[i]) > 127.5 else 'white')
        
    return annotated_image