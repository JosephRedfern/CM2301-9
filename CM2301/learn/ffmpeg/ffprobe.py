import subprocess, json, pprint
class FFProbe(object):
    path = None
    bitrate = None
    format_name = None
    duration = None
    size = None
    
    streams = []
    
    
    def __init__(self, path):
        self.path = path
        output = subprocess.check_output(['/usr/local/bin/ffprobe', 
                                          self.path, 
                                          '-show_format', '-show_streams', 
                                          '-v', 'quiet', 
                                          '-print_format', 'json'])
        decoded = json.loads(output)
        for stream in decoded['streams']:
            self.streams.append(Stream.parse_ffprobe(stream))
        self._parse_format(decoded['format'])


    @property
    def video(self):
        for stream in self.streams:
            if stream.type == 'video':
                return stream

    @property
    def audio(self):
        for stream in self.streams:
            if stream.type == 'audio':
                return stream

    @property
    def height(self):
        return self.video.video_height

    @property
    def width(self):
        return self.video.video_width

    def _parse_format(self, dic):
        for key, value in dic.iteritems():
            if key == 'bit_rate':
                self.bitrate = int(value)
            if key == 'format_name':
                self.format_name = value
            if key == 'duration':
                self.duration = float(value)
            if key == 'size':
                self.size = long(value)
        pass
        
class Stream(object):
    
    def __init__(self):
        self.index = None
        self.type = None
        self.codec = None
        self.codec_desc = None
        self.duration = None
        self.video_width = None
        self.video_height = None
        self.video_fps = None
        self.audio_channels = None
        self.audio_samplerate = None
        
        
    @classmethod
    def parse_ffprobe(cls, dic):        
        stream = cls()
        
        for key, value in dic.iteritems():
            if key == 'index':
                stream.index = int(dic[key])
            elif key == 'codec_type':
                stream.type = dic[key]
            elif key == 'codec_name':
                stream.codec = dic[key]
            elif key == 'codec_long_name':
                stream.codec_desc = dic[key]
            elif key == 'duration':
                stream.duration = float(dic[key])
            elif key == 'width':
                stream.video_width = int(dic[key])
            elif key == 'height':
                stream.video_height = int(dic[key])
            elif key == 'r_frame_rate':
                stream.video_fps = dic[key]
            elif key == 'channels':
                stream.audio_channels = int(dic[key])
            elif key == 'sample_rate':
                stream.audio_samplerate = dic[key]

        return stream

    def __repr__(self):
        d = 'index:%s, type:%s, codec:%s' % (self.index, self.type, self.codec)
        return 'Stream(%s)' % d
        

        
        
probe = FFProbe('/Users/Charlie/Downloads/135628941.mp4')
        
    
