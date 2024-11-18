import os
import sys
import shutil
import ffmpeg

# import subprocess
from yt_dlp import YoutubeDL


print("""1. Change video format
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

    case 2:
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

    case 3:
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

    case 4:
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

    case 5:
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

    case 6:
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

    case 7:
        fileLocation = input(
            "Enter video filepath + extension (or just name and extension for cwd): "
        )
        downloadLink = input("Enter download link: ")
        fileName = os.path.basename(fileLocation)
        downloadPath = os.path.split(fileLocation)[0]

        ydl_options = {
            "format": "best",
            "outtmpl": "%(title)s.%(ext)s",
        }

        if (
            os.getcwd() == fileLocation
            or "/" not in fileLocation
            or "\\" not in fileLocation
        ):
            YoutubeDL(ydl_options).download([downloadLink])
            # subprocess.run(f"yt-dlp {downloadLink} -o {fileName}", shell=True)

        elif os.getcwd() != fileLocation:
            YoutubeDL(ydl_options).download([downloadLink])
            # subprocess.run(f"yt-dlp {downloadLink} -o {fileName}", shell=True)
            shutil.move(fileName, fileLocation)

    case 0:
        print("Exiting...")
        sys.exit()
