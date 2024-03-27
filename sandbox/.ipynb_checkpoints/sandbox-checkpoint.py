from jupyter_client import BlockingKernelClient
from io import StringIO, BytesIO
import sys
import base64
from PIL import Image

class CodeSandbox:
    def __init__(self):
        self.km = BlockingKernelClient()
        self.km.start_channels()

    def execute_code(self, code):
        stdout = BytesIO()
        stderr = BytesIO()

        # Capture stdout and stderr
        sys.stdout = stdout
        sys.stderr = stderr

        # Execute the code
        msg_id = self.km.execute(code)

        # Wait for the execution to finish
        while True:
            msg = self.km.get_iopub_msg()
            if msg['msg_type'] == 'status' and msg['content']['execution_state'] == 'idle':
                break

        # Restore stdout and stderr
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        # Get the captured output
        output = stdout.getvalue().decode('utf-8')
        error = stderr.getvalue().decode('utf-8')

        # Check if the output contains an image
        if output.startswith("data:image/png;base64,"):
            # Extract the base64-encoded image data
            image_data = output.split(",")[1]

            # Decode the base64 data
            image_data = base64.b64decode(image_data)

            # Create a BytesIO object from the image data
            image_stream = BytesIO(image_data)

            # Open the image using PIL
            image = Image.open(image_stream)

            # Save the image to a file
            image.save("generated_image.png")

            output = "Image saved as 'generated_image.png'"

        return output, error

    def shutdown(self):
        self.km.stop_channels()
        self.km.shutdown()

if __name__ == "__main__":
    sandbox = CodeSandbox()

    # Example code to generate an image using matplotlib
    code = '''
    import matplotlib.pyplot as plt
    import numpy as np

    # Generate random data
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    # Create a plot
    plt.plot(x, y)
    plt.title("Sine Wave")
    plt.xlabel("x")
    plt.ylabel("sin(x)")

    # Save the plot as a base64-encoded PNG image
    from io import BytesIO
    import base64

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_data = base64.b64encode(buffer.getvalue()).decode()
    print(f"data:image/png;base64,{image_data}")
    '''

    output, error = sandbox.execute_code(code)
    print("Output:")
    print(output)

if error:
    print("Error:")
    print(error)

sandbox.shutdown()