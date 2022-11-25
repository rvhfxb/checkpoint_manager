import os
import sys
import json
import gradio as gr
import modules.ui
from modules import script_callbacks, sd_models, shared
from modules.ui import setup_progressbar, gr_show
from modules.shared import opts, cmd_opts, state
from webui import wrap_gradio_gpu_call


import gradio as gr
import html

def create_ui():
    with gr.Blocks() as checkpoint_manager:
        with gr.Tabs() as tabs:
            with gr.TabItem("Chectpoint"):
                with gr.Row():
                    reload_button = gr.Button(value="Reload")
                    save_button = gr.Button(value="Save")
                    sety_button = gr.Button(value="Set to Y Values")
                    ckectpoint_to_load = gr.Text(elem_id="ckectpoint_to_load", visible=False)
                    load_checkpoint_button = gr.Button(elem_id="load_checkpoint_button", visible=False)
                    json_data = gr.Text(elem_id="json_data", visible=False).style(container=False)
                ckeckpoint_table = gr.HTML(lambda: ckpt_table())

                reload_button.click(
                    fn=ckpt_table,
                    inputs=[],
                    outputs=[ckeckpoint_table],
                )

                save_button.click(
                    fn=save_json,
                    _js="save_json",
                    inputs=[json_data],
                    outputs=[],
                )

                sety_button.click(
                    fn=set_y_values,
                    _js="set_y_values",
                    inputs=[],
                    outputs=[],
                )

                load_checkpoint_button.click(
                    fn=modules.ui.wrap_gradio_call(load_checkpoint,extra_outputs=[]),
                    inputs=[ckectpoint_to_load],
                    outputs=[],
                )

    return ui


def ckpt_table():
    filename =  os.path.join('extensions', 'checkpoint_manager', "json", 'data.json')
    data = []
    with open(filename) as f:
        data = json.load(f)

    code = f"""
    <style>
        #tab_checkpoint_manager table{{
            border-collapse: collapse;
            width: 100%
        }}

        #tab_checkpoint_manager table td, #tab_checkpoint_manager table th{{
            border: 1px solid #ccc;
            padding: 0.25em 0.5em;
        }}

        #tab_checkpoint_manager table input[type="text"]{{
            width:100%;
        }}

        #tab_checkpoint_manager button{{
            max-width: 16em;
        }}

        #tab_checkpoint_manager input[disabled="disabled"]{{
            opacity: 0.5;
        }}
    </style>
    <table>
        <thead>
            <tr>
                <th>Filename</th>
                <th>Hash</th>
                <th>Comment</th>
                <th>Action</th>
                <th>Select</th>
                <th>Top</th>
            </tr>
        </thead>
        <tbody>
    """

    top = ""
    other = ""

    for c in sd_models.checkpoints_list.values():
        found = list(filter(lambda x: x["hash"]==c.hash,data))
        info = found[0] if len(found) > 0 else {"hash":"","comment":"","top":False}
        tr = f"""
            <tr class="checkpoint_manager_row">
                <td width="50%">{os.path.splitext(os.path.basename(c.filename))[0]}</td>
                <td class="checkpoint_manager_hash">{c.hash}</td>
                <td><input class="checkpoint_manager_comment" type="text" value="{info["comment"]}"></td>
                <td><input onclick="load_checkpoint(this, '{c.title}')" type="button" value="Load" class="gr-button gr-button-lg gr-button-secondary"></td>
                <td><input class="checkpoint_manager_select" type="checkbox"></td>
                <td><input class="checkpoint_manager_top" type="checkbox" {"checked" if info["top"] else ""}></td>
            </tr>
            """
        if info["top"]:
            top += tr
        else:
            other += tr

    code += top
    code += other

    code += """
        </tbody>
    </table>
    """

    return code

def load_checkpoint(title):
    opts.sd_model_checkpoint = title
    sd_models.reload_model_weights()
# fixme : ロードはできるがエラーが出る。左上のドロップダウンが変化しない

# Traceback (most recent call last):
#   File "E:\novelai\stable-diffusion-webui\modules\ui.py", line 185, in f
#     res = list(func(*args, **kwargs))
# TypeError: 'NoneType' object is not iterable

def save_json(data):
    filename =  os.path.join('extensions', 'checkpoint_manager', "json", 'data.json')
    with open(filename, "w") as f:
        json.dump(json.loads(data), f)

def set_y_values():
    pass