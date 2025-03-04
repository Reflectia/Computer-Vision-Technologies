from tensorflow.keras.preprocessing.image import ImageDataGenerator
import cv2
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Define image size and batch size
IMG_SIZE = (128, 128)
BATCH_SIZE = 32


def preprocess_image(image):
    # Check if the image is already in grayscale
    if len(image.shape) == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Resize image
    resized_image = cv2.resize(image, IMG_SIZE)
    return resized_image.reshape(IMG_SIZE + (1,))


# Define a generator with preprocessing
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    validation_split=0.2,
    preprocessing_function=preprocess_image
)

# Load training and validation data
train_generator = train_datagen.flow_from_directory(
    'Eye dataset',
    target_size=IMG_SIZE,
    color_mode='grayscale',
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    'Eye dataset',
    target_size=IMG_SIZE,
    color_mode='grayscale',
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='validation'
)

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE[0], IMG_SIZE[1], 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(
    train_generator,
    epochs=10,
    validation_data=validation_generator
)

# Plot training & validation accuracy values
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')

# Plot training & validation loss values
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')

plt.show()


# Get a batch of images and labels from the validation set
images, labels = next(validation_generator)

# Make predictions on the batch
predictions = (model.predict(images) > 0.5).astype("int32")


# Function to plot images with predictions
def plot_predictions(images, true_labels, predictions, num=10):
    plt.figure(figsize=(20, 10))
    for i in range(num):
        image = images[i]
        true_label = true_labels[i]
        prediction = predictions[i]

        plt.subplot(2, num // 2, i + 1)
        plt.imshow(image.squeeze(), cmap='gray')
        plt.title(
            f"True: {'close' if true_label == 0 else 'forward'}\nPred: {'close' if prediction == 0 else 'forward'}")
        plt.axis('off')

    plt.tight_layout()
    plt.show()


# Visualize predictions on a few images
plot_predictions(images, labels, predictions, num=10)
