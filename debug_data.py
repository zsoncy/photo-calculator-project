import tensorflow as tf
import numpy as np
import cv2
import os
from ml.data_symbols import load_symbols_from_folders


def visualize_training_data():
    print("Visualizing what the machine sees...")

    # Loading own symbols using the EXACT same logic as training
    ds, class_names = load_symbols_from_folders("data/symbols", (28, 28), batch_size=32)

    # Grab one batch of images
    for images, labels in ds.take(1):

        # Create a big canvas to stack them
        rows = []
        row_images = []

        print(f"Displaying {len(images)} sample images...")

        for i in range(min(16, len(images))):  # Show top 16
            img = images[i].numpy()
            label = labels[i].numpy()
            name = class_names[label]

            # Scale up to 0-255
            img_display = (img * 255).astype(np.uint8)

            # If shape is (28,28,1), remove the last dim for OpenCV
            if img_display.shape[-1] == 1:
                img_display = img_display[:, :, 0]

            # Resize for easier viewing (zoom in)
            img_display = cv2.resize(img_display, (100, 100), interpolation=cv2.INTER_NEAREST)

            # Add text label
            cv2.putText(img_display, str(name), (5, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (127), 1)
            cv2.rectangle(img_display, (0, 0), (100, 100), (255), 1)

            row_images.append(img_display)
            if len(row_images) == 4:
                rows.append(np.hstack(row_images))
                row_images = []

        if row_images:  # Append remaining
            rows.append(np.hstack(row_images))

        # Combine all rows
        final_grid = np.vstack(rows[:4])  # Limit to 4 rows

        filename = "debug_what_ai_sees.png"
        cv2.imwrite(filename, final_grid)
        print(f"Saved snapshot to: {os.path.abspath(filename)}")


if __name__ == "__main__":
    visualize_training_data()