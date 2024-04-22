import cv2
import tensorflow as tf
import numpy as np


class custom_feature_extractor(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(custom_feature_extractor, self).__init__(**kwargs)

    def build(self, input_shape):
        self.conv1 = tf.keras.layers.Conv2D(16, (3, 3), padding='same', activation='relu', input_shape=(224, 224, 3))
        self.maxpool1 = tf.keras.layers.MaxPooling2D((3, 3))
        self.batch_norm1 = tf.keras.layers.BatchNormalization(axis=-1)
        self.dropout1 = tf.keras.layers.Dropout(0.25)
        self.conv2 = tf.keras.layers.Conv2D(32, (3, 3), padding='same', activation='relu')
        self.maxpool2 = tf.keras.layers.MaxPooling2D((2, 2))
        self.batch_norm2 = tf.keras.layers.BatchNormalization(axis=-1)
        self.dropout2 = tf.keras.layers.Dropout(0.25)
        self.conv3 = tf.keras.layers.Conv2D(32, (3, 3), padding='same', activation='relu')
        self.batch_norm3 = tf.keras.layers.BatchNormalization(axis=-1)
        self.maxpool3 = tf.keras.layers.MaxPooling2D((2, 2))
        self.dropout3 = tf.keras.layers.Dropout(0.25)
        self.flatten = tf.keras.layers.Flatten()

    def call(self, img):
        x = self.conv1(img)
        x = self.batch_norm1(x)
        x = self.maxpool1(x)
        x = self.dropout1(x)
        x = self.conv2(x)
        x = self.batch_norm2(x)
        x = self.maxpool2(x)
        x = self.dropout2(x)
        x = self.conv3(x)
        x = self.batch_norm3(x)
        x = self.maxpool3(x)
        x = self.dropout3(x)
        x = self.flatten(x)
        return x

    def set_trainable(self, trainable):
        layers_to_train = [self.conv1, self.maxpool1, self.batch_norm1, self.conv2, self.maxpool2, self.batch_norm2,
                           self.conv3, self.batch_norm3, self.maxpool3]
        for layer in layers_to_train:
            layer.trainable = trainable


with tf.device('/GPU:0'):
    age_model = tf.keras.Sequential([
        custom_feature_extractor(),
        tf.keras.layers.Dense(1024, activation='relu'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1024, activation='relu'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.55),
        tf.keras.layers.Dense(1024, activation='relu'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.55),
        tf.keras.layers.Dense(8, activation='softmax')
    ])

    gender_model = tf.keras.Sequential([
        custom_feature_extractor(),
        tf.keras.layers.Dense(1024, activation='relu'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1024, activation='relu'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1024, activation='relu'),
        tf.keras.layers.Flatten(),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(2, activation='softmax')
    ])

input_shape = (None, 224, 224, 3)
age_model.build(input_shape)
gender_model.build(input_shape)
age_model.summary()
gender_model.summary()
age_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
gender_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
for layer in age_model.layers[0:]:
    layer.trainable = False

for layer in gender_model.layers[0:]:
    layer.trainable = False
age_model.load_weights("weights/age_model.h5")
gender_model.load_weights("weights/gender_model.h5")
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
reverse_gender_label = {0: 'm', 1: 'f'}
reverse_age_label = {
    0: '0-2',
    1: '4-6',
    2: '8-13',
    3: '15-20',
    4: '25-32',
    5: '38-43',
    6: '48-53',
    7: '60+'
}
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face_roi = frame[y:y + h, x:x + w]
        resized_face = cv2.resize(face_roi, (224, 224))
        resized_face = np.expand_dims(resized_face, axis=0)
        predicted_age = age_model.predict(resized_face)
        predicted_age = np.argmax(predicted_age, axis=1)
        predicted_age_label = reverse_age_label[predicted_age[0]]
        predicted_gender = gender_model.predict(resized_face)
        predicted_gender = np.argmax(predicted_gender, axis=1)
        predicted_gender_label = reverse_gender_label[predicted_gender[0]]
        cv2.putText(frame, f'Age: {predicted_age_label}, Gender: {predicted_gender_label}', (x, y - 10), cv2.FONT_HERSHEY_COMPLEX,
                    0.7, (0, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Face Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
