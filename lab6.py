"""--------------------ι𝐍Ⓙย𝐬𝓣ᶤςⒺ Ⓐ𝐍ＹωᕼⒺг𝐄 ᶤ𝐬 ᵃ tｈяᗴＡт ⓉＯ 𝐣υ𝔰ｔ𝐢ᶜⓔ 𝐄V乇яｙ山卄εŘ乇 --------------------
Description:
 Checks the SHA-256 Hash value of VLC media player, installs the player only if the downloaded file
   hash value matches the expected hash value given from VideoLAN.
 
Usage:
 python lab6.py

---------------------ι𝐍Ⓙย𝐬𝓣ᶤςⒺ Ⓐ𝐍ＹωᕼⒺг𝐄 ᶤ𝐬 ᵃ tｈяᗴＡт ⓉＯ 𝐣υ𝔰ｔ𝐢ᶜⓔ 𝐄V乇яｙ山卄εŘ乇--------------------"""
import requests, hashlib, os, subprocess

def main():
    # Get the expected SHA-256 hash value of the VLC installer.
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website.
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values.
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer.
        run_installer(installer_path)

        # Delete the VLC installer from disk.
        delete_installer(installer_path)

def get_expected_sha256():
    # Send Get request to download file with expected hash value. 
    hash_file_url = 'https://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe.sha256'
    resp_msg = requests.get(hash_file_url)
    # Check if the download was successful.
    if resp_msg.status_code == requests.codes.ok:
        # Extract text file content from response message body.
        file_content = resp_msg.text
        # Split text file and extract hash value.
        hash_value = file_content.split()
    return hash_value[0]

def download_installer():
    # Send GET request to download file.
    file_url = 'https://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe'
    resp_msg = requests.get(file_url)
    # Check whether the download was successful.
    if resp_msg.status_code == requests.codes.ok:
        # Extract binary file content from response message body.
        file_content = resp_msg.content
        return file_content

def installer_ok(installer_data, expected_sha256):
    # Calculate SHA-256 hash value of download.
    sha256_value = hashlib.sha256(installer_data).hexdigest()
    # Check to see if expected hash value and downloaded hash value match.
    if expected_sha256 == sha256_value:
        print('Expected SHA-256 value matches downloaded SHA-256 Value.')
        return True
    else:
        print(f'SHA-256 Values do not match.\nExpected hash value is: {expected_sha256}.')
        print(f'Downloaded hash value is: {sha256_value}.\nPlease download file from a different source.')

def save_installer(installer_data):
    # Set Directory and file path.
    file_directory = r'C:\temp'
    file_path = 'vlc-3.0.18-win64.exe'
    installer_path = os.path.join(file_directory, file_path)
    # Create the Directory if it doesn't already exits.
    if not os.path.isdir(file_directory):
        os.makedirs(file_directory)
    # Write downloaded data to EXE file.    
    with open(installer_path, 'wb') as file:
        file.write(installer_data)
        return installer_path
  
def run_installer(installer_path):
    subprocess.run([installer_path, '/L=1033', '/S'], shell=True, check=True)
    
def delete_installer(installer_path):
    os.remove(installer_path)

if __name__ == '__main__':
    main()