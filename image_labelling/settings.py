import os
from enum import Enum


IMAGE_FORMAT_TYPES = [
    ('ase', 'ase'), ('art', 'art'), ('bmp', 'bmp'),
    ('blp', 'blp'), ('cd5', 'cd5'), ('cit', 'cit'),
    ('cpt', 'cpt'), ('cr2', 'cr2'), ('cut', 'cut'),
    ('dds', 'dds'), ('dib', 'dib'), ('djvu', 'djvu'),
    ('egt', 'egt'), ('exif', 'exif'), ('gif', 'gif'),
    ('gpl', 'gpl'), ('grf', 'grf'), ('icns', 'icns'),
    ('ico', 'ico'), ('iff', 'iff'), ('jng', 'jng'),
    ('jpeg', 'jpeg'), ('jpg', 'jpg'), ('jfif', 'jfif'),
    ('jp2', 'jp2'), ('jps', 'jps'), ('lbm', 'lbm'),
    ('max', 'max'), ('miff', 'miff'), ('mng', 'mng'),
    ('msp', 'msp'), ('nitf', 'nitf'), ('ota', 'ota'),
    ('pbm', 'pbm'), ('pc1', 'pc1'), ('pc2', 'pc2'),
    ('pc3', 'pc3'), ('pcf', 'pcf'), ('pcx', 'pcx'),
    ('pdn', 'pdn'), ('pgm', 'pgm'), ('PI1', 'PI1'),
    ('PI2', 'PI2'), ('PI3', 'PI3'), ('pict', 'pict'),
    ('pct', 'pct'), ('pnm', 'pnm'), ('pns', 'pns'),
    ('ppm', 'ppm'), ('psb', 'psb'), ('psd', 'psd'),
    ('pdd', 'pdd'), ('psp', 'psp'), ('px', 'px'),
    ('pxm', 'pxm'), ('pxr', 'pxr'), ('qfx', 'qfx'),
    ('raw', 'raw'), ('rle', 'rle'), ('sct', 'sct'),
    ('sgi', 'sgi'), ('rgb', 'rgb'), ('int', 'int'),
    ('bw', 'bw'), ('tga', 'tga'), ('tiff', 'tiff'),
    ('tif', 'tif'), ('vtf', 'vtf'), ('xbm', 'xbm'),
    ('xcf', 'xcf'), ('xpm', 'xpm'), ('3dv', '3dv'),
    ('amf', 'amf'), ('ai', 'ai'), ('awg', 'awg'),
    ('cgm', 'cgm'), ('cdr', 'cdr'), ('cmx', 'cmx'),
    ('dxf', 'dxf'), ('e2d', 'e2d'), ('egt', 'egt'),
    ('eps', 'eps'), ('fs', 'fs'), ('gbr', 'gbr'),
    ('odg', 'odg'), ('svg', 'svg'), ('stl', 'stl'),
    ('vrml', 'vrml'), ('x3d', 'x3d'), ('sxd', 'sxd'),
    ('v2d', 'v2d'), ('vnd', 'vnd'), ('wmf', 'wmf'),
    ('emf', 'emf'), ('art', 'art'), ('xar', 'xar'),
    ('png', 'png'), ('webp', 'webp'), ('jxr', 'jxr'),
    ('hdp', 'hdp'), ('wdp', 'wdp'), ('cur', 'cur'),
    ('ecw', 'ecw'), ('iff', 'iff'), ('lbm', 'lbm'),
    ('liff', 'liff'), ('nrrd', 'nrrd'), ('pam', 'pam'),
    ('pcx', 'pcx'), ('pgf', 'pgf'), ('sgi', 'sgi'),
    ('rgb', 'rgb'), ('rgba', 'rgba'), ('bw', 'bw'),
    ('int', 'int'), ('inta', 'inta'), ('sid', 'sid'),
    ('ras', 'ras'), ('sun', 'sun'), ('tga', 'tga')
]

TEMP_FILE_STORAGE_PATH = os.environ.get("TEMP_FILE_STORAGE_PATH", "/var/image_labelling")

STATUS_CHOICES = [
    ("all", "all"),
    ("active", "active"),
    ("inactive", "inactive")
]


class StatusMapper(Enum):
    all = None
    active = 1
    inactive = 0
