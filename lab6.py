import requests, hashlib, os, sys, subprocess

HASH_VALUE_URL = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.msi.sha256'
DOWNLOAD_URL = 'http://download.videolan.org/pub/videolan/vlc/3.0.17.4/win64/vlc-3.0.17.4-win64.msi'
def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    # Send Get request to download file. 
    file_url = HASH_VALUE_URL
    resp_msg = requests.get(file_url)
    # Check if GET request was successful
    if resp_msg.status_code == requests.codes.ok:
        # Extract text file content from response message body
        file_content = resp_msg.text
        # Split text file content into list
        hash_value = file_content.split()
    return hash_value[0]

def download_installer():
    # Send GET request to download file
    file_url = DOWNLOAD_URL
    resp_msg = requests.get(file_url)
    # Check whether the download was successful
    if resp_msg.status_code == requests.codes.ok:
        # Extract binary file content from response message body
        file_content = resp_msg.content
    return file_content

        
def installer_ok(installer_data, expected_sha256):
    # calculate SHA-256 hash value of download
    sha256_value = hashlib.sha256(installer_data).hexdigest()
    # Check to see if expected hash value and downloaded hash value match
    if expected_sha256 == sha256_value:
        print('Expected SHA-256 value matches downloaded SHA-256 Value.')
    else:
        print(f'SHA-256 Values do not match.\nExpected hash value is: {expected_sha256}.')
        print(f'The hash value of the downloaded file is: {hash_value}.\nPlease download file from a different source.')
        sys.exit()

def save_installer(installer_data):
    file_directory = r'C:\temp\installers'
    file_path = '.exe'
    installer_path = os.path.join(file_directory, file_path)
    if not os.path.isdir(installer_path):
        os.makedirs(installer_path)
        return installer_path
    with open(installer_path, 'wb') as file:
        file.write(installer_data)
    
def run_installer(installer_path):
    #subprocess.run([installer_path, '/L=1033', '/S'])
    return
    
def delete_installer(installer_path):
    #os.remove(installer_path)
    return

if __name__ == '__main__':
    main()