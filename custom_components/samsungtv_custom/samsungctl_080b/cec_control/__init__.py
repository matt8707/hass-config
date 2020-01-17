# -*- coding: utf-8 -*-
# This file is part of the libCEC(R) library.
#
# libCEC(R) is Copyright (C) 2011-2015 Pulse-Eight Limited.
# All rights reserved.
# libCEC(R) is an original work, containing original code.
#
# libCEC(R) is a trademark of Pulse-Eight Limited.
#
# This program is dual-licensed; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301  USA
#
#
# Alternatively, you can license this library under a commercial license,
# please contact Pulse-Eight Licensing for more information.
#
# For more information contact:
# Pulse-Eight Licensing       <license@pulse-eight.com>
#     http://www.pulse-eight.com/
#     http://www.pulse-eight.net/
#
#
# The code contained within this file also falls under the GNU license of
# EventGhost
#
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
import threading
import cec
import time
import logging
import six

try:
    from . import dispatcher
except ValueError:
    import dispatcher

logger = logging.getLogger(__name__)

ISO639_2 = {
    'aar': 'Afar',
    'abk': 'Abkhazian',
    'ace': 'Achinese',
    'ach': 'Acoli',
    'ada': 'Adangme',
    'ady': 'Adyghe',
    'afa': 'Afro-Asiatic languages',
    'afh': 'Afrihili',
    'afr': 'Afrikaans',
    'ain': 'Ainu',
    'aka': 'Akan',
    'akk': 'Akkadian',
    'alb': 'Albanian',
    'ale': 'Aleut',
    'alg': 'Algonquian languages',
    'alt': 'Southern Altai',
    'amh': 'Amharic',
    'ang': 'English, Old (ca.450-1100)',
    'anp': 'Angika',
    'apa': 'Apache languages',
    'ara': 'Arabic',
    'arc': 'Official Aramaic (700-300 BCE)',
    'arg': 'Aragonese',
    'arm': 'Armenian',
    'arn': 'Mapudungun',
    'arp': 'Arapaho',
    'art': 'Artificial languages',
    'arw': 'Arawak',
    'asm': 'Assamese',
    'ast': 'Asturian',
    'ath': 'Athapascan languages',
    'aus': 'Australian languages',
    'ava': 'Avaric',
    'ave': 'Avestan',
    'awa': 'Awadhi',
    'aym': 'Aymara',
    'aze': 'Azerbaijani',
    'bad': 'Banda languages',
    'bai': 'Bamileke languages',
    'bak': 'Bashkir',
    'bal': 'Baluchi',
    'bam': 'Bambara',
    'ban': 'Balinese',
    'baq': 'Basque',
    'bas': 'Basa',
    'bat': 'Baltic languages',
    'bej': 'Beja',
    'bel': 'Belarusian',
    'bem': 'Bemba',
    'ben': 'Bengali',
    'ber': 'Berber languages',
    'bho': 'Bhojpuri',
    'bih': 'Bihari languages',
    'bik': 'Bikol',
    'bin': 'Bini',
    'bis': 'Bislama',
    'bla': 'Siksika',
    'bnt': 'Bantu (Other)',
    'bos': 'Bosnian',
    'bra': 'Braj',
    'bre': 'Breton',
    'btk': 'Batak languages',
    'bua': 'Buriat',
    'bug': 'Buginese',
    'bul': 'Bulgarian',
    'bur': 'Burmese',
    'byn': 'Blin',
    'cad': 'Caddo',
    'cai': 'Central American Indian languages',
    'car': 'Galibi Carib',
    'cat': 'Catalan',
    'cau': 'Caucasian languages',
    'ceb': 'Cebuano',
    'cel': 'Celtic languages',
    'cha': 'Chamorro',
    'chb': 'Chibcha',
    'che': 'Chechen',
    'chg': 'Chagatai',
    'chi': 'Chinese',
    'chk': 'Chuukese',
    'chm': 'Mari',
    'chn': 'Chinook jargon',
    'cho': 'Choctaw',
    'chp': 'Chipewyan',
    'chr': 'Cherokee',
    'chu': 'Church Slavic',
    'chv': 'Chuvash',
    'chy': 'Cheyenne',
    'cmc': 'Chamic languages',
    'cnr': 'Montenegrin',
    'cop': 'Coptic',
    'cor': 'Cornish',
    'cos': 'Corsican',
    'cpe': 'Creoles and pidgins, English based',
    'cpf': 'Creoles and pidgins, French-based ',
    'cpp': 'Creoles and pidgins, Portuguese-based ',
    'cre': 'Cree',
    'crh': 'Crimean Tatar',
    'crp': 'Creoles and pidgins ',
    'csb': 'Kashubian',
    'cus': 'Cushitic languages',
    'cze': 'Czech',
    'dak': 'Dakota',
    'dan': 'Danish',
    'dar': 'Dargwa',
    'day': 'Land Dayak languages',
    'del': 'Delaware',
    'den': 'Slave (Athapascan)',
    'dgr': 'Dogrib',
    'din': 'Dinka',
    'div': 'Divehi',
    'doi': 'Dogri',
    'dra': 'Dravidian languages',
    'dsb': 'Lower Sorbian',
    'dua': 'Duala',
    'dum': 'Dutch, Middle (ca.1050-1350)',
    'dut': 'Dutch',
    'dyu': 'Dyula',
    'dzo': 'Dzongkha',
    'efi': 'Efik',
    'egy': 'Egyptian (Ancient)',
    'eka': 'Ekajuk',
    'elx': 'Elamite',
    'eng': 'English',
    'enm': 'English, Middle (1100-1500)',
    'epo': 'Esperanto',
    'est': 'Estonian',
    'ewe': 'Ewe',
    'ewo': 'Ewondo',
    'fan': 'Fang',
    'fao': 'Faroese',
    'fat': 'Fanti',
    'fij': 'Fijian',
    'fil': 'Filipino',
    'fin': 'Finnish',
    'fiu': 'Finno-Ugrian languages',
    'fon': 'Fon',
    'fre': 'French',
    'frm': 'French, Middle (ca.1400-1600)',
    'fro': 'French, Old (842-ca.1400)',
    'frr': 'Northern Frisian',
    'frs': 'Eastern Frisian',
    'fry': 'Western Frisian',
    'ful': 'Fulah',
    'fur': 'Friulian',
    'gaa': 'Ga',
    'gay': 'Gayo',
    'gba': 'Gbaya',
    'gem': 'Germanic languages',
    'geo': 'Georgian',
    'ger': 'German',
    'gez': 'Geez',
    'gil': 'Gilbertese',
    'gla': 'Gaelic',
    'gle': 'Irish',
    'glg': 'Galician',
    'glv': 'Manx',
    'gmh': 'German, Middle High (ca.1050-1500)',
    'goh': 'German, Old High (ca.750-1050)',
    'gon': 'Gondi',
    'gor': 'Gorontalo',
    'got': 'Gothic',
    'grb': 'Grebo',
    'grc': 'Greek, Ancient (to 1453)',
    'gre': 'Greek, Modern (1453-)',
    'grn': 'Guarani',
    'gsw': 'Swiss German',
    'guj': 'Gujarati',
    'gwi': "Gwich'in",
    'hai': 'Haida',
    'hat': 'Haitian',
    'hau': 'Hausa',
    'haw': 'Hawaiian',
    'heb': 'Hebrew',
    'her': 'Herero',
    'hil': 'Hiligaynon',
    'him': 'Himachali languages',
    'hin': 'Hindi',
    'hit': 'Hittite',
    'hmn': 'Hmong',
    'hmo': 'Hiri Motu',
    'hrv': 'Croatian',
    'hsb': 'Upper Sorbian',
    'hun': 'Hungarian',
    'hup': 'Hupa',
    'iba': 'Iban',
    'ibo': 'Igbo',
    'ice': 'Icelandic',
    'ido': 'Ido',
    'iii': 'Sichuan Yi',
    'ijo': 'Ijo languages',
    'iku': 'Inuktitut',
    'ile': 'Interlingue',
    'ilo': 'Iloko',
    'ina': 'Interlingua (International Auxiliary Language Association)',
    'inc': 'Indic languages',
    'ind': 'Indonesian',
    'ine': 'Indo-European languages',
    'inh': 'Ingush',
    'ipk': 'Inupiaq',
    'ira': 'Iranian languages',
    'iro': 'Iroquoian languages',
    'ita': 'Italian',
    'jav': 'Javanese',
    'jbo': 'Lojban',
    'jpn': 'Japanese',
    'jpr': 'Judeo-Persian',
    'jrb': 'Judeo-Arabic',
    'kaa': 'Kara-Kalpak',
    'kab': 'Kabyle',
    'kac': 'Kachin',
    'kal': 'Kalaallisut',
    'kam': 'Kamba',
    'kan': 'Kannada',
    'kar': 'Karen languages',
    'kas': 'Kashmiri',
    'kau': 'Kanuri',
    'kaw': 'Kawi',
    'kaz': 'Kazakh',
    'kbd': 'Kabardian',
    'kha': 'Khasi',
    'khi': 'Khoisan languages',
    'khm': 'Central Khmer',
    'kho': 'Khotanese',
    'kik': 'Kikuyu',
    'kin': 'Kinyarwanda',
    'kir': 'Kirghiz',
    'kmb': 'Kimbundu',
    'kok': 'Konkani',
    'kom': 'Komi',
    'kon': 'Kongo',
    'kor': 'Korean',
    'kos': 'Kosraean',
    'kpe': 'Kpelle',
    'krc': 'Karachay-Balkar',
    'krl': 'Karelian',
    'kro': 'Kru languages',
    'kru': 'Kurukh',
    'kua': 'Kuanyama',
    'kum': 'Kumyk',
    'kur': 'Kurdish',
    'kut': 'Kutenai',
    'lad': 'Ladino',
    'lah': 'Lahnda',
    'lam': 'Lamba',
    'lao': 'Lao',
    'lat': 'Latin',
    'lav': 'Latvian',
    'lez': 'Lezghian',
    'lim': 'Limburgan',
    'lin': 'Lingala',
    'lit': 'Lithuanian',
    'lol': 'Mongo',
    'loz': 'Lozi',
    'ltz': 'Luxembourgish',
    'lua': 'Luba-Lulua',
    'lub': 'Luba-Katanga',
    'lug': 'Ganda',
    'lui': 'Luiseno',
    'lun': 'Lunda',
    'luo': 'Luo (Kenya and Tanzania)',
    'lus': 'Lushai',
    'mac': 'Macedonian',
    'mad': 'Madurese',
    'mag': 'Magahi',
    'mah': 'Marshallese',
    'mai': 'Maithili',
    'mak': 'Makasar',
    'mal': 'Malayalam',
    'man': 'Mandingo',
    'mao': 'Maori',
    'map': 'Austronesian languages',
    'mar': 'Marathi',
    'mas': 'Masai',
    'may': 'Malay',
    'mdf': 'Moksha',
    'mdr': 'Mandar',
    'men': 'Mende',
    'mga': 'Irish, Middle (900-1200)',
    'mic': "Mi'kmaq",
    'min': 'Minangkabau',
    'mis': 'Uncoded languages',
    'mkh': 'Mon-Khmer languages',
    'mlg': 'Malagasy',
    'mlt': 'Maltese',
    'mnc': 'Manchu',
    'mni': 'Manipuri',
    'mno': 'Manobo languages',
    'moh': 'Mohawk',
    'mon': 'Mongolian',
    'mos': 'Mossi',
    'mul': 'Multiple languages',
    'mun': 'Munda languages',
    'mus': 'Creek',
    'mwl': 'Mirandese',
    'mwr': 'Marwari',
    'myn': 'Mayan languages',
    'myv': 'Erzya',
    'nah': 'Nahuatl languages',
    'nai': 'North American Indian languages',
    'nap': 'Neapolitan',
    'nau': 'Nauru',
    'nav': 'Navajo',
    'nbl': 'Ndebele, South',
    'nde': 'Ndebele, North',
    'ndo': 'Ndonga',
    'nds': 'Low German',
    'nep': 'Nepali',
    'new': 'Nepal Bhasa',
    'nia': 'Nias',
    'nic': 'Niger-Kordofanian languages',
    'niu': 'Niuean',
    'nno': 'Norwegian Nynorsk',
    'nob': 'Bokm\xc3\xa5l, Norwegian',
    'nog': 'Nogai',
    'non': 'Norse, Old',
    'nor': 'Norwegian',
    'nqo': "N'Ko",
    'nso': 'Pedi',
    'nub': 'Nubian languages',
    'nwc': 'Classical Newari',
    'nya': 'Chichewa',
    'nym': 'Nyamwezi',
    'nyn': 'Nyankole',
    'nyo': 'Nyoro',
    'nzi': 'Nzima',
    'oci': 'Occitan (post 1500)',
    'oji': 'Ojibwa',
    'ori': 'Oriya',
    'orm': 'Oromo',
    'osa': 'Osage',
    'oss': 'Ossetian',
    'ota': 'Turkish, Ottoman (1500-1928)',
    'oto': 'Otomian languages',
    'paa': 'Papuan languages',
    'pag': 'Pangasinan',
    'pal': 'Pahlavi',
    'pam': 'Pampanga',
    'pan': 'Panjabi',
    'pap': 'Papiamento',
    'pau': 'Palauan',
    'peo': 'Persian, Old (ca.600-400 B.C.)',
    'per': 'Persian',
    'phi': 'Philippine languages',
    'phn': 'Phoenician',
    'pli': 'Pali',
    'pol': 'Polish',
    'pon': 'Pohnpeian',
    'por': 'Portuguese',
    'pra': 'Prakrit languages',
    'pro': 'Proven\xc3\xa7al, Old (to 1500)',
    'pus': 'Pushto',
    'que': 'Quechua',
    'raj': 'Rajasthani',
    'rap': 'Rapanui',
    'rar': 'Rarotongan',
    'roa': 'Romance languages',
    'roh': 'Romansh',
    'rom': 'Romany',
    'rum': 'Romanian',
    'run': 'Rundi',
    'rup': 'Aromanian',
    'rus': 'Russian',
    'sad': 'Sandawe',
    'sag': 'Sango',
    'sah': 'Yakut',
    'sai': 'South American Indian (Other)',
    'sal': 'Salishan languages',
    'sam': 'Samaritan Aramaic',
    'san': 'Sanskrit',
    'sas': 'Sasak',
    'sat': 'Santali',
    'scn': 'Sicilian',
    'sco': 'Scots',
    'sel': 'Selkup',
    'sem': 'Semitic languages',
    'sga': 'Irish, Old (to 900)',
    'sgn': 'Sign Languages',
    'shn': 'Shan',
    'sid': 'Sidamo',
    'sin': 'Sinhala',
    'sio': 'Siouan languages',
    'sit': 'Sino-Tibetan languages',
    'sla': 'Slavic languages',
    'slo': 'Slovak',
    'slv': 'Slovenian',
    'sma': 'Southern Sami',
    'sme': 'Northern Sami',
    'smi': 'Sami languages',
    'smj': 'Lule Sami',
    'smn': 'Inari Sami',
    'smo': 'Samoan',
    'sms': 'Skolt Sami',
    'sna': 'Shona',
    'snd': 'Sindhi',
    'snk': 'Soninke',
    'sog': 'Sogdian',
    'som': 'Somali',
    'son': 'Songhai languages',
    'sot': 'Sotho, Southern',
    'spa': 'Spanish',
    'srd': 'Sardinian',
    'srn': 'Sranan Tongo',
    'srp': 'Serbian',
    'srr': 'Serer',
    'ssa': 'Nilo-Saharan languages',
    'ssw': 'Swati',
    'suk': 'Sukuma',
    'sun': 'Sundanese',
    'sus': 'Susu',
    'sux': 'Sumerian',
    'swa': 'Swahili',
    'swe': 'Swedish',
    'syc': 'Classical Syriac',
    'syr': 'Syriac',
    'tah': 'Tahitian',
    'tai': 'Tai languages',
    'tam': 'Tamil',
    'tat': 'Tatar',
    'tel': 'Telugu',
    'tem': 'Timne',
    'ter': 'Tereno',
    'tet': 'Tetum',
    'tgk': 'Tajik',
    'tgl': 'Tagalog',
    'tha': 'Thai',
    'tib': 'Tibetan',
    'tig': 'Tigre',
    'tir': 'Tigrinya',
    'tiv': 'Tiv',
    'tkl': 'Tokelau',
    'tlh': 'Klingon',
    'tli': 'Tlingit',
    'tmh': 'Tamashek',
    'tog': 'Tonga (Nyasa)',
    'ton': 'Tonga (Tonga Islands)',
    'tpi': 'Tok Pisin',
    'tsi': 'Tsimshian',
    'tsn': 'Tswana',
    'tso': 'Tsonga',
    'tuk': 'Turkmen',
    'tum': 'Tumbuka',
    'tup': 'Tupi languages',
    'tur': 'Turkish',
    'tut': 'Altaic languages',
    'tvl': 'Tuvalu',
    'twi': 'Twi',
    'tyv': 'Tuvinian',
    'udm': 'Udmurt',
    'uga': 'Ugaritic',
    'uig': 'Uighur',
    'ukr': 'Ukrainian',
    'umb': 'Umbundu',
    'und': 'Undetermined',
    'urd': 'Urdu',
    'uzb': 'Uzbek',
    'vai': 'Vai',
    'ven': 'Venda',
    'vie': 'Vietnamese',
    'vol': 'Volap\xc3\xbck',
    'vot': 'Votic',
    'wak': 'Wakashan languages',
    'wal': 'Walamo',
    'war': 'Waray',
    'was': 'Washo',
    'wel': 'Welsh',
    'wen': 'Sorbian languages',
    'wln': 'Walloon',
    'wol': 'Wolof',
    'xal': 'Kalmyk',
    'xho': 'Xhosa',
    'yao': 'Yao',
    'yap': 'Yapese',
    'yid': 'Yiddish',
    'yor': 'Yoruba',
    'ypk': 'Yupik languages',
    'zap': 'Zapotec',
    'zbl': 'Blissymbols',
    'zen': 'Zenaga',
    'zgh': 'Standard Moroccan Tamazight',
    'zha': 'Zhuang',
    'znd': 'Zande languages',
    'zul': 'Zulu',
    'zun': 'Zuni',
    'zxx': 'No linguistic content',
    'zza': 'Zaza',
}

