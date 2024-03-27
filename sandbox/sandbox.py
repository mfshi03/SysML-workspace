import time
import os
import cairosvg
import base64
import xml.etree.ElementTree as ET
from PIL import Image
from jupyter_client import KernelManager
from io import BytesIO

class JupyterSandbox:
    def __init__(self, kernel_name):
        self.kernel_name = kernel_name
        self.km = None
        self.kc = None
        self.img = None

    def start_kernel(self):
        self.km = KernelManager(kernel_name=self.kernel_name)
        self.km.start_kernel()
        self.kc = self.km.client()
        self.kc.start_channels()
        self.kc.wait_for_ready()

    def execute_code(self, code):
        msg_id = self.kc.execute(code)
        res = {}
        while True:
            try:
                msg = self.kc.get_iopub_msg(timeout=1)
                content = msg["content"]
                if "data" in content and "text/plain" in content["data"]:
                    print("Output:", content["data"]["text/plain"])
                    res["text"] = content["data"]["text/plain"]
                if "data" in content and "image/svg+xml" in content["data"]:
                    res["img"] = content['data']['image/svg+xml']
                    self.img = content['data']['image/svg+xml']
            except KeyboardInterrupt:
                print("Interrupted by user.")
                break
            except:
                pass

    def save_image(self):
        print(self.img)
        try:
            cairosvg.svg2png(bytestring=self.img, write_to="sysmlv2.png")
        except Exception as e:
            print(f"Error saving image: {str(e)}")

    def stop_kernel(self):
        self.kc.stop_channels()
        self.km.shutdown_kernel()

def main():
    sandbox = JupyterSandbox(kernel_name='sysml')
    sandbox.start_kernel()

    code = '''
    part def Camera {
        import PictureTaking::*;
        perform action takePicture[*] :> PictureTaking::takePicture;
        part focusingSubsystem {
            perform takePicture.focus;
        }
        part imagingSubsystem {
            perform takePicture.shoot;
        }
    }

    package PictureTaking {
        part def Exposure;
        action def Focus { out xrsl: Exposure; }
        action def Shoot { in xsf: Exposure; }
        action takePicture {
            action focus: Focus[1];
            flow focus.xrsl to shoot.xsf;
            action shoot: Shoot[1];
        }
    }
    '''

    viz = '''%viz --view=tree PictureTaking'''

    sandbox.execute_code(code)
    sandbox.execute_code(viz)
    sandbox.stop_kernel()
    sandbox.save_image()
    

if __name__ == '__main__':
    main()