""" To tick off checklist item A2

1) rpi takes photo
2) rpi sends photo to PC
3) PC verifies that photo has been sent
4) PC does imagerec
5) PC opens saved image
"""
import os

from PIL import Image
from pathlib import Path
import socket

from predict import predict


def get_exp_number_from_foldername(exp_name: str) -> int:
    """ Get the experiment number from the experiment name experiment names are: "exp", "exp2", "exp3", etc """
    int_string = exp_name[3:]
    if int_string == "":
        return 1
    else:
        return int(int_string)


def get_exp_number_from_folderpath(folderpath: Path) -> int:
    """ Get the experiment number from the experiment name experiment paths are: "exp", "exp2", "exp3", etc """
    return get_exp_number_from_foldername(folderpath.name)


def get_latest_exp_folder_from_detect(detectpath: Path) -> Path:
    """Get the latest exp folder. This is the exp with the largest integer label"""
    return sorted(detectpath.glob("exp*"), key=get_exp_number_from_folderpath)[-1]


def image_recognition():
    # in this step, the output dir of the saved images need to be returned
    predict(best_weight_path, images_source)


def open_photo(folder_path, image_filename):
    # check num photos in folder_path
    images_names = os.listdir(folder_path)
    print(len(images_names))

    if len(images_names) == 1:
        # read the image
        im = Image.open(image_filename)

        # show image
        im.show()
    else:
        # need to merge the images together
        im = Image.open(image_filename)
        im.show()


def get_photo(private_key_path, remote_file_loc, pc_file_loc):
    os.system(f'bash scp_file_transfer.sh {private_key_path} {remote_file_loc} {pc_file_loc}')


if __name__ == "__main__":
    runs_detect_folder = r'/Users/abc/yolov5/runs/detect'
    runs_detect_folder_path = Path(runs_detect_folder)
    latest_exp_folder = get_latest_exp_folder_from_detect(runs_detect_folder_path)
    open_photo(latest_exp_folder, r'/Users/abc/yolov5/runs/detect/exp19/w0011.jpg')

    # SOCKET STUFF
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM)  # AF_INET = IP, SOCKSTREAM = TCPserver.bind(('0.0.0.0', 1002))
    print("Starting server..")
    server.listen()

    client_socket, client_address = server.accept()  # Accepts client addrprint("Client addr: ", client_address, "Connected")

    file = open('server_image.jpg',
                "wb")  # returns streamimage_chunk = client_socket.recv(2048) #Receive 2048 bytewhile image_chunk: #While we have our image    file.write(image_chunk)
    image_chunk = client_socket.recv(2048)  # Receive 2048 bytefile.close()
    client_socket.close()

    private_key_path = r'/Users/abc/.ssh/id_rsa'
    get_photo(private_key_path, "abc", r'/Users/abc/Downloads/imagesFromRPI')

    runs_detect_folder = r'/Users/abc/yolov5/runs/detect'
    runs_detect_folder_path = Path(runs_detect_folder)
    latest_exp_folder = get_latest_exp_folder_from_detect(runs_detect_folder_path)
    open_photo(latest_exp_folder, r'/Users/abc/yolov5/runs/detect/exp19/w0011.jpg')

    # CONFIGURATIONS: remember to change
    use_prev = True
    # images_source = r'/Users/abc/Downloads/mdp_images'
    images_source = 'server_image.jpg'
    if use_prev:
        best_weight_filename = "best.pt"
    else:
        best_weight_filename = "best_13feb.pt"

    model_weights_folder = os.path.join(os.getcwd(), "weights")
    best_weight_path = os.path.join(model_weights_folder, best_weight_filename)
