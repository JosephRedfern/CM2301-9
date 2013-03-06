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
        return self.video.height

    @property
    def width(self):
        return self.video.width

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
        
        if 'index' in dic:
            stream.index = int(dic['index'])
            
        if 'width' in dic:
            stream.width = int(dic['width'])
        
        if 'height' in dic:
            stream.height = int(dic['height'])
            
        if 'codec_type' in dic:
            stream.type = dic['codec_type']
            
        if 'codec_name' in dic:
            stream.codec = dic['codec_name']
            
        if 'codec_long_name' in dic:
            stream.codec_desc = dic['codec_long_name']
            
        if 'duration' in dic:
            stream.duration = float(dic['duration'])
            
        if 'r_frame_rate' in dic:
            stream.video_fps = dic['r_frame_rate']
            
        if 'channels' in dic:
            stream.audio_channels = int(dic['channels'])
            
        if 'sample_rate' in dic:
            stream.audio_samplerate = int(dic['sample_rate'])

        return stream

    def __repr__(self):
        d = 'index:%s, type:%s, codec:%s' % (self.index, self.type, self.codec)
        return 'Stream(%s)' % d
        
        
    
