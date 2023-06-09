import os.path
import gradio as gr
import glob
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

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


with gr.Blocks(css='./styles.css') as demo:
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
        gr.HTML('<iframe src="static/index.html" height=500, width="100%"/>', elem_id='react')
    # append civitai to here
    # TODO: make it a new tab
    with gr.Column(variant="panel"):
        gr.HTML('<iframe src="https://civitai.com/" height=500, width="100%"/>', elem_id='something-amazing')
    btn.click(load_images, text, gallery)

if __name__ == "__main__":
    app = FastAPI()
    static_dir = Path('./easy-animation/build')
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    # mount Gradio app to FastAPI app
    app = gr.mount_gradio_app(app, demo, path="/")
    uvicorn.run(app, host="127.0.0.1", port=7860)