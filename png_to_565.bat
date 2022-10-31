set FFMPEG_PATH=E:\ffmpeg-5.1-full_build\bin\ffmpeg.exe

%FFMPEG_PATH% -vcodec png -i %1 -vcodec rawvideo -f rawvideo -pix_fmt rgb565 %2
