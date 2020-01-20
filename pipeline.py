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
import kfp.onprem as onprem

platform = 'GCP'

@dsl.pipeline(
  name='Fuel',
  description='Fuel Prediction pipeline.'
)
def fuel_pipeline(bucket_name='gs://your-bucket/export',
                   input_file='folder/file',
                   output_folder='output folder',
                   epochs = 10):
  preprocess= dsl.ContainerOp(
      name='preprocess',
      image='gcr.io/kb-poc-262417/fuel:latest',
      arguments=[
          '--input_file', input_file,
          '--output_folder', output_folder,
          '--bucket_name', bucket_name
          ]
  )

  train= dsl.ContainerOp(
      name='train',
      image='gcr.io/kb-poc-262417/fuel/train:latest',
      arguments=[
          '--bucket_name', bucket_name,
          '--epochs', epochs
          ]
  )
  train.after(preprocess)
  
  serve= dsl.ContainerOp(
      name='serve',
      image='gcr.io/kb-poc-262417/fuel/serve:latest',
      arguments=[
          '--bucket_name',bucket_name
          ]
  )

  serve.after(train)

  steps = [preprocess, train, serve]
  for step in steps:
    if platform == 'GCP':
      step.apply(gcp.use_gcp_secret('user-gcp-sa'))
    else:
      step.apply(onprem.mount_pvc(pvc_name, 'local-storage', '/mnt'))

if __name__ == '__main__':
  import kfp.compiler as compiler
  compiler.Compiler().compile(fuel_pipeline, __file__ + '.tar.gz')
