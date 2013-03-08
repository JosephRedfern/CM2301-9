import os, re, subprocess, threading
from ffprobe import *

class FFMpegException(Exception):
    pass

class Converter(object):
    input_file = None
    output_file = None
    ffmpeg_path = None
    container = None
    video_codec = None
    audio_codec = None
    _progress = 0
    is_started = False
    completed = False
    _process = None
    _length = None
    _height = None
    _width = None
    _dimensions = {}

    def __init__(self, input_path, output_path, ffmpeg_path=None):
        """
        Converter constructer, must be initialized with input path video.
        """
        if not ffmpeg_path:
            path = '/usr/local/bin/ffmpeg'
        else:
            path = ffmpeg_path
        if os.path.exists(path):
            self.ffmpeg_path = path
        else:
            raise FFMpegException('ffmpeg binary not found: %s' % (path))
        
        if os.path.exists(input_path):
            self.input_file = input_path
        else:
            raise FFMpegException('Input file does not exist: %s' % (input_path))
        
        self.output_file = output_path

    def set_container(self, container):
        """
        Sets the container format. e.g mp4
        """
        self.container = container

    def set_video_codec(self, video_codec):
        """
        Sets the output video codec.
        
        @param VideoCodec The constant codec 
        """
        self.video_codec = video_codec

    def set_audio_codec(self, audio_codec):
        """
        Set the output audio codec.
        
        @param VideoCodec The codec to be used.
        """
        self.audio_codec = audio_codec
        
    def set_dimensions(self, height=None, width=None):
        """
        Sets either the height, width or both for the encoding.
        
        If using certain VideoCodec then neither of these should be an odd number.
        
        @param height The height in pixels.
        @param width The width in pixels.  
        """
        if height == None and width == None:
             raise TypeError("No dimensions given")
        else:
             self._dimensions = {'width': width, 'height': height}
         

    def start(self):
        """
        Starts the current conversion task the background.
        """
        print ' '.join(self._parse_options())
        thread = threading.Thread(target=self.__conversion)
        thread.start()
        
    def _wait(self):
        self._process.wait()
        self.completed = True
        self.is_started = False
        print "Conversion Completed"

    def cancel(self):
        """
        Cancels the current conversion task.
        """
        if self.is_started:
            self._process.kill()
            self._process = None
            self.is_started = False
            self._progress = 0
            
        else:
            raise FFMpegException('No conversion to kill')
        

    def __to_decimal(self, hms):
        """
        Converts the supplied [h,m,s] list to
        decimal seconds.
        
        @param list List of hms
        returns float Returns total seconds. 
        """
        h = float(hms[0]) * 3600
        m = float(hms[1]) * 60
        s = float(hms[2])
        return h+m+s

    def get_duration(self):
        """
        Returns the duration of the video in seconds as a decimal.
        
        May be better to use FFProbe.
        """
        p = subprocess.Popen(['/usr/local/bin/ffmpeg', '-i', self.input_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = p.stderr.read()
        regex = re.compile('Duration: (\d\d):(\d\d):(\d\d(\.\d\d)?)')
        tmp = regex.findall(output)
        return self.__to_decimal(tmp[0])

    def __conversion(self):
        """
        This method is run by the thread, it executes the ffmpeg process
        and captures the output.
        """
        self.is_started = True
        self._length = self.get_duration()
        self._process = subprocess.Popen(self._parse_options(),
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE)
        thread = threading.Thread(target=self._wait)
        thread.start()

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
                try:
                    parts = tmp[0].split(':')
                except IndexError:
                    self.completed = True
                    return
                progress = self.__to_decimal(parts)
                percent = (progress/self._length)*100
                self._progress = round(percent, 2)
                if progress >= self._length:
                    self.completed = True 
                elif self._progress > 100:
                    self.completed = True
                
                
    def _parse_options(self):
        """
        Checks the current config for the encoding and outputs the 
        correct commands for ffmpeg.
        """
        self._scale()
        video = []
        
        width = self._width
        height = self._height
        
        print (width, height, 'dfsdf')
        
        if self.container is ContainerFormat.WEBM:
            print (self._width, self._height)
            video = ['-codec:v', VideoCodec.VP8, 
                    '-r', '25',
                    '-quality', 'good', 
                    '-cpu-used', '0',
                    '-b:v', '1000k',
                    '-qmin', '10',
                    '-qmax', '42',
                    '-vf', 'scale=' + str(width) + ':' + str(height),
                    '-pix_fmt', 'yuv420p',
                    '-threads', '0',
                    ]
        elif self.container is ContainerFormat.MP4:
            print (self._width, self._height)
            video = ['-codec:v', VideoCodec.H264,
                    '-profile:v', 'baseline',
                    '-r', '25',
                    '-preset', 'slow',
                    '-b:v', '1000k',
                    '-maxrate', '1000k',
                    '-bufsize', '1200k',
                    '-vf', 'scale=' + str(width) + ':' + str(height),
                    '-pix_fmt', 'yuv420p',
                    '-threads', '0',
                    ]
            
        audio = ['-codec:a', self.audio_codec,
                 '-b:a', '128k'
                 ]
        
        cmds = [self.ffmpeg_path, '-i', self.input_file] + video + audio + ['-y', self.output_file]
        return cmds
    
    
    def _scale(self):
        probe = self.probe
        self._width = probe.video.width
        self._height = probe.video.height
        
        if self._width % 2:
            self._width = self._width - 1
            
        if self._height % 2:
            self._height = self._height - 1
            
        print 'run'
        
        #ratio = MIN( maxWidth / width, maxHeight/ height )
        #height = ratio * height
        #width = ratio * width
        

    @property
    def progress(self):
        """
        The current progress of the encoding, as a percentage.
        
        @return float The progress ffmpeg as a percentage.
        """
        if (self._progress is None
            and self.is_started is False):
            raise FFMpegException("Conversion not started")
        else:
            return self._progress
        
    @property
    def probe(self):
        """
        Returns information about the current file using ffprobe.
        @return FFProbe Returns an ffprobe for the current file.
        """
        return FFProbe(self.input_file)

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
    VP8 = 'libvpx'
    H263 = 'h263'
    DIVX = 'mpeg4'
    
class AudioCodec(object):
    """
    Collection of audio codecs for ffmpeg.
    """
    AAC = 'libfaac'
    VORBIS = 'libvorbis'
    MP3 = 'libmp3lame'
    MP2 = 'MP2'
    
