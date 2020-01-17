import xml.etree.ElementTree as ET
import requests

class Upnp:
    def __init__(self, config):
        self._host = config['host']
        self.mute = False
        self.volume = 0
    
    def SOAPrequest(self, action, arguments, protocole):
        headers = {'SOAPAction': '"urn:schemas-upnp-org:service:{protocole}:1#{action}"'.format(action=action, protocole=protocole), 'content-type': 'text/xml'}
        body = """<?xml version="1.0" encoding="utf-8"?>
                <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
                    <s:Body>
                    <u:{action} xmlns:u="urn:schemas-upnp-org:service:{protocole}:1">
                        <InstanceID>0</InstanceID>
                        {arguments}
                    </u:{action}>
                    </s:Body>
                </s:Envelope>""".format(action=action, arguments=arguments, protocole=protocole)
        response = None
        try:
            response = requests.post("http://{host}:9197/upnp/control/{protocole}1".format(host=self._host, protocole=protocole), data=body, headers=headers, timeout=0.2)
            response = response.content
        except:
            pass
        return response

    def get_volume(self):
        self.volume = 0
        response = self.SOAPrequest('GetVolume', "<Channel>Master</Channel>", 'RenderingControl')
        if (response is not None):
            volume_xml = response.decode('utf8')
            tree = ET.fromstring(volume_xml)
            for elem in tree.iter(tag='CurrentVolume'):
                self.volume = elem.text
        return self.volume
    
    def set_volume(self, volume):
        self.SOAPrequest('SetVolume', "<Channel>Master</Channel><DesiredVolume>{}</DesiredVolume>".format(volume), 'RenderingControl')
    
    def get_mute(self):
        self.mute = False
        response = self.SOAPrequest('GetMute', "<Channel>Master</Channel>", 'RenderingControl')
        if (response is not None):
            mute_xml = response.decode('utf8')
            tree = ET.fromstring(mute_xml)
            for elem in tree.iter(tag='CurrentMute'):
                mute = elem.text
            if (int(mute) == 0):
                self.mute = False
            else:
                self.mute = True
        return self.mute

    def set_current_media(self, url):
        """ Set media to playback."""
        self.SOAPrequest('SetAVTransportURI', "<CurrentURI>{url}</CurrentURI><CurrentURIMetaData></CurrentURIMetaData>".format(url=url), 'AVTransport')

    def play(self):
        """ Play media that was already set as current."""
        self.SOAPrequest('Play', "<Speed>1</Speed>", 'AVTransport')