DEVICE_TYPES = [
    cec.CEC_DEVICE_TYPE_TV,
    cec.CEC_DEVICE_TYPE_RECORDING_DEVICE,
    cec.CEC_DEVICE_TYPE_RESERVED,
    cec.CEC_DEVICE_TYPE_TUNER,
    cec.CEC_DEVICE_TYPE_PLAYBACK_DEVICE,
    cec.CEC_DEVICE_TYPE_AUDIO_SYSTEM
]

MEDIA_FORWARD = cec.CEC_PLAY_MODE_PLAY_FORWARD
MEDIA_FORWARD_SLOW = cec.CEC_PLAY_MODE_SLOW_FORWARD_MIN_SPEED
MEDIA_FORWARD_FAST = cec.CEC_PLAY_MODE_FAST_FORWARD_MIN_SPEED
MEDIA_REVERSE = cec.CEC_PLAY_MODE_PLAY_REVERSE
MEDIA_REVERSE_SLOW = cec.CEC_PLAY_MODE_SLOW_REVERSE_MIN_SPEED
MEDIA_REVERSE_FAST = cec.CEC_PLAY_MODE_FAST_REVERSE_MIN_SPEED
MEDIA_RECORD = cec.CEC_DECK_INFO_RECORD
MEDIA_EJECT = cec.CEC_DECK_CONTROL_MODE_EJECT
MEDIA_PLAY = MEDIA_FORWARD
MEDIA_STOP = cec.CEC_DECK_CONTROL_MODE_STOP
MEDIA_PAUSE = cec.CEC_DECK_INFO_STILL
MEDIA_REWIND = MEDIA_REVERSE_SLOW
MEDIA_FASTFORWARD = MEDIA_FORWARD_FAST
MEDIA_SKIPFORWARD = cec.CEC_DECK_CONTROL_MODE_SKIP_FORWARD_WIND
MEDIA_SKIPBACK = cec.CEC_DECK_CONTROL_MODE_SKIP_REVERSE_REWIND

CEC_PLAYBACK_MAPPING = {
    cec.CEC_DECK_INFO_RECORD: None,
    cec.CEC_DECK_INFO_INDEX_SEARCH_FORWARD: None,
    cec.CEC_DECK_INFO_INDEX_SEARCH_REVERSE: None,
    cec.CEC_DECK_INFO_OTHER_STATUS: None,
    cec.CEC_DECK_INFO_OTHER_STATUS_LG: None,
    cec.CEC_PLAY_MODE_PLAY_FORWARD: cec.CEC_DECK_INFO_PLAY,
    cec.CEC_PLAY_MODE_PLAY_REVERSE: cec.CEC_DECK_INFO_PLAY_REVERSE,
    cec.CEC_PLAY_MODE_PLAY_STILL: cec.CEC_DECK_INFO_STILL,
    cec.CEC_PLAY_MODE_FAST_FORWARD_MIN_SPEED: cec.CEC_DECK_INFO_FAST_FORWARD,
    cec.CEC_PLAY_MODE_FAST_FORWARD_MAX_SPEED: cec.CEC_DECK_INFO_FAST_FORWARD,
    cec.CEC_PLAY_MODE_FAST_REVERSE_MIN_SPEED: cec.CEC_DECK_INFO_FAST_REVERSE,
    cec.CEC_PLAY_MODE_FAST_REVERSE_MAX_SPEED: cec.CEC_DECK_INFO_FAST_REVERSE,
    cec.CEC_PLAY_MODE_SLOW_FORWARD_MIN_SPEED: cec.CEC_DECK_INFO_SLOW,
    cec.CEC_PLAY_MODE_SLOW_FORWARD_MEDIUM_SPEED: cec.CEC_DECK_INFO_SLOW,
    cec.CEC_PLAY_MODE_SLOW_FORWARD_MAX_SPEED: cec.CEC_DECK_INFO_SLOW,
    cec.CEC_PLAY_MODE_SLOW_REVERSE_MIN_SPEED: cec.CEC_DECK_INFO_SLOW_REVERSE,
    cec.CEC_PLAY_MODE_SLOW_REVERSE_MAX_SPEED: cec.CEC_DECK_INFO_SLOW_REVERSE,
    cec.CEC_DECK_CONTROL_MODE_STOP: cec.CEC_DECK_INFO_STOP,
    cec.CEC_DECK_CONTROL_MODE_EJECT: cec.CEC_DECK_INFO_NO_MEDIA,
    cec.CEC_DECK_CONTROL_MODE_SKIP_FORWARD_WIND: (
        cec.CEC_DECK_INFO_SKIP_FORWARD_WIND
    ),
    cec.CEC_DECK_CONTROL_MODE_SKIP_REVERSE_REWIND: (
        cec.CEC_DECK_INFO_SKIP_REVERSE_REWIND
    ),
    cec.CEC_PLAY_MODE_SLOW_REVERSE_MEDIUM_SPEED: (
        cec.CEC_DECK_INFO_SLOW_REVERSE
    ),
    cec.CEC_PLAY_MODE_FAST_REVERSE_MEDIUM_SPEED: (
        cec.CEC_DECK_INFO_FAST_REVERSE
    ),
    cec.CEC_PLAY_MODE_FAST_FORWARD_MEDIUM_SPEED: (
        cec.CEC_DECK_INFO_FAST_FORWARD
    )
}

