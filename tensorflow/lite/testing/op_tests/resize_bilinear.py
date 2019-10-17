# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Test configs for resize_bilinear."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tensorflow.lite.testing.zip_test_utils import create_tensor_data
from tensorflow.lite.testing.zip_test_utils import make_zip_of_tests
from tensorflow.lite.testing.zip_test_utils import register_make_test_function


@register_make_test_function()
def make_resize_bilinear_tests(options):
  """Make a set of tests to do resize_bilinear."""

  test_parameters = [{
      "dtype": [tf.float32, tf.int32],
      "input_shape": [[1, 3, 4, 3], [1, 10, 2, 1]],
      "size": [[1, 1], [4, 3], [2, 2], [5, 6]],
      "align_corners": [None, True, False],
  }]

  def build_graph(parameters):
    input_tensor = tf.placeholder(
        dtype=parameters["dtype"],
        name="input",
        shape=parameters["input_shape"])
    out = tf.image.resize_bilinear(
        input_tensor,
        size=parameters["size"],
        align_corners=parameters["align_corners"])
    return [input_tensor], [out]

  def build_inputs(parameters, sess, inputs, outputs):
    input_values = create_tensor_data(parameters["dtype"],
                                      parameters["input_shape"])
    return [input_values], sess.run(
        outputs, feed_dict=dict(zip(inputs, [input_values])))

  make_zip_of_tests(options, test_parameters, build_graph, build_inputs)