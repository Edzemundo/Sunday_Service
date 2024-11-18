import os
import sys
import shutil
import ffmpeg

# import subprocess
from yt_dlp import YoutubeDL

def menu():
    print("""
    1. Change video format
    2. Extract Audio
    3. Bind Audio
    4. Change Gain
    5. Trim Video
    6. Generate Thumbnails
    7. Download Video
    0. Exit
    """)
    command = int(input("Enter command: "))

    match command:
        case 1:
                change_video_format()
        case 2:
                extract_audio()
        case 3:
                bind_audio()
        case 4:
                change_gain()
        case 5:
                trim_video()
        case 6:
                generate_thumbnails()
        case 7:
                download_video()
        case 0:
                exit()



def change_video_format():
    """
    Change the format of a video file using ffmpeg.

    This function prompts the user for input and output file details,
    then uses ffmpeg to convert the video to the specified format.

    The function does not modify the video or audio codecs, only the container format.

    Returns:
        None
    """
    fileLocation = input("Enter input filepath + extension: ")
    fileExtensionInput = fileLocation.split(".")[-1]
    fileExtensionOutput = input("Enter container of output: ")
    if "." in fileExtensionOutput:
        fileExtensionOutput = fileExtensionOutput.replace(".", "")

    (
        ffmpeg.input(fileLocation)
        .output(
            f"{fileLocation.replace(f".{fileExtensionInput}", "."+fileExtensionOutput)}",
            vcodec="copy",
            acodec="copy",
        )
        .run(overwrite_output=True)
    )
    # subprocess.run(f"ffmpeg -i {fileLocation} {fileLocation.replace(f".{fileExtensionInput}", fileExtensionOutput)}", shell=True)


def extract_audio():
    """
    Extract audio from a video file using ffmpeg.

    This function prompts the user for input and output file details,
    then uses ffmpeg to extract the audio from the video file.

    The extracted audio is saved in PCM 32-bit floating-point little-endian format.

    Returns:
        None
    """
    fileInputLocation = input("Enter input filepath + extension: ")
    fileOutputName = input("Enter output filename + extension: ")

    (
        ffmpeg.input(fileInputLocation)
        .output(
            fileInputLocation.replace(
                os.path.basename(fileInputLocation), fileOutputName
            ),
            format=fileOutputName.split(".")[-1],
            acodec="pcm_f32le",
        )
        .run(overwrite_output=True)
    )
    # subprocess.run(f"ffmpeg -i {fileLocation} -vn -c:a pcm_f32le {fileOutputName}", shell=True)


def bind_audio():
    """
    Bind audio to a video file using ffmpeg.

    This function prompts the user for input video and audio file paths,
    as well as the desired output filename. It then uses ffmpeg to merge
    the audio from the specified audio file with the video, creating a new
    output file with the combined audio and video.

    The function uses the 'amerge' filter to combine the audio streams,
    and preserves the original video format.

    Returns:
        None
    """
    videoFileLocation = input("Enter input video filepath: ")
    audioFileLocation = input("Enter input audio filepath: ")
    fileOutputName = input("Enter output filename + extension: ")
    outputFormat = videoFileLocation.split(".")[-1]

    (
        ffmpeg.input(videoFileLocation)
        .input(audioFileLocation)
        .filter("amerge", inputs=2, outputs=1)
        .output(fileOutputName, format=outputFormat)
        .run(overwrite_output=True)
    )
    # subprocess.run(f"ffmpeg -i {videoFileLocation} -i {audioFileLocation} -filter_complex amerge -ac 2 -c:v copy {fileOutputName}", shell=True)


def change_gain():
    """
    Change the gain (volume) of an audio file using ffmpeg.

    This function prompts the user for input file details, desired gain value,
    and output file details. It then uses ffmpeg to adjust the volume of the
    audio file according to the specified gain value.

    The function converts the audio to PCM 32-bit floating-point little-endian format
    and applies the volume filter to adjust the gain.

    Parameters:
    None

    Returns:
    None

    Note:
    - The input filepath is obtained via user input.
    - The gain value (in dB) is obtained via user input and converted to float.
    - The output filename (including extension) is obtained via user input.
    """
    fileLocation = input("Enter input filepath: ")
    gainValue = float(input("Enter gain value (in dB): "))
    fileOutputName = input("Enter output filename + extension: ")

    (
        ffmpeg.input(fileLocation)
        .output(
            fileOutputName,
            acodec="pcm_f32le",
            afilter="volume=volume={}".format(gainValue),
        )
        .run(overwrite_output=True)
    )
    # subprocess.run(f"ffmpeg -i {fileLocation} -vn -c:a pcm_f32le -filter:a volume={gainValue} {fileOutputName}", shell=True)


