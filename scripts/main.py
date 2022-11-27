import os
import sys
import json
import gradio as gr
import modules.ui
from modules import script_callbacks, sd_models, shared
from modules.ui import setup_progressbar, gr_show
from modules.shared import opts, cmd_opts, state
from webui import wrap_gradio_gpu_call
import html

def on_ui_tabs():
    with gr.Blocks() as checkpoint_manager:
        with gr.Tabs() as tabs:
            with gr.TabItem("Chectpoint"):
                with gr.Row():
                    reload_button = gr.Button(value="Reload")
                    save_button = gr.Button(value="Save")
                    sety_button = gr.Button(value="Set to Y Values")
                    hide_checkbox = gr.Checkbox(label="Hide Checked Checkpoint", value=True, interactive=True)
                    ckectpoint_to_load = gr.Text(elem_id="ckectpoint_to_load", visible=False).style(container=False)
                    load_checkpoint_button = gr.Button(elem_id="load_checkpoint_button", visible=False).style(container=False)
                    json_data = gr.Text(elem_id="json_data", visible=False).style(container=False)
                checkpoint_table = gr.HTML(lambda: ckpt_table())

                reload_button.click(
                    fn=ckpt_table,
                    inputs=[hide_checkbox],
                    outputs=[checkpoint_table],
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
                    fn=load_checkpoint,
                    inputs=[ckectpoint_to_load],
                    outputs=[],
                )

                hide_checkbox.change(
                    fn=change_hide_checkbox,
                    inputs=[hide_checkbox],
                    outputs=[checkpoint_table]
                )

    return (checkpoint_manager, "Checkpoint Manager", "checkpoint_manager"),

script_callbacks.on_ui_tabs(on_ui_tabs)

def ckpt_table(hide=True):
    filename =  os.path.join('extensions', 'checkpoint_manager', "json", 'data.json')
    data = []
    with open(filename) as f:
        data = json.load(f)

    code = f"""
    <table>
        <thead>
            <tr>
                <th>Filename</th>
                <th>Hash</th>
                <th>Comment</th>
                <th>Action</th>
                <th>Select</th>
                <th>Top</th>
                <th>Hide</th>
            </tr>
        </thead>
        <tbody>
    """

    top = ""
    other = ""

    for c in sd_models.checkpoints_list.values():
        found = list(filter(lambda x: x["hash"]==c.hash,data))
        info = found[0] if len(found) > 0 else {"hash":"","comment":"","top":False,"hide":False}
        tr = f"""
            <tr class="checkpoint_manager_row" data-title="{c.title}" {"style='visibility:collapse'" if hide and info.get("hide") else ""}>
                <td width="50%">{os.path.splitext(os.path.basename(c.filename))[0]}</td>
                <td class="checkpoint_manager_hash">{c.hash}</td>
                <td><input class="checkpoint_manager_comment" type="text" value="{info["comment"]}"></td>
                <td><input onclick="load_checkpoint(this, '{c.title}')" type="button" value="Load" class="gr-button gr-button-lg gr-button-secondary"></td>
                <td><input class="checkpoint_manager_select" type="checkbox"></td>
                <td><input class="checkpoint_manager_top" type="checkbox" {"checked" if info.get("top") else ""}></td>
                <td><input class="checkpoint_manager_hide" type="checkbox" {"checked" if info.get("hide") else ""}></td>
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
    gr.update()

    return code

def load_checkpoint(title):
    opts.sd_model_checkpoint = title
    sd_models.reload_model_weights()
    # todo: update "Stable Diffusion checkpoint" dropdown

def save_json(data):
    filename =  os.path.join('extensions', 'checkpoint_manager', "json", 'data.json')
    with open(filename, "w") as f:
        json.dump(json.loads(data), f)

def set_y_values():
    pass

def change_hide_checkbox(hide):
    return ckpt_table(hide)
    # todo: hide from "Stable Diffusion checkpoint" dropdown
    # hide
    # del sd_models.checkpoints_list[title]
    # show
    # sd_models.list_models()