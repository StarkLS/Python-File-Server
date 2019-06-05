from socket import *

# variables
address = '172.30.150.239'
port = 7767
manual ='Hallo, Sie sind verbunden mit dem NAS-Pi, dem führenden Netzwerkspeicher der Welt.\n' \
        'Bitte wählen Sie unten Ihre Aktion aus\n' \
        '0 = Verbindung trennen\n' \
        '1 = Eine Datei auf dem NAS-Pi ablegen\n' \
        '2 = Eine Datei vom NAS-PI herunterladen\n' \
        '3 = Eine Datei auf dem NAS-Pi löschen\n4 = Dateien auf dem NAS-Pi anzeigen'

# define functions


def end():
    client.shutdown(SHUT_RDWR)
    client.close()


def list_files():
    client.send(action.encode())
    while True:
        data = client.recv(1024)
        element = data.decode()
        if element == 'final':
            print('Ende der Liste')
            break
        else:
            print('Datei ', element)
            client.send('angekommen'.encode())


def send_file():
    while True:
        local_file = input('Geben Sie den ganzen lokalen Pfad Ihrer Datei an: ')
        try:
            f = open(local_file, mode='rb')
        except FileNotFoundError:
            print('Die von Ihnen angegebene Datei existiert nicht')
            decsf = input('Möchten Sie es noch einmal versuchen? (j/n) ')
            if decsf == 'j':
                continue
            else:
                break
        client.send(action.encode())
        datei_name_nas = input('Geben Sie den gewünschten Namen der Datei auf dem NAS-Pi ein ')
        client.send(datei_name_nas.encode())
        client.send(f.read())
        f.close()
        print('Datei gesendet')
        break


def file_download():
    list_files()
    while True:
        download_file = str(input('Geben Sie den exakten Namen der gewünschten Datei ein '))
        client.send(download_file.encode())
        data = client.recv(1024)
        if data.decode() == 'True':
            client.send('ready for data'.encode())
            f = open(download_file, mode='wb')
            f.write(client.recv(1024))
            f.close()
            print('Datei ins Verzeichnis dieses Programms heruntergeladen')
            break
        else:
            print('Die gewünschte Datei existiert nicht')
            decision = str(input('Möchten Sie es nochmal probieren? (j/n)'))
            client.send(decision.encode())
            if decision == 'n':
                break

def file_delete():
    list_files()
    while True:
        delete_file = input('Geben Sie den Namen der zu löschenden Datei ein ')
        client.send(delete_file.encode())
        data = client.recv(1024).decode()
        if data == 'True':
            delfdes = str(input('Wollen Sie die Datei ' + delete_file + ' löschen? (j/n) '))
            if delfdes == 'j':
                client.send(delfdes.encode())
                print('Datei ', delete_file, ' gelöscht')
                break
            else:
                client.send(delfdes.encode())
                print('Löschen wird abgebrochen')
                break
        else:
            print('Die Datei existiert nicht')
            del_decision = str(input('Wollen Sie es nochmal versuchen? (j/n)'))
            client.send(del_decision.encode())
            if del_decision == 'n':
                break
            


# program


while True:
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((address, port))
    print(manual)
    action = str(input('Aktion = '))
    if action == '0':
        dec = input('Verbindung trennen?(j/n) ')
        if dec == 'j':
            print('Verbindung wird getrennt')
            client.send(action.encode())
            break
        else:
            pass
    if action == '1':
        send_file()
        end()
    elif action == '2':
        file_download()
        end()
    elif action == '3':
        file_delete()
        end()
    elif action == '4':
        list_files()
        end()
client.shutdown(SHUT_RDWR)
client.close()
