import gnupg
import paramiko
import pprint
import os
import datetime


# variables to encrypt the batch file using Bridger PGP key.
GPG_BINARY = 'C:/Program Files (x86)/GnuPG/bin/gpg.exe'
GNUPGHOME = 'C:/Users/pellja02/Documents/AutoBatchPython/'
ASCFILE = 'C:/Users/pellja02/Documents/AutoBatchPython/BridgerInsightXG.asc' # Bridger PGP Key
BATCHFILE = 'C:/Users/pellja02/Documents/AutoBatchPython/individual.csv'
GPGFILE = BATCHFILE + '.gpg'

# variables to send the batch file (encrypted) to Bridger SFTP server.
SFTPHOSTNAME = 'SFTPHOSTNAME or IP'
SFTPUSERNAME = 'USERNAME'
SFTPPASSWORD = 'PASSWORD'
SFTPPATH = "./LoteTeste/individual.csv.gpg" # the folder must exist
SFTPLOG = "C:/Users/pellja02/Documents/AutoBatchPython/sftp.log"

try:
    gpg = gnupg.GPG(gpgbinary=GPG_BINARY, gnupghome=GNUPGHOME, secret_keyring=False)
    key_data = open(ASCFILE).read()
    import_result = gpg.import_keys(key_data)

    gpg1 = gnupg.GPG(gnupghome=GNUPGHOME)
    output = GPGFILE
    with open(BATCHFILE, 'rb') as f:
        status = gpg1.encrypt_file(
            f, import_result.fingerprints, output=output, always_trust=True, passphrase=False)

    print('File read: ', status.ok)
    print('Encryption status: ', status.status)
    print('Encryption output: ', status.stderr)
    print('Encrypted Batch filename: ', output)

except:
    print("Error encrypting. Check the log files!")

try:

    port = 22
    paramiko.util.log_to_file(SFTPLOG)
    # Open a transport
    transport = paramiko.Transport(SFTPHOSTNAME, port)

    # Auth
    transport.connect(None, SFTPUSERNAME, SFTPPASSWORD)

    # Go!
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Upload
    filepath = SFTPPATH
    localpath = GPGFILE
    sftp.put(localpath, filepath)

    # Close
    sftp.close()
    transport.close()

    print("The file was uploaded successfully! For more details see the file sftp.log.")

except:
    print("Error sending! Check the sftp log file.")

datetime_object = datetime.datetime.now()
print("Process completed ", datetime_object)