CEC_OPCODE_PLAY_MODE_MAPPING = [
    cec.CEC_PLAY_MODE_PLAY_FORWARD,
    cec.CEC_PLAY_MODE_PLAY_REVERSE,
    cec.CEC_PLAY_MODE_PLAY_STILL,
    cec.CEC_PLAY_MODE_FAST_FORWARD_MIN_SPEED,
    cec.CEC_PLAY_MODE_FAST_FORWARD_MEDIUM_SPEED,
    cec.CEC_PLAY_MODE_FAST_FORWARD_MAX_SPEED,
    cec.CEC_PLAY_MODE_FAST_REVERSE_MIN_SPEED,
    cec.CEC_PLAY_MODE_FAST_REVERSE_MEDIUM_SPEED,
    cec.CEC_PLAY_MODE_FAST_REVERSE_MAX_SPEED,
    cec.CEC_PLAY_MODE_SLOW_FORWARD_MIN_SPEED,
    cec.CEC_PLAY_MODE_SLOW_FORWARD_MEDIUM_SPEED,
    cec.CEC_PLAY_MODE_SLOW_FORWARD_MAX_SPEED,
    cec.CEC_PLAY_MODE_SLOW_REVERSE_MIN_SPEED,
    cec.CEC_PLAY_MODE_SLOW_REVERSE_MEDIUM_SPEED,
    cec.CEC_PLAY_MODE_SLOW_REVERSE_MAX_SPEED
]

CEC_OPCODE_DECK_CONTROL_MAPPING = [
    cec.CEC_DECK_CONTROL_MODE_SKIP_FORWARD_WIND,
    cec.CEC_DECK_CONTROL_MODE_SKIP_REVERSE_REWIND,
    cec.CEC_DECK_CONTROL_MODE_STOP,
    cec.CEC_DECK_CONTROL_MODE_EJECT
]

CEC_PLAYBACK_COMMAND_MAPPING = {
    cec.CEC_PLAY_MODE_PLAY_FORWARD:                '41:24',
    cec.CEC_PLAY_MODE_PLAY_REVERSE:                '41:20',
    cec.CEC_PLAY_MODE_PLAY_STILL:                  '41:25',
    cec.CEC_PLAY_MODE_FAST_FORWARD_MIN_SPEED:      '41:05',
    cec.CEC_PLAY_MODE_FAST_FORWARD_MEDIUM_SPEED:   '41:06',
    cec.CEC_PLAY_MODE_FAST_FORWARD_MAX_SPEED:      '41:07',
    cec.CEC_PLAY_MODE_FAST_REVERSE_MIN_SPEED:      '41:09',
    cec.CEC_PLAY_MODE_FAST_REVERSE_MEDIUM_SPEED:   '41:0A',
    cec.CEC_PLAY_MODE_FAST_REVERSE_MAX_SPEED:      '41:0B',
    cec.CEC_PLAY_MODE_SLOW_FORWARD_MIN_SPEED:      '41:15',
    cec.CEC_PLAY_MODE_SLOW_FORWARD_MEDIUM_SPEED:   '41:16',
    cec.CEC_PLAY_MODE_SLOW_FORWARD_MAX_SPEED:      '41:17',
    cec.CEC_PLAY_MODE_SLOW_REVERSE_MIN_SPEED:      '41:19',
    cec.CEC_PLAY_MODE_SLOW_REVERSE_MEDIUM_SPEED:   '41:1A',
    cec.CEC_PLAY_MODE_SLOW_REVERSE_MAX_SPEED:      '41:1B',
    cec.CEC_DECK_CONTROL_MODE_SKIP_FORWARD_WIND:   '42:01',
    cec.CEC_DECK_CONTROL_MODE_SKIP_REVERSE_REWIND: '42:02',
    cec.CEC_DECK_CONTROL_MODE_STOP:                '42:03',
    cec.CEC_DECK_CONTROL_MODE_EJECT:               '42:04',
}

PLAY_MODE_TO_STRING = {
    cec.CEC_PLAY_MODE_PLAY_FORWARD: 'play forward',
    cec.CEC_PLAY_MODE_PLAY_REVERSE: 'play reverse',
    cec.CEC_PLAY_MODE_PLAY_STILL: 'play still',
    cec.CEC_PLAY_MODE_FAST_FORWARD_MIN_SPEED: 'fast forward min',
    cec.CEC_PLAY_MODE_FAST_FORWARD_MEDIUM_SPEED: 'fast forward medium',
    cec.CEC_PLAY_MODE_FAST_FORWARD_MAX_SPEED: 'fast forward max',
    cec.CEC_PLAY_MODE_FAST_REVERSE_MIN_SPEED: 'fast reverse min',
    cec.CEC_PLAY_MODE_FAST_REVERSE_MEDIUM_SPEED: 'fast reverse medium',
    cec.CEC_PLAY_MODE_FAST_REVERSE_MAX_SPEED: 'fast reverse max',
    cec.CEC_PLAY_MODE_SLOW_FORWARD_MIN_SPEED: 'slow forward min',
    cec.CEC_PLAY_MODE_SLOW_FORWARD_MEDIUM_SPEED: 'slow forward medium',
    cec.CEC_PLAY_MODE_SLOW_FORWARD_MAX_SPEED: 'slow forward max',
    cec.CEC_PLAY_MODE_SLOW_REVERSE_MIN_SPEED: 'slow reverse min',
    cec.CEC_PLAY_MODE_SLOW_REVERSE_MEDIUM_SPEED: 'slow reverse medium',
    cec.CEC_PLAY_MODE_SLOW_REVERSE_MAX_SPEED: 'slow reverse max',
}
TUNER_STATUS_TO_STRING = {
    cec.CEC_TUNER_DISPLAY_INFO_DISPLAYING_DIGITAL_TUNER:  'digital',
    cec.CEC_TUNER_DISPLAY_INFO_NOT_DISPLAYING_TUNER:      'off',
    cec.CEC_TUNER_DISPLAY_INFO_DISPLAYING_ANALOGUE_TUNER: 'analog',
}
PLAYER_STATUS_TO_STRING = {
    cec.CEC_DECK_INFO_PLAY: "play",
    # cec.CEC_DECK_INFO_RECORD: "record",
    cec.CEC_DECK_INFO_PLAY_REVERSE: "play reverse",
    cec.CEC_DECK_INFO_STILL: "still",
    cec.CEC_DECK_INFO_SLOW: "slow",
    cec.CEC_DECK_INFO_SLOW_REVERSE: "slow reverse",
    cec.CEC_DECK_INFO_FAST_FORWARD: "fast forward",
    cec.CEC_DECK_INFO_FAST_REVERSE: "fast reverse",
    cec.CEC_DECK_INFO_NO_MEDIA: "no media",
    cec.CEC_DECK_INFO_STOP: "stop",
    cec.CEC_DECK_INFO_SKIP_FORWARD_WIND: "skip forward",
    cec.CEC_DECK_INFO_SKIP_REVERSE_REWIND: "skip back",
    cec.CEC_DECK_INFO_INDEX_SEARCH_FORWARD: "search forward",
    cec.CEC_DECK_INFO_INDEX_SEARCH_REVERSE: "search reverse",
    cec.CEC_DECK_INFO_OTHER_STATUS: "other",
    cec.CEC_DECK_INFO_OTHER_STATUS_LG: "LG other",
}

