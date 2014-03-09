import json
from imapclient import IMAPClient
from getpass import getpass
from email import message_from_string


class Mails:

    def __init__(self, host=None, port=None, ssl=False, configFileName=None):
        """ Initialize and connect to the imap server

        An IMAPClient instance is created and connected to using the given
        arguments

        Keyword arguments:
        host -- (mandatory) The URI of the IMAP server
        port -- (mandatory) The port of the IMAP server
        ssl -- (optional) If SSL should be used
        configFileName -- (optional) Can be used instead of the other arguments
        configFileName should be the file name of a JSON file of the following
        type: {"imap": {SSL, host, username, password}} with the inner pairs
        representing key-value pairs of the keyword arguments not stated."""
        if configFileName:
            # Read from config file
            with open(configFileName, 'r') as configFile:

                config = json.load(configFile)
                ssl = config['imap'].get('SSL', False)
                host = config['imap']['host']
                port = config['imap'].get('port', None)
                password = config['imap']['password'] \
                    if 'password' in config['imap'] \
                    else None

        # Retrieve password from command line
        if password is None:
            password = getpass()

        # Generate imap server class
        print('Connecting to server')
        self.imap = IMAPClient(host, ssl=ssl, port=port, use_uid=True)

        # Try login
        print('Authenticating')

        self.imap.login(config['imap']['username'], password)

    def getMails(self, mailbox='INBOX', criterion='ALL'):
        """ Return a list of mail messages matching the arguments

        Keyword arguments:
        mailbox -- name of the mailbox
        criterion -- IMAP search criterion
        """
        self.imap.select_folder(mailbox)
        uids = self.imap.search(criterion)
        mails = self.imap.fetch(uids, ['RFC822'])
        emails = [message_from_string(m['RFC822']) for m in mails.values()]
        return emails


def extract_text(mail):
    """Return all plaintext in the mail as one string

    Iterate through the parts of the message while concatenating all
    text/plain parts to the returned string
    """
    result_string = ''
    for part in mail.walk():
        if part.get_content_type() == 'text/plain':
            result_string += part.get_payload()
    return result_string


if __name__ == '__main__':
    server = Mails(configFileName='mail.json')
