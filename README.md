# AES-flask-with-samba-server

Study and implementation of on-the-fly encryption and decryption techniques that allow you to take a file, encrypt it in AES (with a randomly generated password), save the encrypted file on a samba server and write the file's metadata to mondodb (file hash unencrypted, hash of the encrypted file, size, date and time, device, AES encryption password). Furthermore, the system must be able to take the files encrypted by samba, verify their integrity, decrypt with the psw AES, verify the integrity of the plain file and transfer the files in clear text to an sftp server. 

## Dependencies
1. Docker
2. MongoDB
3. Samba Server connected

## How to run

docker compose up --build

## How to verify

### Check Encryption 
`http://localhost:5010/upload`

### Check Decryption 
`http://localhost:5010/decryption`