CONTROL_CODES = [
    cec.CEC_USER_CONTROL_CODE_SELECT,
    cec.CEC_USER_CONTROL_CODE_UP,
    cec.CEC_USER_CONTROL_CODE_DOWN,
    cec.CEC_USER_CONTROL_CODE_LEFT,
    cec.CEC_USER_CONTROL_CODE_RIGHT,
    cec.CEC_USER_CONTROL_CODE_RIGHT_UP,
    cec.CEC_USER_CONTROL_CODE_RIGHT_DOWN,
    cec.CEC_USER_CONTROL_CODE_LEFT_UP,
    cec.CEC_USER_CONTROL_CODE_LEFT_DOWN,
    cec.CEC_USER_CONTROL_CODE_ROOT_MENU,
    cec.CEC_USER_CONTROL_CODE_SETUP_MENU,
    cec.CEC_USER_CONTROL_CODE_CONTENTS_MENU,
    cec.CEC_USER_CONTROL_CODE_FAVORITE_MENU,
    cec.CEC_USER_CONTROL_CODE_EXIT,
    cec.CEC_USER_CONTROL_CODE_TOP_MENU,
    cec.CEC_USER_CONTROL_CODE_DVD_MENU,
    cec.CEC_USER_CONTROL_CODE_NUMBER_ENTRY_MODE,
    cec.CEC_USER_CONTROL_CODE_NUMBER11,
    cec.CEC_USER_CONTROL_CODE_NUMBER12,
    cec.CEC_USER_CONTROL_CODE_NUMBER0,
    cec.CEC_USER_CONTROL_CODE_NUMBER1,
    cec.CEC_USER_CONTROL_CODE_NUMBER2,
    cec.CEC_USER_CONTROL_CODE_NUMBER3,
    cec.CEC_USER_CONTROL_CODE_NUMBER4,
    cec.CEC_USER_CONTROL_CODE_NUMBER5,
    cec.CEC_USER_CONTROL_CODE_NUMBER6,
    cec.CEC_USER_CONTROL_CODE_NUMBER7,
    cec.CEC_USER_CONTROL_CODE_NUMBER8,
    cec.CEC_USER_CONTROL_CODE_NUMBER9,
    cec.CEC_USER_CONTROL_CODE_DOT,
    cec.CEC_USER_CONTROL_CODE_ENTER,
    cec.CEC_USER_CONTROL_CODE_CLEAR,
    cec.CEC_USER_CONTROL_CODE_NEXT_FAVORITE,
    cec.CEC_USER_CONTROL_CODE_CHANNEL_UP,
    cec.CEC_USER_CONTROL_CODE_CHANNEL_DOWN,
    cec.CEC_USER_CONTROL_CODE_PREVIOUS_CHANNEL,
    cec.CEC_USER_CONTROL_CODE_SOUND_SELECT,
    cec.CEC_USER_CONTROL_CODE_INPUT_SELECT,
    cec.CEC_USER_CONTROL_CODE_DISPLAY_INFORMATION,
    cec.CEC_USER_CONTROL_CODE_HELP,
    cec.CEC_USER_CONTROL_CODE_PAGE_UP,
    cec.CEC_USER_CONTROL_CODE_PAGE_DOWN,
    cec.CEC_USER_CONTROL_CODE_POWER,
    cec.CEC_USER_CONTROL_CODE_VOLUME_UP,
    cec.CEC_USER_CONTROL_CODE_VOLUME_DOWN,
    cec.CEC_USER_CONTROL_CODE_MUTE,
    cec.CEC_USER_CONTROL_CODE_PLAY,
    cec.CEC_USER_CONTROL_CODE_STOP,
    cec.CEC_USER_CONTROL_CODE_PAUSE,
    cec.CEC_USER_CONTROL_CODE_RECORD,
    cec.CEC_USER_CONTROL_CODE_REWIND,
    cec.CEC_USER_CONTROL_CODE_FAST_FORWARD,
    cec.CEC_USER_CONTROL_CODE_EJECT,
    cec.CEC_USER_CONTROL_CODE_FORWARD,
    cec.CEC_USER_CONTROL_CODE_BACKWARD,
    cec.CEC_USER_CONTROL_CODE_STOP_RECORD,
    cec.CEC_USER_CONTROL_CODE_PAUSE_RECORD,
    cec.CEC_USER_CONTROL_CODE_ANGLE,
    cec.CEC_USER_CONTROL_CODE_SUB_PICTURE,
    cec.CEC_USER_CONTROL_CODE_VIDEO_ON_DEMAND,
    cec.CEC_USER_CONTROL_CODE_ELECTRONIC_PROGRAM_GUIDE,
    cec.CEC_USER_CONTROL_CODE_TIMER_PROGRAMMING,
    cec.CEC_USER_CONTROL_CODE_INITIAL_CONFIGURATION,
    cec.CEC_USER_CONTROL_CODE_SELECT_BROADCAST_TYPE,
    cec.CEC_USER_CONTROL_CODE_SELECT_SOUND_PRESENTATION,
    cec.CEC_USER_CONTROL_CODE_PLAY_FUNCTION,
    cec.CEC_USER_CONTROL_CODE_PAUSE_PLAY_FUNCTION,
    cec.CEC_USER_CONTROL_CODE_RECORD_FUNCTION,
    cec.CEC_USER_CONTROL_CODE_PAUSE_RECORD_FUNCTION,
    cec.CEC_USER_CONTROL_CODE_STOP_FUNCTION,
    cec.CEC_USER_CONTROL_CODE_MUTE_FUNCTION,
    cec.CEC_USER_CONTROL_CODE_RESTORE_VOLUME_FUNCTION,
    cec.CEC_USER_CONTROL_CODE_TUNE_FUNCTION,
    cec.CEC_USER_CONTROL_CODE_SELECT_MEDIA_FUNCTION,
    cec.CEC_USER_CONTROL_CODE_SELECT_AV_INPUT_FUNCTION,
    cec.CEC_USER_CONTROL_CODE_SELECT_AUDIO_INPUT_FUNCTION,
    cec.CEC_USER_CONTROL_CODE_POWER_TOGGLE_FUNCTION,
    cec.CEC_USER_CONTROL_CODE_POWER_OFF_FUNCTION,
    cec.CEC_USER_CONTROL_CODE_POWER_ON_FUNCTION,
    cec.CEC_USER_CONTROL_CODE_F1_BLUE,
    cec.CEC_USER_CONTROL_CODE_F2_RED,
    cec.CEC_USER_CONTROL_CODE_F3_GREEN,
    cec.CEC_USER_CONTROL_CODE_F4_YELLOW,
    cec.CEC_USER_CONTROL_CODE_F5,
    cec.CEC_USER_CONTROL_CODE_DATA,
    cec.CEC_USER_CONTROL_CODE_AN_RETURN,
    cec.CEC_USER_CONTROL_CODE_AN_CHANNELS_LIST,
    cec.CEC_USER_CONTROL_CODE_MAX,
    cec.CEC_USER_CONTROL_CODE_UNKNOWN,
]

DEVICE_POWER_EVENT = 0x00
DEVICE_OSD_EVENT = 0x01
DEVICE_CONNECTED_EVENT = 0x02
DEVICE_DISCONNECT_EVENT = 0x03
TV_SOURCE_EVENT = 0x04
TV_REMOTE_EVENT = 0x05
AUDIO_VOLUME_EVENT = 0x06
AUDIO_MUTE_EVENT = 0x07
AUDIO_STATE_EVENT = 0x08
PLAYER_STATUS_EVENT = 0x09


class KeyCodes(object):

    def __init__(self):
        self.__control_codes = {}
        cec_lib = cec.ICECAdapter.Create(cec.libcec_configuration())

        for code in CONTROL_CODES:
            code_name = cec_lib.UserControlCodeToString(code).title()
            self.__control_codes[code_name.replace(' (Function)', '')] = (
                code
            )
        cec_lib.Close()

    def keys(self):
        return self.__control_codes.keys()

    def __getitem__(self, item):

        for codes in self.__control_codes.items():
            if item in codes:
                return codes[int(not codes.index(item))]

        raise KeyError(item)

    def __iter__(self):
        for key in sorted(self.__control_codes.keys()):
            yield key

    def __contains__(self, item):
        return (
            item in self.__control_codes.keys() or
            item in self.__control_codes.values()
        )


KEY_CODES = KeyCodes()


def get_adapter_ports():
    cec_lib = cec.ICECAdapter.Create(cec.libcec_configuration())
    try:
        return sorted(
            list(
                a.strComName
                for a in cec_lib.DetectAdapters()
            )
        )
    finally:
        cec_lib.Close()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args):
        if cls not in cls._instances:
            cls._instances[cls] = {}

        keys = list(args[:])
        for i, arg in enumerate(keys[:]):
            if isinstance(arg, dict):
                keys[i] = str(arg)

        keys = tuple(keys)

        instances = cls._instances[cls]

        for key, value in instances.items():
            if key == keys:
                return value

        instances[keys] = super(
            Singleton,
            cls
        ).__call__(*args)

        return instances[keys]


class EventThread(threading.Thread):
    def __init__(self, adapter, interval):
        self._adapter = adapter
        self.__interval = interval
        self.__event = threading.Event()

        threading.Thread.__init__(
            self,
            name='CECAdapter.{0}.Thread'.format(self._adapter.name)
        )
        self.daemon = True

    def run(self):
        adapter = self._adapter
        old_devices = list(device for device in adapter)
        old = {}

        for device in old_devices:
            old[device] = dict(
                power=device.power,
                osd_name=device.osd_name,
            )

        old_audio = self._adapter.audio

        if old_audio:
            old_mute = self._adapter.mute
            old_volume = self._adapter.volume
        else:
            old_mute = None
            old_volume = None

        power_count = 0

        while not self.__event.isSet():
            new_audio = self._adapter.audio

            if new_audio != old_audio:
                old_audio = new_audio
                dispatcher.send(
                    AUDIO_STATE_EVENT,
                    self._adapter,
                    device=None,
                    value=new_audio
                )
                logger.debug(
                    'CEC.AVRAudio.{0}'.format('On' if new_audio else 'Off')
                )

            if new_audio:
                new_mute = self._adapter.mute
                new_volume = self._adapter.volume

                if new_mute != old_mute:
                    old_mute = new_mute
                    dispatcher.send(
                        AUDIO_MUTE_EVENT,
                        self._adapter,
                        device=None,
                        value=new_mute
                    )
                    logger.debug(
                        'CEC.AVRAudio.Mute.{0}'.format(
                            'On' if new_mute else 'Off'
                        )
                    )

                if new_volume != old_volume:
                    old_volume = new_volume

                    dispatcher.send(
                        AUDIO_VOLUME_EVENT,
                        self._adapter,
                        device=None,
                        value=int(new_volume)
                    )
                    logger.debug(
                        'CEC.AVRAudio.Volume.{0}'.format(int(new_volume))
                    )
            else:
                old_mute = None
                old_volume = None

            new_devices = self._adapter.GetActiveDevices()

            for i in range(16):
                device = old_devices[i]
                name = device.name
                if new_devices.IsSet(i):
                    if not device.connected:
                        device.connected = True

                        dispatcher.send(
                            DEVICE_CONNECTED_EVENT,
                            self._adapter,
                            device=device,
                            value=None
                        )
                        logger.debug(
                            'CEC.Device.{0}.Connected'.format(name)
                        )

                    power = device.power
                    osd_name = device.osd_name

                    if power != old[device]['power']:

                        if (
                            old[device]['power'] ==
                            cec.CEC_POWER_STATUS_IN_TRANSITION_STANDBY_TO_ON
                            and
                            power != cec.CEC_POWER_STATUS_ON
                            and
                            power_count < 50
                        ):
                            power_count += 1

                        elif (
                            old[device]['power'] ==
                            cec.CEC_POWER_STATUS_IN_TRANSITION_ON_TO_STANDBY
                            and
                            power != cec.CEC_POWER_STATUS_STANDBY
                            and
                            power_count < 50
                        ):
                            power_count += 1

                        else:
                            power_count = 0
                            old[device]['power'] = power

                            dispatcher.send(
                                DEVICE_POWER_EVENT,
                                self._adapter,
                                device=device,
                                value=device.power
                            )

                            state = self._adapter.PowerStatusToString(power)
                            state = state.title().replace(' ', '')

                            logger.debug(
                                'CEC.Device.{0}.Power.{1}'.format(name, state)
                            )

                    if osd_name != old[device]['osd_name']:
                        old[device]['osd_name'] = osd_name

                        dispatcher.send(
                            DEVICE_OSD_EVENT,
                            self._adapter,
                            device=device,
                            value=osd_name
                        )

                        logger.debug(
                            'CEC.Device.{0}.OSD.Changed.{0}'.format(
                                name,
                                osd_name
                            )
                        )

                elif device.connected:
                    device.connected = False

                    if old[device]['power']:
                        old[device]['power'] = False

                        dispatcher.send(
                            DEVICE_POWER_EVENT,
                            self._adapter,
                            device=device,
                            value=False
                        )

                        logger.debug(
                            'CEC.Device.{0}.Power.Off'.format(name)
                        )

                    dispatcher.send(
                        DEVICE_DISCONNECT_EVENT,
                        self._adapter,
                        device=device,
                        value=None
                    )

                    logger.debug(
                        'CEC.Device.{0}.Disconnected'.format(name)
                    )

            self.__event.wait(self.__interval)

    def stop(self):
        self.__event.set()
        self.join()


