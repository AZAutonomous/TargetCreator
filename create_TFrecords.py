import os, json
import tensorflow as tf

#function converts image to TFRecord but does not save it
def convert2TF(image_path, image_name, label):
    filename_queue = tf.train.string_input_producer(image_path)
    reader= tf.WholeFileReader()
    key, value = reader.read(filename_queue)
    my_img = tf.image.decode_jpg(value)
    init_op = tf.initialize_all_variables()
    with tf.Session() as sess:
        sess.run(init_op)
    # Start populating the filename queue.
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    for i in range(1): #length of your filename list
        image = my_img.eval() #here is your image Tensor :) 
        print(image.shape)
        Image.show(Image.fromarray(np.asarray(image)))
        
        coord.request_stop()
        coord.join(threads)
    

#saves Tensor as a file
#***needs to be redone have issues
def convert_to(image, label, name):

 
    
def _int64_feature(value):
  return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

def _bytes_feature(value):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))  

def main():
    path_to_json = '/Users/Milap/Desktop/TargetCreator/generated/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    
    for index, js in enumerate(json_files):
        with open(os.path.join(path_to_json, js)) as json_file:
            json_text = json.load(json_file)
            alpha_color=json_text['alphanumeric_color']
            shape_color=json_text['background_color']
            shape=json_text['shape']
            alphanumeric=json_text['alphanumeric']
            image_name=json_text['image']
            image_path= path_to_json+image_name
            convert2TF(image_path,image_name,alpha_color)

if __name__ == '__main__':
    main()
   