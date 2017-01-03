import random
from tkinter.filedialog import *
from Crypto.Cipher import AES
import base64

def open_file():
    op = askopenfile()
    op = str(op)
    st = op.find('name=') + 6
    fin = op.find('mode') - 2
    path = op[st:fin]
    return path

def to_bin(n):
    r = []
    while n > 0:
        r.append(n & 1)
        n //= 2
    return r

def test(a, n):
    b = to_bin(n - 1)
    k = 1
    for i in range(len(b) - 1, -1, -1):
        x = k
        k = (k * k) % n
        if k == 1 and x != 1 and x != n - 1:
            return True
        if b[i] == 1:
            k = (k * a) % n
    if k != 1:
        return True
    return False

def is_prime(n, bits):
    if n == 1:
        return False
    for j in range(0, bits):
        a = random.randint(2, n - 1)
        if test(a, n):
            return False
    return True

def gen_p(bits):
    while True:
        p = random.randint(2 ** (bits - 2), 2 ** (bits - 1))
        while p % 2 == 0:
            p = random.randint(2 ** (bits - 2), 2 ** (bits - 1))
        while not is_prime(p, bits):
            p = random.randint(2 ** (bits - 2), 2 ** (bits - 1))
            while p % 2 == 0:
                p = random.randint(2 ** (bits - 2), 2 ** (bits - 1))
        p = p * 2 + 1
        if is_prime(p, bits):
            return p

if __name__  == '__main__':
    print("Привееет :)")
    BLOCK_SIZE = 32
    PADDING = '{'
    mode = input("Выбери режим выполнения программы:\n1 - генерация группы ключей\n2 - шифрование\n3 - дешифрование\n4 - выход из программы ")
    while True:
        if mode == "1":
            n = int(input("Будь так добр, введи количество пользователей: "))
            p = gen_p(256)
            g = random.randint(2, p - 1)
            x = []
            a = []
            for i in range(0, n):
                x.append(random.randint(2, p - 1))
            for i in range(0, n):
                ax = g
                for j in range(0, n):
                    if i != j:
                        ax = pow(ax, x[j], p)
                a.append(ax)
            for i in range(0, n):
                open(str(i+1), 'tw', encoding='utf-8').close()
                ff = open(str(i+1), 'w')
                ff.write(str(p) + " " + str(x[i]) + " " + str(a[i]))
                ff.close()

        elif mode == "2":
            print("Выбери файл для шифрования")
            path = open_file()
            f = open(path, 'rb')
            plaintext = f.read()
            f.close()
            print("Красава. Теперь выбери файл с ключом")
            f = open(open_file(), 'r')
            keytext = f.read()
            f.close()

            keytextsplt = str(keytext).split()
            p = int(keytextsplt[0])
            x = int(keytextsplt[1])
            a = int(keytextsplt[2])
            key = pow(a, x, p)

            pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING.encode(encoding='utf-8')
            EncAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
            cipher = AES.new((key).to_bytes(32, byteorder='big'))
            ciphertext = EncAES(cipher, plaintext)
            open(path + '.enc', 'tw', encoding='utf-8').close()
            f = open(path + '.enc', 'wb')
            f.write(bytes(ciphertext))
            f.close()

        elif mode == "3":
            print("Выбери файл для дешифрования")
            path = open_file()
            f = open(path, 'rb')
            ciphertext = f.read()
            f.close()
            print("Молорик. Теперь настала очередь файлика с ключом")
            f = open(open_file(), 'r')
            keytext = f.read()
            f.close()

            keytextsplt = str(keytext).split()
            p = int(keytextsplt[0])
            x = int(keytextsplt[1])
            a = int(keytextsplt[2])
            key = pow(a, x, p)

            pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING.encode(encoding='utf-8')
            DecAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING.encode(encoding='utf-8'))
            cipher = AES.new((key).to_bytes(32, byteorder='big'))
            plaintext = DecAES(cipher, ciphertext)
            open(path[:-4] + '.dec', 'tw', encoding='utf-8').close()
            f = open(path[:-4] + '.dec', 'wb')
            f.write(plaintext)
            f.close()

        elif mode == "4":
            print("Ну ты это, заходи, если что")
            exit(0)

        else:
            print("Нет такого режима, братишка ;)")

        mode = input("Выбери режим: ")