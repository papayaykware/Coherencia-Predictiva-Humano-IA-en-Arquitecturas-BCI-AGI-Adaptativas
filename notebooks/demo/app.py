import gradio as gr
from training.train import train

model, tae = train()

def run_demo():
    return "CPEA activo y ejecutándose"

gr.Interface(fn=run_demo, inputs=[], outputs="text").launch()
