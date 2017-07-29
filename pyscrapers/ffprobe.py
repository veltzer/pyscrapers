import json
import subprocess

"""
This is a module that returns information about video streams based on running ffprobe
as a subprocess.

References:
- http://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python/3844467
"""


def probe(vid_file_path):
    """ Give a json from ffprobe command line

    @vid_file_path : The absolute (full) path of the video file, string.
    """
    if type(vid_file_path) != str:
        raise Exception('Give ffprobe a full file path of the video')

    args = [
        "ffprobe",
        "-loglevel",
        "quiet",
        "-print_format",
        "json",
        # "-show_format",
        "-show_streams",
        "-select_streams",
        "v",
        vid_file_path,
    ]
    return json.loads(subprocess.check_output(args).decode())


def width(vid):
    _json = probe(vid)
    return int(_json["streams"][0]["width"])


def height(vid):
    _json = probe(vid)
    return int(_json["streams"][0]["height"])


def duration(vid_file_path):
    """ Video's duration in seconds, return a float number
    """
    _json = probe(vid_file_path)

    if 'format' in _json:
        if 'duration' in _json['format']:
            return float(_json['format']['duration'])

    if 'streams' in _json:
        # commonly stream 0 is the video
        for s in _json['streams']:
            if 'duration' in s:
                return float(s['duration'])

    # if everything didn't happen,
    # we got here because no single 'return' in the above happen.
    raise Exception('I found no duration')
