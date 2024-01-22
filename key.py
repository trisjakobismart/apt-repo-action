import logging
import os
import sys
import gnupg  # Make sure this is python-gnupg

def detectPublicKey(key_dir):
    logging.info('Detecting public key')

    public_key_path = os.path.join(key_dir, 'public.key')
    logging.debug(f'Looking for public key at {public_key_path}')

    if not os.path.isfile(public_key_path):
        logging.error(f'Public key file not found at {public_key_path}')
        sys.exit(1)

    with open(public_key_path, 'r') as key_file:
        pub_key = key_file.read()

    logging.debug('Trying to import key')
    
    gpg = gnupg.GPG(options=['--yes', '--always-trust'])
    public_import_result = gpg.import_keys(pub_key)

    if not public_import_result.fingerprints or len(public_import_result.fingerprints) != 1:
        logging.error('Invalid public key provided, please provide 1 valid key')
        sys.exit(1)

    logging.info('Public key valid')

def importPrivateKey(sign_key):
    logging.info('Importing private key')

    gpg = gnupg.GPG(options=['--yes', '--always-trust'])
    private_import_result = gpg.import_keys(sign_key)

    if not private_import_result.fingerprints or len(private_import_result.fingerprints) != 1:
        logging.error('Invalid private key provided, please provide 1 valid key')
        sys.exit(1)

    private_key_id = private_import_result.fingerprints[0]
    logging.info('Private key valid')
    logging.debug(f'Key id: {private_key_id}')

    logging.info('-- Done importing key --')

    return private_key_id