@six.add_metaclass(Singleton)
class PyCECDevice(object):
    is_player = False
    is_tuner = False
    is_recorder = False
    is_tv = False

    def __init__(self, adapter, logical_address):
        self._adapter = adapter
        self._logical_address = logical_address
        self._connected = False
        self._reply_event = threading.Event()
        self._reply = None

    def key_press(self, key):
        self._adapter.SendKeypress(self._logical_address, key, True)

    def key_release(self):
        self._adapter.SendKeyRelease(self._logical_address, True)

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        self._connected = value

    @property
    def name(self):
        return self._adapter.LogicalAddressToString(self._logical_address)

    @property
    def port(self):

        for port in range(1, 16):
            address = (port * 16) * 256
            if self.physical_address == address:
                return port

    @property
    def logical_address(self):
        return self._logical_address

    @property
    def vendor(self):
        return self._adapter.VendorIdToString(
            self._adapter.GetDeviceVendorId(self._logical_address)
        )

    @property
    def physical_address(self):
        return self._adapter.GetDevicePhysicalAddress(self._logical_address)

    @property
    def active_source(self):
        return self._adapter.IsActiveSource(self._logical_address)

    @active_source.setter
    def active_source(self, flag=True):
        if flag:
            port = self.port

            if port is not None:
                packet = cec.cec_command()

                packet.Format(
                    packet,
                    4,
                    15,
                    130
                )

                address = (port * 16) * 256
                address = hex(address)[2:]
                address = list(
                    int(address[i] + address[i + 1], 16)
                    for i in range(0, len(address), 2)
                )

                for addr in address:
                    packet.PushBack(addr)

                self._adapter.Transmit(packet)
            self._adapter.SetActiveSource(self._logical_address)

    @property
    def active_device(self):
        return self._adapter.IsActiveDevice(self._logical_address)

    @property
    def cec_version(self):
        return self._adapter.CecVersionToString(
            self._adapter.GetDeviceCecVersion(self._logical_address)
        )

    @property
    def power(self):
        return self._adapter.GetDevicePowerStatus(self._logical_address)

    @power.setter
    def power(self, value):
        if value:
            self._adapter.PowerOnDevices(self._logical_address)
        else:
            self._adapter.StandbyDevices(self._logical_address)

    @property
    def osd_name(self):
        return self._adapter.GetDeviceOSDName(self._logical_address)

    @osd_name.setter
    def osd_name(self, value):
        if self._logical_address != self._adapter.logical_address:
            raise AttributeError

        self._adapter.SetAdapterOSDName(value)

    def display_osd_message(self, message, duration):
        self._adapter.SetOSDString(
            self._logical_address,
            duration,
            str(message)
        )

    def transmit_menu_state(self, destination, state):
        # CEC_MENU_STATE_ACTIVATED
        # CEC_MENU_STATE_DEACTIVATED
        self._adapter.raw_command(
            self.logical_address,
            destination,
            cec.CEC_OPCODE_MENU_STATUS,
            state
        )

    @property
    def menu_language(self):
        return self._adapter.GetDeviceMenuLanguage(self._logical_address)

    @menu_language.setter
    def menu_language(self, value):
        language = list(ord(char) for char in list(value))
        self._adapter.raw_command(
            self._adapter.logical_address,
            self.logical_address,
            cec.CEC_OPCODE_SET_MENU_LANGUAGE,
            language
        )

    def transmit_menu_language(self, destination, language):
        language = list(ord(char) for char in list(language))

        self._adapter.raw_command(
            self.logical_address,
            destination,
            cec.CEC_OPCODE_GET_MENU_LANGUAGE,
            language
        )

    def command_callback(self, command):
        if command.opcode == cec.CEC_OPCODE_MENU_REQUEST:
            if command.parameters.At(0) == cec.CEC_MENU_REQUEST_TYPE_QUERY:
                self._adapter.trigger_event(
                    '{0}.Menu.StateRequest'.format(self.osd_name),
                    self._adapter[command.initiator].osd_name
                )

            elif (
                command.parameters.At(0) ==
                cec.CEC_MENU_REQUEST_TYPE_ACTIVATE
            ):
                self._adapter.trigger_event(
                    '{0}.Menu.Activate.Request'.format(self.osd_name),
                    self._adapter[command.initiator].osd_name
                )

            elif (
                command.parameters.At(0) ==
                cec.CEC_MENU_REQUEST_TYPE_DEACTIVATE
            ):
                self._adapter.trigger_event(
                    '{0}.Menu.Deactivate.Request'.format(self.osd_name),
                    self._adapter[command.initiator].osd_name
                )

        elif command.opcode == cec.CEC_OPCODE_SET_MENU_LANGUAGE:
            language = (
                chr(command.parameters.At(0)) +
                chr(command.parameters.At(1)) +
                chr(command.parameters.At(2))
            )
            self._adapter.trigger_event(
                '{0}.Menu.LanguageSet.Request.{1}'.format(
                    self.osd_name,
                    language
                ),
                self._adapter[command.initiator].osd_name
            )

        elif command.opcode == cec.CEC_OPCODE_GET_MENU_LANGUAGE:
            self._adapter.trigger_event(
                '{0}.Menu.LanguageGet.Request'.format(self.osd_name),
                self._adapter[command.initiator].osd_name
            )

    def __getattr__(self, item):

        if item in self.__dict__:
            return self.__dict__[item]

        if (
            item in self.__class__.__dict__ and
            hasattr(self.__class__.__dict__[item], 'fget') and
            self.__class__.__dict__[item].fget is not None
        ):
            return self.__class__.__dict__[item].fget(self)

        raise AttributeError(item)


class PyCECTV(PyCECDevice):
    is_tv = True

    def volume_up(self):
        self.key_press(cec.CEC_USER_CONTROL_CODE_VOLUME_UP)

    def volume_down(self):
        self.key_press(cec.CEC_USER_CONTROL_CODE_VOLUME_DOWN)

    def toggle_mute(self):
        self.key_press(cec.CEC_USER_CONTROL_CODE_MUTE)

    @property
    def power(self):
        return self._adapter.GetDevicePowerStatus(self._logical_address)

    @power.setter
    def power(self, value):
        if value:
            def is_tv_off():
                return self.power not in (
                    cec.CEC_POWER_STATUS_IN_TRANSITION_STANDBY_TO_ON,
                    cec.CEC_POWER_STATUS_ON
                )

            self._adapter.PowerOnDevices(self._logical_address)

            if is_tv_off():
                self._adapter.StandbyDevices(self._logical_address)
                self._adapter.PowerOnDevices(self._logical_address)
                if is_tv_off():
                    for device in self._adapter:
                        if device.connected and device.active_source:
                            device.active_source = True
                            break
                    else:
                        self.active_source = True
        else:
            self._adapter.StandbyDevices(self._logical_address)


class PyCECPlayer(PyCECDevice):
    is_player = True

    def __init__(self, adapter, logical_address):
        self.__deck_status = None
        self._enable_notifications = False
        self.__playback_speed = None
        PyCECDevice.__init__(self, adapter, logical_address)

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        self._connected = value
        if value and self._enable_notifications:
            self._adapter.raw_command(
                self._adapter.logical_address,
                self.logical_address,
                cec.CEC_OPCODE_GIVE_DECK_STATUS,
                cec.CEC_STATUS_REQUEST_ON
            )

    def enable_notifications(self, value):
        if value and self.connected:
            self._enable_notifications = True
            self._adapter.raw_command(
                self._adapter.logical_address,
                self.logical_address,
                cec.CEC_OPCODE_GIVE_DECK_STATUS,
                cec.CEC_STATUS_REQUEST_ON
            )

        elif not value:
            if self.connected:
                self._adapter.raw_command(
                    self._adapter.logical_address,
                    self.logical_address,
                    cec.CEC_OPCODE_GIVE_DECK_STATUS,
                    cec.CEC_STATUS_REQUEST_OFF
                )

            self._enable_notifications = False

    enable_notifications = property(fset=enable_notifications)

    def play(self):
        playback_mapping = {
            cec.CEC_PLAY_MODE_PLAY_FORWARD:              (
                cec.CEC_PLAY_MODE_SLOW_FORWARD_MIN_SPEED
            ),
            cec.CEC_PLAY_MODE_SLOW_FORWARD_MIN_SPEED:    (
                cec.CEC_PLAY_MODE_SLOW_FORWARD_MEDIUM_SPEED
            ),
            cec.CEC_PLAY_MODE_SLOW_FORWARD_MEDIUM_SPEED: (
                cec.CEC_PLAY_MODE_SLOW_FORWARD_MAX_SPEED
            )
        }
        if self.__deck_mode in playback_mapping:
            self.__deck_mode = playback_mapping[self.__deck_mode]
        else:
            self.__deck_mode = cec.CEC_PLAY_MODE_PLAY_FORWARD

    def pause(self):
        if self.__deck_mode == cec.CEC_PLAY_MODE_PLAY_STILL:
            self.__deck_mode = cec.CEC_PLAY_MODE_PLAY_FORWARD
        else:
            self.__deck_mode = cec.CEC_PLAY_MODE_PLAY_STILL

    def stop(self):
        if self.__deck_mode != cec.CEC_DECK_CONTROL_MODE_STOP:
            self.__deck_mode = cec.CEC_DECK_CONTROL_MODE_STOP

    def eject(self):
        self.__deck_mode = cec.CEC_DECK_CONTROL_MODE_STOP
        self.__deck_mode = cec.CEC_DECK_CONTROL_MODE_EJECT

    def rewind(self):
        playback_mapping = {
            cec.CEC_PLAY_MODE_SLOW_REVERSE_MIN_SPEED:    (
                cec.CEC_PLAY_MODE_SLOW_REVERSE_MEDIUM_SPEED
            ),
            cec.CEC_PLAY_MODE_SLOW_REVERSE_MEDIUM_SPEED: (
                cec.CEC_PLAY_MODE_SLOW_REVERSE_MAX_SPEED
            ),
            cec.CEC_PLAY_MODE_SLOW_REVERSE_MAX_SPEED:    (
                cec.CEC_PLAY_MODE_PLAY_REVERSE
            ),
            cec.CEC_PLAY_MODE_PLAY_REVERSE:              (
                cec.CEC_PLAY_MODE_FAST_REVERSE_MIN_SPEED
            ),
            cec.CEC_PLAY_MODE_FAST_REVERSE_MIN_SPEED:    (
                cec.CEC_PLAY_MODE_FAST_REVERSE_MEDIUM_SPEED
            ),
            cec.CEC_PLAY_MODE_FAST_REVERSE_MEDIUM_SPEED: (
                cec.CEC_PLAY_MODE_FAST_REVERSE_MAX_SPEED
            ),
        }
        if self.__deck_mode in playback_mapping:
            self.__deck_mode = playback_mapping[self.__deck_mode]
        else:
            self.__deck_mode = (
                cec.CEC_PLAY_MODE_SLOW_REVERSE_MIN_SPEED
            )

    def fastforward(self):
        playback_mapping = {
            cec.CEC_PLAY_MODE_FAST_FORWARD_MIN_SPEED:    (
                cec.CEC_PLAY_MODE_FAST_FORWARD_MEDIUM_SPEED
            ),
            cec.CEC_PLAY_MODE_FAST_FORWARD_MEDIUM_SPEED: (
                cec.CEC_PLAY_MODE_FAST_FORWARD_MAX_SPEED
            )
        }

        if self.__deck_mode in playback_mapping:
            self.__deck_mode = playback_mapping[self.__deck_mode]
        else:
            self.__deck_mode = (
                cec.CEC_PLAY_MODE_FAST_FORWARD_MIN_SPEED
            )

    def skip_forward(self):
        if (
            self.__deck_mode !=
            cec.CEC_DECK_CONTROL_MODE_SKIP_FORWARD_WIND
        ):
            self.__deck_mode = (
                cec.CEC_DECK_CONTROL_MODE_SKIP_FORWARD_WIND
            )

    def skip_back(self):
        if (
            self.__deck_mode !=
            cec.CEC_DECK_CONTROL_MODE_SKIP_REVERSE_REWIND
        ):
            self.__deck_mode = (
                cec.CEC_DECK_CONTROL_MODE_SKIP_REVERSE_REWIND
            )

    @property
    def status(self):
        command = self._adapter.raw_command(
            self._adapter.logical_address,
            self.logical_address,
            cec.CEC_OPCODE_GIVE_DECK_STATUS,
            cec.CEC_STATUS_REQUEST_ONCE
        )

        if command:
            self._reply_event.clear()
            self._reply_event.wait(5)
            if self._reply_event.isSet():
                response_opcode = command.GetResponseOpcode(
                    cec.CEC_OPCODE_GIVE_DECK_STATUS
                )
                reply = self._reply

                if response_opcode == reply.opcode:
                    response = reply.parameters.At(0)
                    self._reply = None
                    return self._adapter.DeckInfoToString(response).title()

        return 'Not Available'

    @property
    def __deck_mode(self):
        return self.__playback_speed

    @__deck_mode.setter
    def __deck_mode(self, mode):
        opcode = (
            cec.CEC_OPCODE_DECK_CONTROL
            if mode in CEC_OPCODE_DECK_CONTROL_MAPPING
            else cec.CEC_OPCODE_PLAY
        )

        command = self._adapter.raw_command(
            self._adapter.logical_address,
            self.logical_address,
            opcode,
            mode
        )

        if command and self._logical_address == self._adapter.logical_address:
            info = CEC_PLAYBACK_MAPPING[mode]
            if info is not None:
                self._adapter.SetDeckInfo(info)

        self.__playback_speed = mode

    def transmit_deck_info(self, destination, info):
        # CEC_DECK_INFO_PLAY
        # CEC_DECK_INFO_RECORD
        # CEC_DECK_INFO_PLAY_REVERSE
        # CEC_DECK_INFO_STILL
        # CEC_DECK_INFO_SLOW
        # CEC_DECK_INFO_SLOW_REVERSE
        # CEC_DECK_INFO_FAST_FORWARD
        # CEC_DECK_INFO_FAST_REVERSE
        # CEC_DECK_INFO_NO_MEDIA
        # CEC_DECK_INFO_STOP
        # CEC_DECK_INFO_SKIP_FORWARD_WIND
        # CEC_DECK_INFO_SKIP_REVERSE_REWIND
        # CEC_DECK_INFO_INDEX_SEARCH_FORWARD
        # CEC_DECK_INFO_INDEX_SEARCH_REVERSE
        # CEC_DECK_INFO_OTHER_STATUS
        # CEC_DECK_INFO_OTHER_STATUS_LG

        self._adapter.raw_command(
            self.logical_address,
            destination,
            cec.CEC_OPCODE_DECK_STATUS,
            info
        )

    def command_callback(self, command):
        if command.opcode == cec.CEC_OPCODE_DECK_STATUS:
            if not self._reply_event.isSet():
                self._reply = command
                self._reply_event.set()
            if self._enable_notifications:

                status = self._adapter.DeckInfoToString(
                    command.parameters.At(0)
                ).title().replace(' ', '')

                dispatcher.send(
                    PLAYER_STATUS_EVENT,
                    self._adapter[command.initiator],
                    device=self,
                    value=status
                )

                logger.debug(
                    'CEC.Player.{0}.Status.{1}'.format(self.osd_name, status)
                )

        elif command.opcode == cec.CEC_OPCODE_GIVE_DECK_STATUS:
            dispatcher.send(
                PLAYER_STATUS_EVENT,
                self._adapter[command.initiator],
                device=self,
                value=None
            )

            logger.debug(
                'CEC.Player.{0}.StatusRequest'.format(self.osd_name)
            )

        elif command.opcode == cec.CEC_OPCODE_DECK_CONTROL:
            status = self._adapter.DeckControlModeToString(
                command.parameters.At(0)
            )

            dispatcher.send(
                PLAYER_STATUS_EVENT,
                self._adapter[command.initiator],
                device=self,
                value=status
            )

            logger.debug(
                'CEC.Player.{0}.Request.{1}'.format(self.osd_name, status)
            )

        elif command.opcode == cec.CEC_OPCODE_PLAY:
            status = self._adapter.PlayModeToString(
                command.parameters.At(0)
            )

            dispatcher.send(
                PLAYER_STATUS_EVENT,
                self._adapter[command.initiator],
                device=self,
                value=status
            )

            logger.debug(
                'CEC.Player.{0}.Request.{1}'.format(self.osd_name, status)
            )

        else:
            PyCECDevice.command_callback(self, command)


