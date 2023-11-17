import subprocess
import string
import random
import re
import argparse

def get_random_mac_address():
    """Generate dan Mengembalikan alamat MAC dalam format Linux."""
    # Dapatkan hexdigits yang di-uppercased
    uppercased_hexdigits = "".join(set(string.hexdigits.upper()))

    # Karakter kedua harus 0, 2, 4, 6, A, C, atau E
    mac = ""
    for i in range(6):
        for j in range(2):
            if i == 0:
                mac += random.choice("02468ACE")
            else:
                mac += random.choice(uppercased_hexdigits)
        mac += ":"
    return mac.strip(":")

def get_current_mac_address(iface):
    # Gunakan perintah IFconfig untuk mendapatkan detail antarmuka, termasuk Alamat MAC
    output = subprocess.check_output(f"ifconfig {iface}", shell=True).decode()
    return re.search("ether(.+)", output).group().split()[1].strip()

def change_mac_address(iface, new_mac_address):
    # Nonaktifkan antarmuka jaringan
    subprocess.check_output(f"ifconfig {iface} down", shell=True)
    # Ubah MAC
    subprocess.check_output(f"ifconfig {iface} hw ether {new_mac_address}", shell=True)
    # Aktifkan kembali antarmuka jaringan
    subprocess.check_output(f"ifconfig {iface} up", shell=True)

if __name__ == "__main__":
    # Parse argumen baris perintah
    parser = argparse.ArgumentParser(description="Pengganti MAC Python pada Linux")
    parser.add_argument("Interface", help="Nama antarmuka jaringan di Linux")
    parser.add_argument("-r", "--random", action="store_true", help="Apakah ingin menghasilkan Alamat MAC acak")
    parser.add_argument("-m", "--mac", help="MAC baru yang ingin diubah")

    args = parser.parse_args()
    iface = args.Interface
    if args.random:
        # Jika parameter acak diatur, hasilkan MAC acak
        new_mac_address = get_random_mac_address()
    elif args.mac:
        # Jika MAC diatur, gunakan yang tersebut
        new_mac_address = args.mac
    # Dapatkan Alamat MAC saat ini
    old_mac_address = get_current_mac_address(iface)
    print(f"[*] Alamat MAC Lama: ", old_mac_address)
    # Ubah Alamat MAC
    change_mac_address(iface, new_mac_address)
    # Periksa apakah benar-benar berubah
    new_mac_address = get_current_mac_address(iface)
    print("[+] Alamat MAC Baru: ", new_mac_address)