def trim_video():
    """
    Trim a video file using ffmpeg.

    This function prompts the user for input file details, start and end times,
    and output file details. It then uses ffmpeg to trim the video according
    to the specified start and end times.

    The function does not modify the video or audio codecs, only trims the duration.

    Parameters:
    None

    Returns:
    None

    Note:
    - The input filepath is obtained via user input.
    - The start time is obtained via user input in the format xx:xx:xx.xxx.
      If left blank, it defaults to 00:00:00.000.
    - The end time is obtained via user input in the format xx:xx:xx.xxx.
    - The output filename (including extension) is obtained via user input.
    """
    fileLocation = input("Enter input filepath + extension: ")
    startTime = input(
        "Enter start time in seconds (format=xx:xx:xx.xxx, default = 00:00:00.000): "
    )
    endTime = input("Enter end time in seconds (format=xx:xx:xx.xxx): ")
    fileOutputName = input("Enter output filename + extension: ")

    if not startTime:
        startTime = "00:00:00.000"

    (
        ffmpeg.input(fileLocation, ss=startTime)
        .output(
            fileLocation.replace(os.path.basename(fileLocation), fileOutputName),
            t=endTime,
        )
        .run(overwrite_output=True)
    )
    # subprocess.run(f"ffmpeg -i {fileLocation} -ss {startTime} -t {endTime} {fileOutputName}", shell=True)


def generate_thumbnails():
    """
    Generate a thumbnail from a video file using ffmpeg.

    This function prompts the user for input video file details, timestamp for the thumbnail,
    and desired thumbnail size. It then uses ffmpeg to generate a PNG thumbnail from the
    specified video at the given timestamp.

    Parameters:
    None

    Returns:
    None

    Note:
    - The input video filepath is obtained via user input.
    - The timestamp for the thumbnail is obtained via user input in the format xx:xx:xx.xxx.
    - The thumbnail size is obtained via user input in the format widthxheight.
      If left blank, it defaults to '720p'.
    - The generated thumbnail is saved in the same directory as the input video
      with the filename 'thumbnail_001.png'.
    """
    fileLocation = input("Enter input video filepath: ")
    timeStamp = input("Enter time to generate thumbnail (format=xx:xx:xx.xxx): ")
    thumbnailSize = input(
        "Enter thumbnail size (format = widthxheight, default = 720p): "
    )

    if not thumbnailSize:
        thumbnailSize = "720p"

    # Create output directory if it doesn't exist
    # if not os.path.exists(outputDirectory):
    #     os.makedirs(outputDirectory)

    # Generate thumbnails
    (
        ffmpeg.input(fileLocation, ss=timeStamp)
        .output(
            os.path.join(os.path.split(fileLocation)[0], "thumbnail_%03d.png"),
            vframes=1,
            vcodec="png",
        )
        .run(overwrite_output=True)
    )
    # subprocess.run(f"ffmpeg -i {fileLocation} -vf thumbnail,scale={thumbnailSize} -r {thumbnailCount} {outputDirectory}/thumbnail_%03d.jpg", shell=True)


def download_video():
    """
    Download a video from a given URL using YouTube-DL.

    This function prompts the user for a download location and a download link.
    It then uses YouTube-DL to download the video in the best available format.
    If a custom download location is provided, the video is moved there after download.

    Parameters:
    None

    Returns:
    None

    Note:
    - The download location is obtained via user input. If left blank, the current working directory is used.
    - The download link is obtained via user input.
    - The video is downloaded in the best available format.
    - The output template for the downloaded file is set to "%(title)s.%(ext)s".
    """
    fileLocation = input("Enter video download location (leave blank for CWD): ")
    downloadLink = input("Enter download link: ")

    ydl_options = {
        "format": "best",
        "outtmpl": "%(title)s.%(ext)s",
    }

    if os.getcwd() == fileLocation or len(fileLocation) == 0:
        YoutubeDL(ydl_options).download([downloadLink])
        # subprocess.run(f"yt-dlp {downloadLink} -o {fileName}", shell=True)

    else:
        with YoutubeDL(ydl_options) as ydl:
            YoutubeDL(ydl_options).download([downloadLink])
            # subprocess.run(f"yt-dlp {downloadLink} -o {fileName}", shell=True)
            video_filename = ydl.prepare_filename(
                ydl.extract_info(downloadLink, download=False)
            )
            shutil.move(f"{video_filename}", f"{fileLocation}")

def exit():
    """
    Exits.
    
    This function exits the program.
    
    Parameters:
    None. Cuz you're exiting.
    
    Returns:
    None. Cuz you've exited.
    
    Note:
    - Bye-bye for now.
    
    """
    print("Exiting...")
    sys.exit()


if __name__ == "__main__":
    while True:
        menu()