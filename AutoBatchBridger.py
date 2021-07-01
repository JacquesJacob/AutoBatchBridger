import gnupg
import paramiko
import pprint
import os
import datetime


# variables to encrypt the batch file using Bridger PGP key.
GPG_BINARY = 'C:/Program Files (x86)/GnuPG/bin/gpg.exe'
GNUPGHOME = 'C:/Users/pellja02/Documents/AutoBatchPython/'  # all files must be here (.asc, .csv)

asc_file = [f for f in os.listdir(GNUPGHOME) if f.endswith('.asc')]
ASCFILE = GNUPGHOME + asc_file[0] # Bridger PGP key .asc file

csv_file = [f for f in os.listdir(GNUPGHOME) if f.endswith('.csv')]
BATCHFILE = GNUPGHOME + csv_file[0]
GPGFILE = BATCHFILE + '.gpg' # the .gpg file will be created here

# variables to send the batch file (encrypted) to Bridger SFTP server.
SFTPHOSTNAME = 'BridgerFTP.lexisnexis.com'
SFTPUSERNAME = 'USERNAME'
SFTPPASSWORD = 'PASSWORD'
SFTPPATH = f"./LoteTeste/{csv_file[0]}.gpg" # WARNING! The folder must exist
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
