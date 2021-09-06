# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 17:37:51 2021

@author: suvarna
"""

########################## LIBRARIES & MODULES #############################

import numpy as np
import cv2
from PIL import Image
from io import BytesIO
import colour
import streamlit as st

########################## DEFINE FUNCTIONS ################################
# Function to covert Red background image to Transparent background image
######### Finding memory size ##############
def input_img(inp_img):
    open_image = inp_img
    out_file = BytesIO()
    if(open_image.mode != 'CMYK'):
        if(open_image.format == 'JPEG'):
            open_image.save(out_file, 'png')
            img = np.array(Image.open(out_file))
        else:
            img = np.array(open_image)
    else:
        open_image.convert('RGB').save(out_file, 'png')
        img = np.array(Image.open(out_file))
    return(img)

def memory_size(inp_image):
    ext = inp_image.format
    out_file = BytesIO()    
    if(ext == 'PNG'):
        inp_image.save(out_file, 'png')
    elif(ext == 'JPEG' ):
        if(inp_image.mode != 'CMYK'):
            inp_image.save(out_file, 'jpeg')
        else:
            inp_image.convert('RGB')
            inp_image.save(out_file, 'jpeg')
    out_size = out_file.tell()/1000   
    return(out_size)

######### CHECKING FOR delta_E #############
def pix_delta(path1, path2):
    image1_rgb = path1
    image2_rgb = path2
    image1_lab = cv2.cvtColor(image1_rgb.astype(np.float32) / 255, cv2.COLOR_RGB2Lab)
    image2_lab = cv2.cvtColor(image2_rgb.astype(np.float32) / 255, cv2.COLOR_RGB2Lab)
    deltaE = colour.delta_E(image1_lab, image2_lab)
    del_mean = np.mean(deltaE)
    if(del_mean == 0.0):
        return('True')
    else:
        return('False')

############################################################################
########################## CODE BEGINS HERE ################################
############################################################################

# Give a title
st.title('IMAGE COMPARATOR')

# Upload the images

img_data1 = st.file_uploader(label='Load First Image', type=['png', 'jpg', 'jpeg'])
img_data2 = st.file_uploader(label='Load Second Image', type=['png', 'jpg', 'jpeg'])

if img_data1 and img_data2 is not None:
    
    uploaded_img1 = Image.open(img_data1)
    uploaded_img2 = Image.open(img_data2)
    
    img11 = input_img(uploaded_img1)
    img22 = input_img(uploaded_img2)
    
    # Display Uploaded Images Horizontally
    col1, col2 = st.beta_columns(2)
    col1.markdown('**Image 1**')
    col1.image(img11, use_column_width=True)
    col1.text('Size: ' + str(memory_size(uploaded_img1)) + ' KB,' + '  Dimensions: ' + str(uploaded_img1.size))  
    
    col2.markdown('**Image 2**')
    col2.image(img22, use_column_width=True)
    col2.text('Size: ' + str(memory_size(uploaded_img2)) + ' KB,' + '  Dimensions: ' + str(uploaded_img2.size)) 
    
############################################################################
    
    if(uploaded_img1.size == uploaded_img2.size):
        pixel_check = pix_delta(img11, img22)
        if(pixel_check == 'True'):
            st.text('Pixels match exactly')
        else:
            st.text('Pixels do not match exactly')
    else:
        st.text('Dimensions are different')
        
    memory = (memory_size(uploaded_img1) == memory_size(uploaded_img2))
    dimension = (str(uploaded_img1.size) == str(uploaded_img2.size))
    
    if(memory and dimension and pixel_check):
        st.markdown('**Images are same: DO NOT PROCESS**')
    else:
        st.markdown('**Images are different: PROCESS**')
 