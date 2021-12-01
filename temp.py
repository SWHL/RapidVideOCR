import multiprocessing as mp

import numpy as np
import onnxruntime as ort


# This is a wrapper to make the current InferenceSession class pickable.
class PickableInferenceSession:
    def __init__(self, model_path):
        self.model_path = model_path
        self.sess = self.init_session(self.model_path)

    def run(self, *args):
        return self.sess.run(*args)

    def __getstate__(self):
        return {'model_path': self.model_path}

    def __setstate__(self, values):
        self.model_path = values['model_path']
        self.sess = self.init_session(self.model_path)

    def init_session(self, model_path):
        EP_list = ['CPUExecutionProvider']
        sess = ort.InferenceSession(model_path, providers=EP_list)
        return sess


class IOProcess(mp.Process):
    def __init__(self):
        super(IOProcess, self).__init__()
        self.sess = PickableInferenceSession('resources/models/ch_mobile_v2.0_rec_infer.onnx')

    def run(self):
        print("calling run")
        onnx_inputs = {self.sess.sess.get_inputs()[0].name: np.zeros((1, 3, 32, 320), dtype=np.float32)}
        print(self.sess.run({}, onnx_inputs))
        # print(self.sess)


if __name__ == '__main__':
    # This is important and MUST be inside the name==main block.
    mp.set_start_method('spawn')
    io_process = IOProcess()
    io_process.start()
    io_process.join()