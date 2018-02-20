import time
import math
import os
import data
import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw, ImageFont

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

testing_dir = 'Datasets/Testing'
model_dir = 'checkpoints/'

imageWidth = 92
imageHeight = 112
imageSize =imageWidth*imageHeight
NChannels = 1
NClasses = 40

NEpochs = 50000
learningRate = 0.1

training_dir = 'Datasets/Training'
X, Y= data.LoadTrainingData(training_dir, (imageWidth, imageHeight))

y = 1
for i in range(360):
    if Y[i][y] == 1:
        break
init = tf.constant(X.reshape([-1, imageSize])[i].reshape([1, imageSize]))
x = tf.Variable(init)

#x = tf.Variable(tf.truncated_normal([1, imageSize]))

w = tf.placeholder(tf.float32, shape=(imageSize, NClasses))
b = tf.placeholder(tf.float32, shape=(NClasses))

def main():
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        new_saver = tf.train.import_meta_graph(model_dir+'model.meta')
        new_saver.restore(sess, tf.train.latest_checkpoint(model_dir))
        graph = tf.get_default_graph()
        weights = sess.run(graph.get_tensor_by_name("weights:0"))
        biases = sess.run(graph.get_tensor_by_name("biases:0"))

        logits = tf.nn.softmax(tf.matmul(x, w) + b)
        loss = 1 - logits[0][y]
        optimizer = tf.train.GradientDescentOptimizer(learningRate).minimize(loss)
        for epoch in range(NEpochs):
            _, l = sess.run([optimizer, loss], feed_dict={w: weights, b: biases})
            if epoch % 1000 == 0:
                print l
 
        data = np.asarray(sess.run(x)*255, dtype=np.uint8).reshape([-1, imageHeight, imageWidth])[0]
        img = Image.fromarray(data, 'L')
        img.save('/home/ubuntu/test.png')           

if __name__ == '__main__':
    main()
