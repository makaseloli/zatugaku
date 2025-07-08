from gradio_ui import define_gradio_interface
from config import GRADIO_HOST, GRADIO_PORT

def main():
    interface = define_gradio_interface()
    interface.launch(server_name=GRADIO_HOST, server_port=GRADIO_PORT, mcp_server=True, pwa=True)


if __name__ == "__main__":
    main()