class PyCECTuner(PyCECDevice):
    is_tuner = True

    def __init__(self, adapter, logical_address):

        self._enable_notifications = False

        PyCECDevice.__init__(self, adapter, logical_address)

    def transmit_tuner_status(self, destination, status):
        # CEC_TUNER_DISPLAY_INFO_DISPLAYING_DIGITAL_TUNER
        # CEC_TUNER_DISPLAY_INFO_NOT_DISPLAYING_TUNER
        # CEC_TUNER_DISPLAY_INFO_DISPLAYING_ANALOGUE_TUNER

        self._adapter.raw_command(
            self.logical_address,
            destination,
            cec.CEC_OPCODE_TUNER_DEVICE_STATUS,
            status
        )

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        self._connected = value
        if value and self._enable_notifications:
            self._adapter.raw_command(
                self._adapter.logical_address,
                self.logical_address,
                cec.CEC_OPCODE_GIVE_TUNER_DEVICE_STATUS,
                cec.CEC_STATUS_REQUEST_ON
            )

    def enable_notifications(self, value):
        if value and self.connected:
            self._enable_notifications = True
            self._adapter.raw_command(
                self._adapter.logical_address,
                self.logical_address,
                cec.CEC_OPCODE_GIVE_TUNER_DEVICE_STATUS,
                cec.CEC_STATUS_REQUEST_ON
            )

        elif not value:
            self._enable_notifications = False

            if self.connected:
                self._adapter.raw_command(
                    self._adapter.logical_address,
                    self.logical_address,
                    cec.CEC_OPCODE_GIVE_TUNER_DEVICE_STATUS,
                    cec.CEC_STATUS_REQUEST_OFF
                )

    enable_notifications = property(fset=enable_notifications)

    def command_callback(self, command):

        if command.opcode == cec.CEC_OPCODE_TUNER_DEVICE_STATUS:

            if not self._reply_event.isSet():
                self._reply = command
                self._reply_event.set()

            if self._enable_notifications:
                self._adapter.trigger_event(
                    '{0}.Tuner.{1}.Status'.format(
                        self.osd_name,
                        self._adapter.TunerStatusToString(
                            command.parameters.At(0)
                        ).title().replace(' ', '')
                    ),
                    self._adapter[command.initiator].osd_name
                )
        elif command.opcode == cec.CEC_OPCODE_GIVE_TUNER_DEVICE_STATUS:
            self._adapter.trigger_event(
                '{0}.Tuner.StatusRequest'.format(self.osd_name),
                self._adapter[command.initiator].osd_name
            )
        elif command.opcode == cec.CEC_OPCODE_TUNER_STEP_INCREMENT:
            self._adapter.trigger_event(
                '{0}.Tuner.ChannelUp.Request'.format(self.osd_name),
                self._adapter[command.initiator].osd_name
            )

        elif command.opcode == cec.CEC_OPCODE_TUNER_STEP_DECREMENT:
            self._adapter.trigger_event(
                '{0}.Tuner.ChannelDown.Request'.format(self.osd_name),
                self._adapter[command.initiator].osd_name
            )
        else:
            PyCECDevice.command_callback(self, command)

    def channel_up(self):
        self._adapter.raw_command(
            self._adapter.logical_address,
            self.logical_address,
            cec.CEC_OPCODE_TUNER_STEP_INCREMENT
        )

    def channel_down(self):
        self._adapter.raw_command(
            self._adapter.logical_address,
            self.logical_address,
            cec.CEC_OPCODE_TUNER_STEP_DECREMENT
        )

    @property
    def status(self):
        command = self._adapter.raw_command(
            self._adapter.logical_address,
            self.logical_address,
            cec.CEC_OPCODE_GIVE_TUNER_DEVICE_STATUS,
            cec.CEC_STATUS_REQUEST_ONCE
        )

        if command:
            self._reply_event.clear()
            self._reply_event.wait(5)
            if self._reply_event.isSet():
                response_opcode = command.GetResponseOpcode(
                    cec.CEC_OPCODE_GIVE_TUNER_DEVICE_STATUS
                )
                reply = self._reply
                if response_opcode == reply.opcode:
                    response = reply.parameters.At(0)
                    self._reply = None
                    return self._adapter.TunerStatusToString(response).title()

        return 'Not Available'

    # CEC_CHANNEL_NUMBER_FORMAT_MASK
    # CEC_1_PART_CHANNEL_NUMBER
    # CEC_2_PART_CHANNEL_NUMBER
    # CEC_MAJOR_CHANNEL_NUMBER_MASK
    # CEC_MINOR_CHANNEL_NUMBER_MASK
    # def tuner_analog(self, source, service, channel):
    #     if not self.is_tuner_device:
    #         raise AttributeError
    # CEC_OPCODE_SELECT_ANALOGUE_SERVICE
    # CEC_ANALOGUE_BROADCAST_TYPE_CABLE
    # CEC_ANALOGUE_BROADCAST_TYPE_SATELLITE
    # CEC_ANALOGUE_BROADCAST_TYPE_TERRESTIAL
    #     ANALOG_TUNER_SERVICES = [
    #         'PAL B/G',0
    #         'SECAM L`',1
    #         'PAL M',2
    #         'NTSC M',3
    #         'PAL I',4
    #         'SECAM DK',5
    #         'SECAM B/G',6
    #         'SECAM L',7
    #         'PAL DK',8
    #         'Other'31
    #     ]
    #     ANALOG_TUNER_SOURCES = [
    #         'Cable',
    #         'Satellite',
    #         'Terrestrial'
    #     ]
    #
    #     channel = '{0:04X}'.format(channel)
    #
    #     command = '{0:01X}{1:01X}:92:{2:02X}:{3}:{4}:{5:02X}'.format(
    #         self._adapter.logical_address,
    #         self.logical_address,
    #         source,
    #         channel[:2],
    #         channel[2:],
    #         service
    #     )
    #     self._adapter.raw_command(command)
    # CEC_OPCODE_SELECT_DIGITAL_SERVICE
    # def tuner_digital(self, channel, service, service_id, channel_format):
    #     if not self.is_tuner_device:
    #         raise AttributeError
    #
    #     if service_id:
    #         service += 128
    #         if channel_format:
    #             service_id = 8
    #             stream_id, program_number = channel[:2]
    #
    #             service_id += stream_id / 255
    #             stream_id %= 255
    #
    #             stream_id = '{0:04X}'.format(stream_id)
    #             program_number = '{0:04X}'.format(program_number)
    #             encoded_channel = '{0}:{1}:{2}:{3}'.format(
    #                 stream_id[:2],
    #                 stream_id[2:],
    #                 program_number[:2],
    #                 program_number[2:]
    #             )
    #         else:
    #             service_id = 4
    #             stream_id = channel[0]
    #             service_id += stream_id / 16384
    #             stream_id %= 255
    #             channel = '{0:04X}'.format()
    #             encoded_channel = '{0}:{1}'.format(channel[:2], channel[2:])
    #
    #     else:
    #         stream_id, program_number = channel[:2]
    #         stream_id = '{0:04X}'.format(stream_id)
    #         program_number = '{0:04X}'.format(program_number)
    #         encoded_channel = '{0}:{1}:{2}:{3}'.format(
    #             stream_id[:2],
    #             stream_id[2:],
    #             program_number[:2],
    #             program_number[2:]
    #         )
    #
    #
    #         if service not in (1, 16, 17, 18):
    #             network = channel[-1]
    #             network = '{0:04X}'.format(network)
    #             encoded_channel = '{0}:{1}:{2}'.format(
    #                 encoded_channel,
    #                 network[:2],
    #                 network[2:]
    #             )
    #
    #     command = '{0:01X}{1:01X}:93:{2:02X}:{3:02X}:{4}'.format(
    #         self._adapter.logical_address,
    #         self.logical_address,
    #         service,
    #         service_id,
    #         encoded_channel
    #     )
    #
    #     DIGITAL_TUNER_CHANNEL_IDS = [
    #         'Digital ID\'s',
    #         'Channels'
    #     ]
    #
    #     DIGITAL_TUNER_CHANNEL_FORMAT = [
    #         '1 Part Channel Number', 4
    #         '2 Part Channel Number' 8
    #     ]
    #
    #     DIGITAL_TUNER_SERVICES = {
    #         'ARIB generic': 0,
    #         'ATSC generic': 1,
    #         'DVB generic': 2,
    #         'ARIB BS': 8,
    #         'ARIB CS': 9,
    #         'ARIB T': 10,
    #         'ATSC Cable': 16,
    #         'ATSC Satellite': 17,
    #         'ATSC Terrestrial': 18,
    #         'DVB C': 24,
    #         'DVB S': 25,
    #         'DVB S2': 26,
    #         'DVB T': 27
    #     }
    #     DIGITAL_TUNER_SOURCES = [
    #         'Cable',
    #         'Satellite',
    #         'Terrestrial'
    #     ]
    #
    #     # (service, ID method, channel number format)
    #
    #     # 1 part channels 13:93:     90      :  08:38
    #     #                          service      channel
    #
    #     # 2 part channels 13:93:     90      :  08:38  :  00:07
    #     #                          service       major    minor
    #
    #     channel = '{0:04X}'.format(channel)
    #
    #
    #     self._adapter.raw_command(command)


