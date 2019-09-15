from cryptography.fernet import Fernet
from os.path import dirname, abspath

HOME = '/'.join(abspath(dirname(__file__)).split('/')[:3])


if __name__ == "__main__":
    
    # generate encryption key
    key = Fernet.generate_key()
    with open(f'{HOME}/.chat-app.key', 'wb') as f:
        f.write(key)
    
    # get user info
    os.system("stty -echo")
    password = input('Password: ')
    os.system("stty echo")
    print()
       
    bytes_info = password.encode("utf-8")
    fernet = Fernet(key)
    encrypted = fernet.encrypt(bytes_info)

    with open(f'{HOME}/.chat-app-user-secrets', 'wb') as f:
        f.write(encrypted) 
