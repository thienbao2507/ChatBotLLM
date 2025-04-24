import gradio as gr

def build_gradio_ui(chat_func, upload_func, toggle_func):
    with gr.Blocks() as app:
        gr.Markdown("## 🤖 ChatBot Gemini")
        pdf_upload = gr.File(label="📄 Tải lên file PDF", file_types=[".pdf"])
        upload_status = gr.Textbox(label="Trạng thái đọc file", interactive=False)
        chatbot = gr.ChatInterface(fn=chat_func)
        pdf_upload.change(fn=upload_func, inputs=pdf_upload, outputs=upload_status)
        mode_toggle = gr.Checkbox(label="🛍️ Bật chế độ tư vấn khách hàng")
        toggle_status = gr.Textbox(label="Trạng thái chế độ", interactive=False)
        mode_toggle.change(fn=toggle_func, inputs=mode_toggle, outputs=toggle_status)
    return app
