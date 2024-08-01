
# Introducing Deep Learning Pipelines for Apache Spark

## Overview

This project demonstrates the use of Databricks' Deep Learning Pipelines for scalable deep learning model application and transfer learning with Apache Spark. The Deep Learning Pipelines library integrates popular deep learning libraries (TensorFlow, Keras) with Spark MLlib Pipelines and Spark SQL, providing high-level APIs for efficient image processing and model deployment.

## Table of Contents

1. [Introduction](#introduction)
2. [Cluster Setup](#cluster-setup)
3. [Quick User Guide](#quick-user-guide)
4. [Implementation](#implementation)
   - [TensorFlow Integration](#tensorflow-integration)
   - [Keras Integration](#keras-integration)
5. [Testing](#testing)
6. [Enhancements](#enhancements)
7. [Conclusion](#conclusion)
8. [References](#references)

## Introduction

Deep Learning Pipelines is a library by Databricks designed to simplify the application of deep learning models and transfer learning within Spark environments. It allows users to work seamlessly with images, leveraging both TensorFlow and Keras for scalable deep learning tasks.

## Cluster Setup

### Installation

1. **Add Deep Learning Pipelines Library:**
   - Go to your Databricks cluster settings.
   - Add a new library with the Source option "Maven Coordinate."
   - Search for and add `spark-deep-learning`.

2. **Additional Libraries:**
   - Install TensorFlow, Keras, and h5py via PyPI.

3. **Compatibility:**
   - Deep Learning Pipelines is compatible with Spark versions 2.0 or higher.
   - Works with both CPU and GPU instances.

*Note:* This setup uses `spark-deep-learning` release `0.1.0-spark2.1-s_2.11`. Check the [project's GitHub page](https://github.com/databricks/spark-deep-learning) for the latest versions and updates.

## Quick User Guide

Deep Learning Pipelines provides tools for:

- Working with images natively in Spark DataFrames
- Transfer learning for leveraging pre-trained deep learning models
- Applying models at scale to image data
- Deploying models as SQL functions (upcoming feature)
- Distributed hyper-parameter tuning via Spark MLlib Pipelines (upcoming feature)

## Implementation

### TensorFlow Integration

1. **Example Code:**

   ```python
   from sparkdl import readImages, TFImageTransformer
   from sparkdl.transformers import utils
   import tensorflow as tf

   image_df = readImages(sample_img_dir)

   g = tf.Graph()
   with g.as_default():
       image_arr = utils.imageInputPlaceholder()
       resized_images = tf.image.resize_images(image_arr, (299, 299))
       frozen_graph = utils.stripAndFreezeGraph(g.as_graph_def(add_shapes=True), tf.Session(graph=g), [resized_images])

   transformer = TFImageTransformer(inputCol="image", outputCol="transformed_img", graph=frozen_graph,
                                    inputTensor=image_arr, outputTensor=resized_images, outputMode="image")
   tf_trans_df = transformer.transform(image_df)
   ```

2. **Explanation:**
   - Transform image data using TensorFlow models
   - Utilize pre-trained models or custom TensorFlow graphs

### Keras Integration

1. **Example Code:**

   ```python
   from keras.applications import InceptionV3
   from keras.preprocessing.image import img_to_array, load_img
   import numpy as np
   from pyspark.sql.types import StringType
   from sparkdl import KerasImageFileTransformer

   model = InceptionV3(weights="imagenet")
   model.save('/tmp/model-full.h5')
   dbfs_model_path = 'dbfs:/models/model-full.h5'
   dbutils.fs.cp('file:/tmp/model-full.h5', dbfs_model_path)

   def loadAndPreprocessKerasInceptionV3(uri):
       image = img_to_array(load_img(uri, target_size=(299, 299)))
       image = np.expand_dims(image, axis=0)
       return preprocess_input(image)

   dbutils.fs.cp(dbfs_model_path, 'file:/tmp/model-full-tmp.h5')
   transformer = KerasImageFileTransformer(inputCol="uri", outputCol="predictions",
                                           modelFile='/tmp/model-full-tmp.h5',
                                           imageLoader=loadAndPreprocessKerasInceptionV3,
                                           outputMode="vector")

   files = ["/dbfs" + str(f.path)[5:] for f in dbutils.fs.ls(sample_img_dir)]
   uri_df = sqlContext.createDataFrame(files, StringType()).toDF("uri")
   keras_pred_df = transformer.transform(uri_df)
   ```

2. **Explanation:**
   - Load and preprocess images using Keras
   - Apply pre-trained or custom Keras models to image data

## Testing

- **Evaluation:**
  - Verify model predictions
  - Compare performance with and without transfer learning
  - Visualize prediction results and model accuracy

## Enhancements

- **Upcoming Features:**
  - SQL function deployment for models
  - Distributed hyper-parameter tuning

## Conclusion

Deep Learning Pipelines for Apache Spark provides an efficient way to integrate and deploy deep learning models at scale. The library simplifies image processing tasks and allows for easy integration with TensorFlow and Keras, making it a powerful tool for scalable deep learning applications.

## Presentation Slides
https://docs.google.com/presentation/d/1t0HoznxrmKUX8rkt3nGpKTNuwXx3eP5vw9aE3yni0EM/edit?usp=sharing

## References

- [Databricks Blog Post on Deep Learning Pipelines](https://databricks.com/blog/2023/09/01/deep-learning-pipelines.html)
- [Deep Learning Pipelines GitHub Repository](https://github.com/databricks/spark-deep-learning)
- [Databricks Documentation](https://docs.databricks.com/)

```

