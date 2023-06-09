# -*- coding: UTF-8 -*-

import pathlib
import typing

import urllib3
import modules.scripts as scripts
import gradio as gr
import os
import webbrowser
import requests
import random
import hashlib
import json
import shutil
import re
import modules
from modules import script_callbacks
from modules import shared

# init

# root path
root_path = os.getcwd()

# extension path
extension_path = scripts.basedir()

# iterate over files in
# that directory
valid_images = [".jpg", ".bmp", ".png", ".tga"]
cwd = os.path.normpath(os.path.join(__file__, "../"))

image_store = []

def load_images(dir):
    image_store.clear()
    assert os.path.exists(dir)
    images = []
    for image in glob.iglob(f'{dir}/*'):
        ext = os.path.splitext(image)[1]
        if ext.lower() not in valid_images:
            continue
        images.append(image)
    images.sort()
    image_store.extend(images)
    return images

def on_select(evt: gr.SelectData):
    pre_frame = image_store[evt.index - 1] if evt.index > 1 else None
    next_frame = image_store[evt.index + 1] if evt.index + 1 < len(image_store) else None
    return [pre_frame, image_store[evt.index], next_frame]

def on_ui_tabs():
    with gr.Blocks(css='./styles.css') as sd_easy_animation:
        with gr.Column(variant="panel"):
            with gr.Row(variant="compact"):
                text = gr.Textbox(
                    label="Frame dist",
                    show_label=False,
                    max_lines=1,
                    placeholder="Enter your frame dist",
                ).style(container=False)
                btn = gr.Button("Load Images").style(full_width=False)
            gallery = gr.Gallery(
                label="Generated images", show_label=False, elem_id="gallery"
            ).style(columns=2, preview=True)
            with gr.Row(variant="compact"):
                previousFrame = gr.Image(label="Previous Frame")
                currentFrame = gr.Image(label="Current Frame")
                nextFrame = gr.Image()
            gallery.select(fn=on_select, inputs=None, outputs=[previousFrame, currentFrame, nextFrame])
        with gr.Column(variant="panel"):
            html_path =  os.path.join(extension_path,"easy-animation","build","index.html")
            html_url = f"/file={html_path}"
            print("test" + html_url)
            gr.HTML(
                f"""
                <iframe src="{html_url}" height=500, width="100%"/>
                """,
                elem_id='react'
            )
        btn.click(load_images, text, gallery)

        return (
            (
                sd_easy_animation,
                "sd-easy-animation",
                "sd_easy_animation",
            ),
        )

def on_civitai_ui_tabs():
    with gr.Blocks(css='./styles.css') as sd_easy_civitai:
        # append civitai to here
        with gr.Column(variant="panel"):
            gr.HTML('<iframe src="https://civitai.com/" height=850, width="100%"/>', elem_id='something-amazing')
        return (
            (
                sd_easy_civitai,
                "sd-easy-civitai",
                "sd_easy_civitai",
            ),
        )

def InitTabUI():
    script_callbacks.on_ui_tabs(on_ui_tabs)
    script_callbacks.on_ui_tabs(on_civitai_ui_tabs)

InitTabUI()