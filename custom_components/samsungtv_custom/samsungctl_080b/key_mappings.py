# -*- coding: utf-8 -*-


class SendButtonCls(object):

    def __init__(self, key, group, description):
        self.key = key
        self.group = group
        self.description = description

    def __call__(self, remote):
        remote.control(self.key)

    def __str__(self):
        if self.description != self.key:

            return '        {0}:{1}{2}'.format(
                self.key,
                ' ' * (35 - len(self.key)),
                self.description
            )

        else:
            return '        {0}'.format(self.key)


KEY_MAPPINGS = (
    ('Power Keys ', (
        ('Power OFF',                        'KEY_POWEROFF'),
        ('Power On',                         'KEY_POWERON'),
        ('Power Toggle',                     'KEY_POWER')
    )),
    ('Input Keys ', (
        ('Source',                           'KEY_SOURCE'),
        ('Component 1',                      'KEY_COMPONENT1'),
        ('Component 2',                      'KEY_COMPONENT2'),
        ('AV 1',                             'KEY_AV1'),
        ('AV 2',                             'KEY_AV2'),
        ('AV 3',                             'KEY_AV3'),
        ('S Video 1',                        'KEY_SVIDEO1'),
        ('S Video 2',                        'KEY_SVIDEO2'),
        ('S Video 3',                        'KEY_SVIDEO3'),
        ('HDMI',                             'KEY_HDMI'),
        ('HDMI 1',                           'KEY_HDMI1'),
        ('HDMI 2',                           'KEY_HDMI2'),
        ('HDMI 3',                           'KEY_HDMI3'),
        ('HDMI 4',                           'KEY_HDMI4'),
        ('FM Radio',                         'KEY_FM_RADIO'),
        ('DVI',                              'KEY_DVI'),
        ('DVR',                              'KEY_DVR'),
        ('TV',                               'KEY_TV'),
        ('Analog TV',                        'KEY_ANTENA'),
        ('Digital TV',                       'KEY_DTV')
    )),
    ('Number Keys ', (
        ('Key1',                             'KEY_1'),
        ('Key2',                             'KEY_2'),
        ('Key3',                             'KEY_3'),
        ('Key4',                             'KEY_4'),
        ('Key5',                             'KEY_5'),
        ('Key6',                             'KEY_6'),
        ('Key7',                             'KEY_7'),
        ('Key8',                             'KEY_8'),
        ('Key9',                             'KEY_9'),
        ('Key0',                             'KEY_0')
    )),
    ('Misc Keys ', (
        ('3D',                               'KEY_PANNEL_CHDOWN'),
        ('AnyNet+',                          'KEY_ANYNET'),
        ('Energy Saving',                    'KEY_ESAVING'),
        ('Sleep Timer',                      'KEY_SLEEP'),
        ('DTV Signal',                       'KEY_DTV_SIGNAL')
    )),
    ('Channel Keys ', (
        ('Channel Up',                       'KEY_CHUP'),
        ('Channel Down',                     'KEY_CHDOWN'),
        ('Previous Channel',                 'KEY_PRECH'),
        ('Favorite Channels',                'KEY_FAVCH'),
        ('Channel List',                     'KEY_CH_LIST'),
        ('Auto Program',                     'KEY_AUTO_PROGRAM'),
        ('Magic Channel',                    'KEY_MAGIC_CHANNEL'),
    )),
    ('Volume Keys ', (
        ('Volume Up',                        'KEY_VOLUP'),
        ('Volume Down',                      'KEY_VOLDOWN'),
        ('Mute',                             'KEY_MUTE')
    )),
    ('Direction Keys ', (
        ('Navigation Up',                    'KEY_UP'),
        ('Navigation Down',                  'KEY_DOWN'),
        ('Navigation Left',                  'KEY_LEFT'),
        ('Navigation Right',                 'KEY_RIGHT'),
        ('Navigation Return/Back',           'KEY_RETURN'),
        ('Navigation Enter',                 'KEY_ENTER')
    )),
    ('Media Keys ', (
        ('Rewind',                           'KEY_REWIND'),
        ('Stop',                             'KEY_STOP'),
        ('Play',                             'KEY_PLAY'),
        ('Fast Forward',                     'KEY_FF'),
        ('Record',                           'KEY_REC'),
        ('Pause',                            'KEY_PAUSE'),
        ('Live',                             'KEY_LIVE'),
        ('fnKEY_QUICK_REPLAY',               'KEY_QUICK_REPLAY'),
        ('fnKEY_STILL_PICTURE',              'KEY_STILL_PICTURE'),
        ('fnKEY_INSTANT_REPLAY',             'KEY_INSTANT_REPLAY')
    )),
    ('Picture in Picture ', (
        ('PIP On/Off',                       'KEY_PIP_ONOFF'),
        ('PIP Swap',                         'KEY_PIP_SWAP'),
        ('PIP Size',                         'KEY_PIP_SIZE'),
        ('PIP Channel Up',                   'KEY_PIP_CHUP'),
        ('PIP Channel Down',                 'KEY_PIP_CHDOWN'),
        ('PIP Small',                        'KEY_AUTO_ARC_PIP_SMALL'),
        ('PIP Wide',                         'KEY_AUTO_ARC_PIP_WIDE'),
        ('PIP Bottom Right',                 'KEY_AUTO_ARC_PIP_RIGHT_BOTTOM'),
        ('PIP Source Change',                'KEY_AUTO_ARC_PIP_SOURCE_CHANGE'),
        ('PIP Scan',                         'KEY_PIP_SCAN')
    )),
    ('Modes ', (
        ('VCR Mode',                         'KEY_VCR_MODE'),
        ('CATV Mode',                        'KEY_CATV_MODE'),
        ('DSS Mode',                         'KEY_DSS_MODE'),
        ('TV Mode',                          'KEY_TV_MODE'),
        ('DVD Mode',                         'KEY_DVD_MODE'),
        ('STB Mode',                         'KEY_STB_MODE'),
        ('PC Mode',                          'KEY_PCMODE')
    )),
    ('Color Keys ', (
        ('Green',                            'KEY_GREEN'),
        ('Yellow',                           'KEY_YELLOW'),
        ('Cyan',                             'KEY_CYAN'),
        ('Red',                              'KEY_RED')
    )),
    ('Teletext ', (
        ('Teletext Mix',                     'KEY_TTX_MIX'),
        ('Teletext Subface',                 'KEY_TTX_SUBFACE')
    )),
    ('Aspect Ratio ', (
        ('Aspect Ratio',                     'KEY_ASPECT'),
        ('Picture Size',                     'KEY_PICTURE_SIZE'),
        ('Aspect Ratio 4:3',                 'KEY_4_3'),
        ('Aspect Ratio 16:9',                'KEY_16_9'),
        ('Aspect Ratio 3:4 (Alt)',           'KEY_EXT14'),
        ('Aspect Ratio 16:9 (Alt)',          'KEY_EXT15')
    )),
    ('Picture Mode ', (
        ('Picture Mode',                     'KEY_PMODE'),
        ('Picture Mode Panorama',            'KEY_PANORAMA'),
        ('Picture Mode Dynamic',             'KEY_DYNAMIC'),
        ('Picture Mode Standard',            'KEY_STANDARD'),
        ('Picture Mode Movie',               'KEY_MOVIE1'),
        ('Picture Mode Game',                'KEY_GAME'),
        ('Picture Mode Custom',              'KEY_CUSTOM'),
        ('Picture Mode Movie (Alt)',         'KEY_EXT9'),
        ('Picture Mode Standard (Alt)',      'KEY_EXT10')
    )),
    ('Menus ', (
        ('Menu',                             'KEY_MENU'),
        ('Top Menu',                         'KEY_TOPMENU'),
        ('Tools',                            'KEY_TOOLS'),
        ('Home',                             'KEY_HOME'),
        ('Contents',                         'KEY_CONTENTS'),
        ('Guide',                            'KEY_GUIDE'),
        ('Disc Menu',                        'KEY_DISC_MENU'),
        ('DVR Menu',                         'KEY_DVR_MENU'),
        ('Help',                             'KEY_HELP')
    )),
    ('OSD ', (
        ('Info',                             'KEY_INFO'),
        ('Caption',                          'KEY_CAPTION'),
        ('ClockDisplay',                     'KEY_CLOCK_DISPLAY'),
        ('Setup Clock',                      'KEY_SETUP_CLOCK_TIMER'),
        ('Subtitle',                         'KEY_SUB_TITLE'),
    )),
    ('Zoom ', (
        ('Zoom Move',                        'KEY_ZOOM_MOVE'),
        ('Zoom In',                          'KEY_ZOOM_IN'),
        ('Zoom Out',                         'KEY_ZOOM_OUT'),
        ('Zoom 1',                           'KEY_ZOOM1'),
        ('Zoom 2',                           'KEY_ZOOM2')
    )),
    ('Other Keys ', (
        ('Wheel Left',                       'KEY_WHEEL_LEFT'),
        ('Wheel Right',                      'KEY_WHEEL_RIGHT'),
        ('Add/Del',                          'KEY_ADDDEL'),
        ('Plus 100',                         'KEY_PLUS100'),
        ('AD',                               'KEY_AD'),
        ('Link',                             'KEY_LINK'),
        ('Turbo',                            'KEY_TURBO'),
        ('Convergence',                      'KEY_CONVERGENCE'),
        ('Device Connect',                   'KEY_DEVICE_CONNECT'),
        ('Key 11',                           'KEY_11'),
        ('Key 12',                           'KEY_12'),
        ('Key Factory',                      'KEY_FACTORY'),
        ('Key 3SPEED',                       'KEY_3SPEED'),
        ('Key RSURF',                        'KEY_RSURF'),
        ('FF_',                              'KEY_FF_'),
        ('REWIND_',                          'KEY_REWIND_'),
        ('Angle',                            'KEY_ANGLE'),
        ('Reserved 1',                       'KEY_RESERVED1'),
        ('Program',                          'KEY_PROGRAM'),
        ('Bookmark',                         'KEY_BOOKMARK'),
        ('Print',                            'KEY_PRINT'),
        ('Clear',                            'KEY_CLEAR'),
        ('V Chip',                           'KEY_VCHIP'),
        ('Repeat',                           'KEY_REPEAT'),
        ('Door',                             'KEY_DOOR'),
        ('Open',                             'KEY_OPEN'),
        ('DMA',                              'KEY_DMA'),
        ('MTS',                              'KEY_MTS'),
        ('DNIe',                             'KEY_DNIe'),
        ('SRS',                              'KEY_SRS'),
        ('Convert Audio Main/Sub',           'KEY_CONVERT_AUDIO_MAINSUB'),
        ('MDC',                              'KEY_MDC'),
        ('Sound Effect',                     'KEY_SEFFECT'),
        ('PERPECT Focus',                    'KEY_PERPECT_FOCUS'),
        ('Caller ID',                        'KEY_CALLER_ID'),
        ('Scale',                            'KEY_SCALE'),
        ('Magic Bright',                     'KEY_MAGIC_BRIGHT'),
        ('W Link',                           'KEY_W_LINK'),
        ('DTV Link',                         'KEY_DTV_LINK'),
        ('Application List',                 'KEY_APP_LIST'),
        ('Back MHP',                         'KEY_BACK_MHP'),
        ('Alternate MHP',                    'KEY_ALT_MHP'),
        ('DNSe',                             'KEY_DNSe'),
        ('RSS',                              'KEY_RSS'),
        ('Entertainment',                    'KEY_ENTERTAINMENT'),
        ('ID Input',                         'KEY_ID_INPUT'),
        ('ID Setup',                         'KEY_ID_SETUP'),
        ('Any View',                         'KEY_ANYVIEW'),
        ('MS',                               'KEY_MS'),
        ('KEY_MORE',                         'KEY_MORE'),
        ('KEY_MIC',                          'KEY_MIC'),
        ('KEY_NINE_SEPERATE',                'KEY_NINE_SEPERATE'),
        ('Auto Format',                      'KEY_AUTO_FORMAT'),
        ('DNET',                             'KEY_DNET')
    )),
    ('Auto Arc Keys ', (
        ('KEY_AUTO_ARC_C_FORCE_AGING',       'KEY_AUTO_ARC_C_FORCE_AGING'),
        ('KEY_AUTO_ARC_CAPTION_ENG',         'KEY_AUTO_ARC_CAPTION_ENG'),
        ('KEY_AUTO_ARC_USBJACK_INSPECT',     'KEY_AUTO_ARC_USBJACK_INSPECT'),
        ('KEY_AUTO_ARC_RESET',               'KEY_AUTO_ARC_RESET'),
        ('KEY_AUTO_ARC_LNA_ON',              'KEY_AUTO_ARC_LNA_ON'),
        ('KEY_AUTO_ARC_LNA_OFF',             'KEY_AUTO_ARC_LNA_OFF'),
        ('KEY_AUTO_ARC_ANYNET_MODE_OK',      'KEY_AUTO_ARC_ANYNET_MODE_OK'),
        ('KEY_AUTO_ARC_ANYNET_AUTO_START',   'KEY_AUTO_ARC_ANYNET_AUTO_START'),
        ('KEY_AUTO_ARC_CAPTION_ON',          'KEY_AUTO_ARC_CAPTION_ON'),
        ('KEY_AUTO_ARC_CAPTION_OFF',         'KEY_AUTO_ARC_CAPTION_OFF'),
        ('KEY_AUTO_ARC_PIP_DOUBLE',          'KEY_AUTO_ARC_PIP_DOUBLE'),
        ('KEY_AUTO_ARC_PIP_LARGE',           'KEY_AUTO_ARC_PIP_LARGE'),
        ('KEY_AUTO_ARC_PIP_LEFT_TOP',        'KEY_AUTO_ARC_PIP_LEFT_TOP'),
        ('KEY_AUTO_ARC_PIP_RIGHT_TOP',       'KEY_AUTO_ARC_PIP_RIGHT_TOP'),
        ('KEY_AUTO_ARC_PIP_LEFT_BOTTOM',     'KEY_AUTO_ARC_PIP_LEFT_BOTTOM'),
        ('KEY_AUTO_ARC_PIP_CH_CHANGE',       'KEY_AUTO_ARC_PIP_CH_CHANGE'),
        ('KEY_AUTO_ARC_AUTOCOLOR_SUCCESS',   'KEY_AUTO_ARC_AUTOCOLOR_SUCCESS'),
        ('KEY_AUTO_ARC_AUTOCOLOR_FAIL',      'KEY_AUTO_ARC_AUTOCOLOR_FAIL'),
        ('KEY_AUTO_ARC_JACK_IDENT',          'KEY_AUTO_ARC_JACK_IDENT'),
        ('KEY_AUTO_ARC_CAPTION_KOR',         'KEY_AUTO_ARC_CAPTION_KOR'),
        ('KEY_AUTO_ARC_ANTENNA_AIR',         'KEY_AUTO_ARC_ANTENNA_AIR'),
        ('KEY_AUTO_ARC_ANTENNA_CABLE',       'KEY_AUTO_ARC_ANTENNA_CABLE'),
        ('KEY_AUTO_ARC_ANTENNA_SATELLITE',   'KEY_AUTO_ARC_ANTENNA_SATELLITE'),
    )),
    ('Panel Keys ', (
        ('KEY_PANNEL_POWER',                 'KEY_PANNEL_POWER'),
        ('KEY_PANNEL_CHUP',                  'KEY_PANNEL_CHUP'),
        ('KEY_PANNEL_VOLUP',                 'KEY_PANNEL_VOLUP'),
        ('KEY_PANNEL_VOLDOW',                'KEY_PANNEL_VOLDOW'),
        ('KEY_PANNEL_ENTER',                 'KEY_PANNEL_ENTER'),
        ('KEY_PANNEL_MENU',                  'KEY_PANNEL_MENU'),
        ('KEY_PANNEL_SOURCE',                'KEY_PANNEL_SOURCE'),
        ('KEY_PANNEL_ENTER',                 'KEY_PANNEL_ENTER')
    )),
    ('Extended Keys ', (
        ('KEY_EXT1',                         'KEY_EXT1'),
        ('KEY_EXT2',                         'KEY_EXT2'),
        ('KEY_EXT3',                         'KEY_EXT3'),
        ('KEY_EXT4',                         'KEY_EXT4'),
        ('KEY_EXT5',                         'KEY_EXT5'),
        ('KEY_EXT6',                         'KEY_EXT6'),
        ('KEY_EXT7',                         'KEY_EXT7'),
        ('KEY_EXT8',                         'KEY_EXT8'),
        ('KEY_EXT11',                        'KEY_EXT11'),
        ('KEY_EXT12',                        'KEY_EXT12'),
        ('KEY_EXT13',                        'KEY_EXT13'),
        ('KEY_EXT16',                        'KEY_EXT16'),
        ('KEY_EXT17',                        'KEY_EXT17'),
        ('KEY_EXT18',                        'KEY_EXT18'),
        ('KEY_EXT19',                        'KEY_EXT19'),
        ('KEY_EXT20',                        'KEY_EXT20'),
        ('KEY_EXT21',                        'KEY_EXT21'),
        ('KEY_EXT22',                        'KEY_EXT22'),
        ('KEY_EXT23',                        'KEY_EXT23'),
        ('KEY_EXT24',                        'KEY_EXT24'),
        ('KEY_EXT25',                        'KEY_EXT25'),
        ('KEY_EXT26',                        'KEY_EXT26'),
        ('KEY_EXT27',                        'KEY_EXT27'),
        ('KEY_EXT28',                        'KEY_EXT28'),
        ('KEY_EXT29',                        'KEY_EXT29'),
        ('KEY_EXT30',                        'KEY_EXT30'),
        ('KEY_EXT31',                        'KEY_EXT31'),
        ('KEY_EXT32',                        'KEY_EXT32'),
        ('KEY_EXT33',                        'KEY_EXT33'),
        ('KEY_EXT34',                        'KEY_EXT34'),
        ('KEY_EXT35',                        'KEY_EXT35'),
        ('KEY_EXT36',                        'KEY_EXT36'),
        ('KEY_EXT37',                        'KEY_EXT37'),
        ('KEY_EXT38',                        'KEY_EXT38'),
        ('KEY_EXT39',                        'KEY_EXT39'),
        ('KEY_EXT40',                        'KEY_EXT40'),
        ('KEY_EXT41',                        'KEY_EXT41')
    ))
)

KEYS = {}

for grp in KEY_MAPPINGS:
    for k in grp[1]:
        desc, cmd = k
        KEYS[cmd] = SendButtonCls(cmd, grp[0], desc)
