#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import qrcode
import sys


def generate_mail_code(to, **kwargs):
    """
    Generates a qr code sending a mail

    to -- Adress or list of adresses as string
    kwargs (cc, bcc, subject, body)
    """

    query = '&'.join(map(lambda x: '='.join(x), kwargs.items()))
    string = "mailto:%s?%s" % (to, query)
    return qrcode.make(string)


if __name__ == '__main__':
    import argparse
    import json

    parser = argparse.ArgumentParser('Create qrcodes for products')
    parser.add_argument('file', type=argparse.FileType('r'))
    opt = parser.parse_args()

    try:
        products = json.load(opt.file)
    except ValueError as err:
        print('Error parsing %s:\n%s' % (opt.file.name, err))
        sys.exit()

    for p in products:
        print(p)
        qr = generate_mail_code('kaffee@goth-1.de',
                                subject='BUY', body='1 %s' % p)
        qr.save("%s.png" % p)
