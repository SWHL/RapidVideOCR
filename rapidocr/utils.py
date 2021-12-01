# !/usr/bin/env python
# -*- encoding: utf-8 -*-
# @File: utils.py
# @Author: SWHL
# @Contact: liekkaskono@163.com
import onnxruntime as ort


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

    def get_inputs(self, *args):
        return self.sess.get_inputs(*args)

    def get_outputs(self, *args):
        return self.sess.get_outputs(*args)

    def init_session(self, model_path):
        EP_list = ['CPUExecutionProvider']
        sess = ort.InferenceSession(model_path, providers=EP_list)
        return sess
