# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Kubeflow Pipelines MNIST example

Run this script to compile pipeline
"""

import kfp.dsl as dsl
import kfp.gcp as gcp
from kfp.dsl.types import String


@dsl.pipeline(
  name='MNIST Pipeline',
  description='Demonstrate TF-Serving'
)
def mnist_serveonly(model_export_dir='gs://your-bucket/export'
  ):

  serve = dsl.ContainerOp(
      name='serve',
      image='gcr.io/google-samples/ml-pipeline-kubeflow-tfserve:v2',
      arguments=["--model_name", 'mnist-%s' % (dsl.RUN_ID_PLACEHOLDER,),
          "--model_path",
          'gs://a-kb-poc-262417/mnist2/export/model'
          ]
      ).apply(gcp.use_gcp_secret('user-gcp-sa'))



if __name__ == '__main__':
  import kfp.compiler as compiler
  compiler.Compiler().compile(mnist_serveonly, __file__ + '.tar.gz')
