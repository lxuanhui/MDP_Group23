from PIL import Image


def tile_images(image_paths):
    # Load all images
    images = [Image.open(path) for path in image_paths]
    # Determine the number of rows and columns
    num_images = len(images)
    num_cols = 2 if num_images > 4 else 1
    num_rows = (num_images + num_cols - 1) // num_cols
    # Calculate the width and height of the tiled image
    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)
    tiled_width = max_width * num_cols
    tiled_height = max_height * num_rows
    # Create the tiled image
    tiled_image = Image.new('RGB', (tiled_width, tiled_height))
    # Paste each image into the tiled image
    for i, img in enumerate(images):
        col_idx = i % num_cols
        row_idx = i // num_cols
        x = col_idx * max_width
        y = row_idx * max_height
        tiled_image.paste(img, (x, y))
    return tiled_image


if __name__ == "__main__":
    image_paths = ['/Users/abc/yolov5/runs/detect/exp152/image0.jpg', '/Users/abc/yolov5/runs/detect/exp153/image0.jpg',
                   '/Users/abc/yolov5/runs/detect/exp154/image0.jpg'] # , '/Users/abc/yolov5/runs/detect/exp155/image0.jpg',
                   # '/Users/abc/yolov5/runs/detect/exp156/image0.jpg', '/Users/abc/yolov5/runs/detect/exp158/image0.jpg',
                   # '/Users/abc/yolov5/runs/detect/exp159/image0.jpg', '/Users/abc/yolov5/runs/detect/exp160/image0.jpg']
    tiled_image = tile_images(image_paths)
    tiled_image.show()  # displays the tiled image

    # image_paths = ['/Users/abc/yolov5/runs/detect/exp102/image0.jpg', '/Users/abc/yolov5/runs/detect/exp103/image0.jpg',
    #                '/Users/abc/yolov5/runs/detect/exp104/image0.jpg', '/Users/abc/yolov5/runs/detect/exp105/image0.jpg',
    #                '/Users/abc/yolov5/runs/detect/exp106/image0.jpg', '/Users/abc/yolov5/runs/detect/exp107/image0.jpg',
    #                '/Users/abc/yolov5/runs/detect/exp108/image0.jpg', '/Users/abc/yolov5/runs/detect/exp109/image0.jpg'
    #                ]
    # tiled_image = tile_images(image_paths)
    # tiled_image.show()  # displays the tiled image
    #
    # image_paths = ['/Users/abc/yolov5/runs/detect/exp102/image0.jpg', '/Users/abc/yolov5/runs/detect/exp103/image0.jpg',
    #                '/Users/abc/yolov5/runs/detect/exp104/image0.jpg', '/Users/abc/yolov5/runs/detect/exp105/image0.jpg',
    #                '/Users/abc/yolov5/runs/detect/exp106/image0.jpg', '/Users/abc/yolov5/runs/detect/exp107/image0.jpg',
    #                '/Users/abc/yolov5/runs/detect/exp108/image0.jpg' #, '/Users/abc/yolov5/runs/detect/exp109/image0.jpg'
    #                ]
    # tiled_image = tile_images(image_paths)
    # tiled_image.show()  # displays the tiled image