class PyCECRecorder(PyCECDevice):
    is_recorder = True


CEC_DEVICE_MAPPING = {
    cec.CECDEVICE_UNKNOWN: None,
    cec.CECDEVICE_TV: PyCECTV,
    cec.CECDEVICE_RECORDINGDEVICE1: PyCECRecorder,
    cec.CECDEVICE_RECORDINGDEVICE2: PyCECRecorder,
    cec.CECDEVICE_TUNER1: PyCECTuner,
    cec.CECDEVICE_PLAYBACKDEVICE1: PyCECPlayer,
    cec.CECDEVICE_AUDIOSYSTEM: PyCECDevice,
    cec.CECDEVICE_TUNER2: PyCECTuner,
    cec.CECDEVICE_TUNER3: PyCECTuner,
    cec.CECDEVICE_PLAYBACKDEVICE2: PyCECPlayer,
    cec.CECDEVICE_RECORDINGDEVICE3: PyCECRecorder,
    cec.CECDEVICE_TUNER4: PyCECTuner,
    cec.CECDEVICE_PLAYBACKDEVICE3: PyCECPlayer,
    cec.CECDEVICE_RESERVED1: PyCECDevice,
    cec.CECDEVICE_RESERVED2: PyCECDevice,
    cec.CECDEVICE_FREEUSE: PyCECDevice,
    cec.CECDEVICE_UNREGISTERED: PyCECDevice
}


# noinspection PyMethodMayBeStatic,PyPep8Naming
class PyCECAdapter(object):

    @property
    def audio(self):
        value = self._adapter.AudioStatus()
        return value != cec.CEC_AUDIO_VOLUME_STATUS_UNKNOWN

    @audio.setter
    def audio(self, value):
        self._adapter.AudioEnable(bool(value))

    @property
    def source(self):
        for device in self:
            if device.active_source:
                return device.port

    @source.setter
    def source(self, port):
        packet = cec.cec_command()

        packet.Format(
            packet,
            4,
            15,
            130
        )

        address = (port * 16) * 256
        address = hex(address)[2:]
        address = list(
            int(address[i] + address[i + 1], 16)
            for i in range(0, len(address), 2)
        )

        for addr in address:
            packet.PushBack(addr)

        self._adapter.Transmit(packet)

    @property
    def mute(self):
        value = self._adapter.AudioStatus()

        if value == cec.CEC_AUDIO_VOLUME_STATUS_UNKNOWN:
            raise AttributeError

        return bool(value & cec.CEC_AUDIO_MUTE_STATUS_MASK)

    @mute.setter
    def mute(self, value):
        try:
            _ = self.mute
        except AttributeError:
            raise AttributeError

        if value:
            self._adapter.AudioMute()
        else:
            self._adapter.AudioUnmute()

    def toggle_mute(self):
        if self.audio:
            self._adapter.AudioToggleMute()
            return self.mute
        else:
            self.tv.toggle_mute()

    @property
    def volume(self):
        value = self._adapter.AudioStatus()

        if value == cec.CEC_AUDIO_VOLUME_STATUS_UNKNOWN:
            self.volume_down()
            self.volume_up()

            value = self._adapter.AudioStatus()
            if value == cec.CEC_AUDIO_VOLUME_STATUS_UNKNOWN:
                raise AttributeError

        return value & cec.CEC_AUDIO_VOLUME_STATUS_MASK

    @volume.setter
    def volume(self, value):
        try:
            _ = self.volume
        except AttributeError:
            raise AttributeError

        def do(new_volume):
            volume = self.volume

            start = time.time()

            while not time.time() - start < 11 and volume != new_volume:
                if new_volume < volume:
                    self._adapter.VolumeDown()

                elif new_volume > volume:
                    self._adapter.VolumeUp()

                volume = self.volume

        t = threading.Thread(target=do, args=(int(value),))
        t.daemon = True
        t.start()

    def volume_up(self):
        if self.audio:
            volume = self.volume + 1
            if volume < 101:
                self._adapter.VolumeUp()
                return self.volume
        else:
            self.tv.volume_up()

    def volume_down(self):
        if self.audio:
            volume = self.volume - 1
            if volume > -1:
                self._adapter.VolumeDown()
                return self.volume
        else:
            self.tv.volume_down()

    @property
    def power(self):
        for device in self:
            if device.power:
                return True
        return False

    @power.setter
    def power(self, value):
        if value:
            self._adapter.PowerOnDevices(cec.CECDEVICE_BROADCAST)
            for device in self:
                if device.connected and device.power not in (
                    cec.CEC_POWER_STATUS_IN_TRANSITION_STANDBY_TO_ON,
                    cec.CEC_POWER_STATUS_ON
                ):
                    device.power = True
        else:
            self._adapter.StandbyDevices(cec.CECDEVICE_BROADCAST)
            for device in self:
                if device.connected and device.power not in (
                    cec.CEC_POWER_STATUS_IN_TRANSITION_ON_TO_STANDBY,
                    cec.CEC_POWER_STATUS_STANDBY
                ):
                    device.power = False

    @property
    def name(self):
        return self.__cec_configuration.strDeviceName

    @property
    def port(self):
        return self.__cec_configuration.strComName

    @property
    def server_version(self):
        return self.VersionToString(
            self.__cec_configuration.serverVersion
        )

    @property
    def vendor(self):
        return self.VendorIdToString(
            self._adapter.GetAdapterVendorId()
        )

    @property
    def product_id(self):
        return self._adapter.GetAdapterProductId()

    @property
    def info(self):
        return self._adapter.GetLibInfo()

    @property
    def osd_name(self):
        return self._adapter.GetDeviceOSDName(self.logical_address)

    @osd_name.setter
    def osd_name(self, value):
        self._adapter.SetAdapterOSDName(value)

    @property
    def __devices(self):
        devices = self._adapter.GetActiveDevices()

        for i in range(16):
            cls = CEC_DEVICE_MAPPING[i]
            device = cls(self, i)
            if devices.IsSet(i):
                device.connected = True

            yield device

    def __contains__(self, item):
        for device in self.__devices:
            if item in (device.osd_name, device.logical_address):
                return True
        return False

    def __getitem__(self, item):
        if isinstance(item, (slice, int)):
            return list(self.__devices)[item]
        else:
            for device in self.__devices:
                if item == device.osd_name:
                    return device
            raise KeyError(item)

    def raw_command(
        self,
        initiator=None,
        destination=None,
        opcode=None,
        params=(),
        packet=None
    ):

        if packet is None:
            packet = cec.cec_command()
            cec.cec_command.Format(
                packet,
                initiator,
                destination,
                opcode
            )

            if not isinstance(params, (tuple, list)):
                params = [params]

            for param in params:
                packet.PushBack(param)

        return self._adapter.Transmit(packet)

    def __init__(self, cec_configuration):
        self._keypress = False
        self._command = False
        self._menu = False
        self._source = False
        self.lastKeyPressed = None
        cec_configuration.SetLogCallback(self.__log_callback)
        cec_configuration.SetMenuStateCallback(self.__menu_callback)
        cec_configuration.SetCommandCallback(self.__command_callback)
        cec_configuration.SetKeyPressCallback(self.__keypress_callback)
        cec_configuration.SetSourceActivatedCallback(self.__source_callback)

        self.__cec_configuration = cec_configuration
        self._adapter = cec.ICECAdapter.Create(cec_configuration)
        self._adapter.Open(cec_configuration.strComName)
        self.__menu_intercept = False
        self.__log_level = 0
        self._power_thread = None

        for device in self:
            if device.osd_name == cec_configuration.strDeviceName:
                self.__lib_cec_device_logical_address = device.logical_address
                break
        else:
            self.__lib_cec_device_logical_address = self.logical_address

        # print libCEC version and compilation information

        self._adapter.AudioEnable(cec_configuration.avr_audio)
        template = (
            'CEC Adapter Started\n'
            'Adapter Name: {adapter_name}\n'
            'Adapter Serial Port: {adapter_port}\n'
            'Adapter Device Emulation: {adapter_types}\n'
            'Available Devices: {device_names}\n'
            'AVR Volume Control: {avr_control}'
        )
        logger.info(
            template.format(
                adapter_name=cec_configuration.strDeviceName,
                adapter_port=cec_configuration.strComName,
                adapter_types=(
                    ', '.join(
                        self._adapter.DeviceTypeToString(adapter_type)
                        for adapter_type in cec_configuration.adapter_types)
                ),
                device_names=(
                    ', '.join(
                        device.osd_name for device in self if device.connected
                    )
                ),
                avr_control='On' if cec_configuration.avr_audio else 'Off'
            )
        )

    def __iter__(self):
        for device in self.__devices:
            yield device

    @property
    def lib_cec_device(self):
        return self[self.__lib_cec_device_logical_address]

    @property
    def logical_address(self):
        return self.__cec_configuration.logicalAddresses.primary

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if hasattr(self._adapter, item):
            return getattr(self._adapter, item)

        for device in self.__devices:
            if device.name.lower().replace(' ', '_') == item:
                return device

        if (
            item in PyCECAdapter.__dict__ and
            hasattr(PyCECAdapter.__dict__[item], 'fget') and
            PyCECAdapter.__dict__[item].fget is not None
        ):
            return PyCECAdapter.__dict__[item].fget(self)

        raise AttributeError(item)

    def keypress_events(self, value):
        self._keypress = value

    keypress_events = property(fset=keypress_events)

    def menu_events(self, value):
        self._menu = value

    menu_events = property(fset=menu_events)

    def command_events(self, value):
        self._command = value

    command_events = property(fset=command_events)

    def status_events(self, value):
        if value and self._power_thread is None:
            self._power_thread = EventThread(self, 0.2)
            self._power_thread.start()

        elif not value and self._power_thread is not None:
            self._power_thread.stop()
            self._power_thread = None

    status_events = property(fset=status_events)

    def source_events(self, value):
        self._source = value

    source_events = property(fset=source_events)

    def trigger_event(self, event, payload=None):
        logger.info('EVENT: {0} PAYLOAD: {1}'.format(event, payload))

    @property
    def menu_intercept(self):
        return self.__menu_intercept

    @menu_intercept.setter
    def menu_intercept(self, value):
        self.__menu_intercept = value

    @property
    def log_level(self):
        return self.__log_level

    @log_level.setter
    def log_level(self, value):
        if value > 5:
            value = 31
        self.__log_level = value

    def __menu_callback(self, logical_address, activated):
        if not self._menu:
            return True

        self.trigger_event(
            '{0}.Menu.{1}'.format(
                self[logical_address].osd_name,
                self._adapter.MenuStateToString(activated).title()
            )
        )

        return self.__menu_intercept

    def __source_callback(self, logical_address, activated):
        if not self._source:
            return 0

        status = self._adapter.MenuStateToString(not activated).title()

        dispatcher.send(
            TV_SOURCE_EVENT,
            self,
            device=self[logical_address],
            value=status
        )

        logger.debug(
            'CEC.{0}.Source.{1}'.format(self[logical_address].osd_name, status)
        )

        return 0

    def trigger_enduring_event(self, _):
        pass

    def end_last_event(self):
        pass

    # key press callback
    def __keypress_callback(self, key, _):
        if not self._keypress:
            return 0

        key = self._adapter.UserControlCodeToString(key).title()

        dispatcher.send(
            TV_REMOTE_EVENT,
            self,
            device=None,
            value=key
        )

        logger.debug(
            'CEC.RemoteKeyPress.{0}'.format(key)
        )

        return 0

    # command received callback
    def __command_callback(self, command):
        if not self._command:
            return 0
        if (
            command.opcode in
            (cec.CEC_OPCODE_DECK_STATUS, cec.CEC_OPCODE_TUNER_DEVICE_STATUS)
        ):
            device = list(self)[command.initiator]
        else:
            device = list(self)[command.destination]
        device.command_callback(command)
        return 0

    def __log_callback(self, level, _, message):
        if level > self.log_level:
            level = 0

        def dummy_logger(_):
            pass

        levels = {
            0:                   dummy_logger,
            cec.CEC_LOG_ERROR:   self.print_error,
            cec.CEC_LOG_WARNING: self.print_warning,
            cec.CEC_LOG_NOTICE:  self.print_notice,
            cec.CEC_LOG_TRAFFIC: self.print_info,
            cec.CEC_LOG_DEBUG:   self.print_debug
        }

        logger = levels[level]
        logger(message)

    def print_error(self, msg):
        logger.error(msg)

    def print_warning(self, msg):
        logger.warning(msg)

    def print_notice(self, msg):
        logger.info('NOTICE: ' + msg)

    def print_info(self, msg):
        logger.info(msg)

    def print_debug(self, msg):
        logger.debug(msg)

    def PlayModeToString(self, value):
        return PLAY_MODE_TO_STRING[value]

    def TunerStatusToString(self, value):
        return TUNER_STATUS_TO_STRING[value]

    def MenuLanguageToString(self, value):
        return ISO639_2[value]


