# -*- coding: utf-8 -*-

ENVELOPE_XMLNS = 'http://schemas.xmlsoap.org/soap/envelope/'


def strip_xmlns(root):
    def iter_node(n):
        nsmap = n.nsmap
        for child in n:
            nsmap.update(iter_node(child))
        return nsmap

    xmlns = list('{' + item + '}' for item in iter_node(root).values())

    def strip_node(n):
        for item in xmlns:
            n.tag = n.tag.replace(item, '')

        for child in n[:]:
            try:
                strip_node(child)
            except AttributeError:
                n.remove(child)
    strip_node(root)

    return root
