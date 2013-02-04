import os, re, subprocess, threading

class FFMpegException(Exception):
    pass

class Converter(object):
    input_file = None
    output_file = None
    ffmpeg_path = None
    container = None
    video_format = None
    audio_format = None
    _progress = None
    _is_started = False
    _process = None
    _length = None

    def __init__(self, ffmpeg_path=None):
        if not ffmpeg_path:
            path = '/usr/local/bin/ffmpeg'
        else:
            path = ffmpeg_path
        if os.path.exists(path):
            self.ffmpeg_path = path
        else:
            raise FFMpegException('ffmpeg binary not found: %s' % (path))
        

    def set_input(self, path):
        if not os.path.exists(path):
            raise FFMpegException('Input file not found at path: %s' % (path))
        self.input_file = path

    def set_container(self, container):
        self.container = container

    def set_video_format(self, video_format):
        self.video_format = video_format

    def set_audio_format(self, audio_format):
        self.audio_format = audio_format

    def set_output(self, path):
        self.output_file = path

    def start_conversion(self):
        thread = threading.Thread(target=self.__conversion)
        thread.start()

    def cancel_conversion(self):
        self._process.kill()

    def __to_decimal(self, hms):
        h = float(hms[0]) * 3600
        m = float(hms[1]) * 60
        s = float(hms[2])
        return h+m+s

    def get_duration(self):
        p = subprocess.Popen(['/usr/local/bin/ffmpeg', '-i', self.input_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = p.stderr.read()
        regex = re.compile('Duration: (\d\d):(\d\d):(\d\d(\.\d\d)?)')
        tmp = regex.findall(output)
        return self.__to_decimal(tmp[0])

    def __conversion(self):
        self._is_started = True
        self._length = self.get_duration()
        self._process = subprocess.Popen([self.ffmpeg_path,                                         
                            '-i', self.input_file,
                            '-vcodec', self.video_format,
                            '-vprofile', 'high',
                            '-preset', 'slow', '-b:v', '500k', '-maxrate',
                            '500k', '-bufsize', '1000k', '-vf', 'scale=-1',
                            '-threads', '0',
                            '-acodec', self.audio_format,
                            '-b:a', '128k',
                            '-strict', '-2',
                            '-y', self.output_file],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        buf = ''
        total_output = ''
        pat = re.compile(r'time=([0-9.:]+) ')

        while True:
            fd = self._process.stderr
            ret = fd.read(10)

            if not ret:
                break

            total_output += ret
            buf += ret

            if '\r' in buf:
                line, buf = buf.split('\r', 1)
                tmp = pat.findall(line)
                parts = tmp[0].split(':')
                progress = self.__to_decimal(parts)
                percent = (progress/self._length)*100
                self._progress = round(percent, 2)
        

    @property
    def progress(self):
        if (self._progress is None
            and self._is_started is False):
            raise FFMpegException("Conversion not started")
        else:
            return self._progress


class FFProbe(object):
    pass


class ContainerFormat(object):
    """
    Container format class
    """
    OGG = 'ogg'
    AVI = 'avi'
    MKV = 'matroska'
    WEBM = 'webm'
    FLV = 'flv'
    MOV = 'mov'
    MP4 = 'mp4'

class VideoCodec(object):
    """
    Collection of VideoCodec for ffmpeg.
    """
    THEORA = 'libtheora'
    H264 = 'libx264'
    FLV = 'flv'
    VP8 = 'vp8'
    H263 = 'h263'
    DIVX = 'mpeg4'


c = Converter()
c.set_input('/Users/Charlie/Downloads/211653.flv')
c.set_output('/Users/Charlie/Downloads/output.mp4')
c.set_video_format(VideoCodec.H264)
c.set_audio_format('aac')