def discover(config):
    str_com_name = getattr(config, 'strComName', None)
    if str_com_name is not None:
        return PyCECAdapter(config)

    for port in get_adapter_ports():
        if not str_com_name or str_com_name == port:
            logger.info("found a CEC adapter:")
            logger.info("port:     " + port)
            config.strComName = port
            return PyCECAdapter(config)

    logger.info('No CEC adapters found')


class PyCECConfiguration(cec.libcec_configuration):

    def __init__(
        self,
        adapter_name=None,
        adapter_port=None,
        adapter_types=None,
        power_off=None,
        power_standby=None,
        wake_avr=None,
        keypress_combo=None,
        keypress_combo_timeout=None,
        keypress_repeat=None,
        keypress_release_delay=None,
        keypress_double_tap=None,
        hdmi_port=None,
        avr_audio=False
    ):
        cec.libcec_configuration.__init__(self)

        if adapter_port is not None:
            self.strComName = str(adapter_port)

        # the version of the client that is connecting
        self.clientVersion = cec.LIBCEC_VERSION_CURRENT

        # 13 characters the device name to use on the CEC bus
        if adapter_name is None:
            adapter_name = 'SamsungTVCEC'

        if len(adapter_name) > 12:
            adapter_name = adapter_name[:12]

        self.strDeviceName = str(adapter_name)

        # the device type(s) to use on the CEC bus for libCEC
        # cec_device_type_list
        if adapter_types is None:
            adapter_types = [cec.CEC_DEVICE_TYPE_PLAYBACK_DEVICE]

        if not isinstance(adapter_types, (list, tuple)):
            adapter_types = [adapter_types]

        self.adapter_types = list(
            DEVICE_TYPES[adapter_type] for adapter_type in adapter_types
        )

        for adapter_type in self.adapter_types:
            self.deviceTypes.Add(adapter_type)

        # (read only) set to 1 by libCEC when the physical address
        # was auto detected
        # self.bAutodetectAddress =

        # the physical address of the CEC adapter
        # self.iPhysicalAddress =

        # the logical address of the device to which the adapter is connected.
        # only used when iPhysicalAddress = 0 or when the adapter doesn't
        # support auto detection cec_logical_address
        # self.baseDevice =

        # 1-15 the HDMI port to which the adapter is connected. only used when
        # iPhysicalAddress = 0 or when the adapter doesn't support
        # auto detection

        if hdmi_port is None:
            hdmi_port = 1

        self.iHDMIPort = hdmi_port

        # override the vendor ID of the TV. leave this untouched to autodetect
        # self.tvVendor =

        # list of devices to wake when initialising libCEC or when calling
        # PowerOnDevices() without any parameter. cec_logical_addresses
        # self.wakeDevices =

        # list of devices to power off when calling StandbyDevices() without
        # any parameter. cec_logical_addresses
        # self.powerOffDevices =

        # the version number of the server. read-only
        # self.serverVersion =

        # true to get the settings from the ROM
        # (if set, and a v2 ROM is present), false to use these settings.
        # self.bGetSettingsFromROM =

        # 0/1 make libCEC the active source on the bus when starting the player
        # application
        self.bActivateSource = 0

        # 0/1 put this PC in standby mode when the TV is switched off.
        # only used when bShutdownOnStandby = 0
        if power_standby is None:
            power_standby = False

        self.bPowerOffOnStandby = power_standby

        # 0/1 shuts down the PC when standby command is received
        if power_off is None:
            power_off = False

        self.bShutdownOnStandby = power_off

        # the object to pass along with a call of the callback methods.
        # NULL to ignore
        # self.callbackParam =

        # the callback methods to use. set this to NULL when not using
        # callbacks ICECCallbacks
        # self.callbacks =

        # (read-only) the current logical addresses.
        # added in 1.5.3 cec_logical_addresses
        # self.logicalAddresses =

        # (read-only) the firmware version of the adapter. added in 1.6.0
        # self.iFirmwareVersion =

        # the menu language used by the client. 3 character ISO 639-2
        # country code. see http://http://www.loc.gov/standards/iso639-2/
        # self.strDeviceLanguage = menu_language

        # (read-only) the build date of the firmware, in seconds since epoch.
        # if not available, this value will be set to 0. added in 1.6.2
        # self.iFirmwareBuildDate =

        # won't allocate a CCECClient when starting the connection when set
        # (same as monitor mode). added in 1.6.3
        # self.bMonitorOnly =

        # CEC spec version to use by libCEC. defaults to v1.4. added in 1.8.0
        # self.cecVersion =

        # type of the CEC adapter that we're connected to. added in 1.8.2
        # cec_adapter_type
        # self.adapterType =

        # key code that initiates combo keys.
        # defaults to CEC_USER_CONTROL_CODE_F1_BLUE.
        # CEC_USER_CONTROL_CODE_UNKNOWN to disable. cec_user_control_code

        if keypress_combo is None:
            keypress_combo = cec.CEC_USER_CONTROL_CODE_F1_BLUE

        self.comboKey = keypress_combo

        # timeout until the combo key is sent as normal keypress
        if keypress_combo_timeout is None:
            keypress_combo_timeout = 200

        self.iComboKeyTimeoutMs = keypress_combo_timeout

        # rate at which buttons auto repeat. 0 means rely on CEC device
        if keypress_repeat is None:
            keypress_repeat = 90

        self.iButtonRepeatRateMs = keypress_repeat

        # duration after last update until a button is considered released
        if keypress_release_delay is None:
            keypress_release_delay = 40

        self.iButtonReleaseDelayMs = keypress_release_delay

        # prevent double taps within this timeout. defaults to 200ms.
        # added in 4.0.0
        if keypress_double_tap is None:
            keypress_double_tap = 100

        self.iDoubleTapTimeoutMs = keypress_double_tap

        # set to 1 to automatically waking an AVR when the source is activated.
        # added in 4.0.0
        if wake_avr is None:
            wake_avr = False

        self.bAutoWakeAVR = wake_avr

        if avr_audio:
            self.baseDevice = cec.CECDEVICE_AUDIOSYSTEM
        else:
            self.baseDevice = cec.CECDEVICE_TV

        self.avr_audio = avr_audio


if __name__ == '__main__':
    # initialise libCEC
    config = PyCECConfiguration(
        adapter_name='Test',
        adapter_port='COM15',
        adapter_types=cec.CEC_DEVICE_TYPE_PLAYBACK_DEVICE,
        power_off=False,
        power_standby=False,
        wake_avr=False,
        keypress_combo=cec.CEC_USER_CONTROL_CODE_F1_BLUE,
        keypress_combo_timeout=200,
        keypress_repeat=90,
        keypress_release_delay=40,
        keypress_double_tap=100,
        avr_audio=True
    )
    lib = PyCECAdapter(config)

    print(lib.tv.power)

    if lib.tv.power == 1:

        lib.tv.power = True
        import time

        time.sleep(10.0)

    lib.audio = True

    # lib.log_level = 31
    lib.source_events = True
    lib.command_events = True
    lib.menu_events = True
    lib.keypress_events = True
    lib.deck_events = True
    lib.state_events = True
    # lib.tv.power = False
    #
    # time.sleep(5)
    # lib.tv.power = True
    # time.sleep(20)

    try:
        print('volume:', lib.volume)
    except AttributeError:
        print('volume not enabled')

    try:
        print('mute:', lib.mute)
    except AttributeError:
        print('mute not enabled')
    print('audio:', lib.audio)

    for _ in range(10):
        lib.volume_up()
        time.sleep(1)

    print('info:', lib.info)
    print('product_id:', lib.product_id)
    print('vendor:', lib.vendor)
    print('server_version:', lib.server_version)
    print('port:', lib.port)
    print('name:', lib.name)
    print('power:', lib.power)

    lib.tv.active_source = True

    lib.tv.volume_up()

    for dev in lib:
        if dev.active_device:
            print()
            print()
            print()
            print('name:', dev.name)
            print('power:', dev.power)
            # print 'type:', dev.type
            print('menu_language:', dev.menu_language)
            print('osd_name:', dev.osd_name)
            print('cec_version:', dev.cec_version)
            print('active_source:', dev.active_source)
            print('active_device:', dev.active_device)
            print('physical_address:', dev.physical_address)
            print('vendor:', dev.vendor)
            print('logical_address:', dev.logical_address)

    # lib.lib_cec_device.display_osd_message('Message', 30)
