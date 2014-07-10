import mails
import re
from collections import defaultdict

countmatrix = defaultdict(lambda: defaultdict(int))


def parse_product_list(input, product_a_users):
    mailcount = defaultdict(lambda: defaultdict(int))

    for line in input.splitlines():
        if line == '':
            continue
        qty, name = parse_product_a(line)
        for u in product_a_users:
            mailcount[u][name] += qty

    # Merge dictionaries
    for user, udict in mailcount.items():
        for product, qty in udict.items():
            countmatrix[u][product] += qty


def parse_product_a(input):
    match = re.match(r'(\d+)\s+([\w\s]+)', input)
    if not match:
        raise ValueError('\'%s\' is not a valid product a string' % input)

    return int(match.groups()[0]), match.groups()[1]


def main():
    server = mails.Mails(configFileName='../etc/config/mail.json')

    # Insert checking of the flags here
    buymails = server.get_mails('BUY', 'ALL')

    for uid, mail in buymails:
        users = mail.get('from', '')
        try:
            parse_product_list(mails.extract_text(mail), [users])
        except:
            server.imap.add_flags(uid, r'\FLAGGED')
    print(countmatrix)

if __name__ == '__main__':
    main()
