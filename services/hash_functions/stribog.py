import hashlib

def stribog(message):
    # Инициализация начального состояния
    h = [0] * 64
    n = len(message) * 8

    # Добавление длины сообщения в конец
    message += b'\x01'
    while len(message) % 64 != 56:
        message += b'\x00'
    message += n.to_bytes(8, 'little')

    # Обработка блоков по 64 байта
    for i in range(len(message) // 64):
        block = message[i*64 : (i+1)*64]
        w = [0] * 64

        # Инициализация блока
        for j in range(16):
            w[j] = int.from_bytes(block[j*4 : (j+1)*4], 'little')

        # Расширение блока
        for j in range(16, 64):
            s0 = (w[j-15] >> 1) ^ (w[j-15] << 63) ^ (w[j-15] >> 8)
            s1 = (w[j-2] >> 19) ^ (w[j-2] << 45) ^ (w[j-2] >> 61)
            w[j] = (s0 + w[j-7] + s1 + w[j-16]) & 0xFFFFFFFFFFFFFFFF

        # Инициализация переменных
        a = h[0]
        b = h[1]
        c = h[2]
        d = h[3]
        e = h[4]
        f = h[5]
        g = h[6]
        hh = h[7]

        # Сжатие блока
        for j in range(64):
            s0 = (a >> 28) ^ (a << 36) ^ (a >> 34)
            s1 = (e >> 14) ^ (e << 50) ^ (e >> 18)
            ch = (e & f) ^ (~e & g)
            maj = (a & b) ^ (a & c) ^ (b & c)
            t1 = hh + s1 + ch + k[j] + w[j]
            t2 = s0 + maj
            hh = g
            g = f
            f = e
            e = (d + t1) & 0xFFFFFFFFFFFFFFFF
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xFFFFFFFFFFFFFFFF

        # Обновление состояния
        h[0] = (h[0] + a) & 0xFFFFFFFFFFFFFFFF
        h[1] = (h[1] + b) & 0xFFFFFFFFFFFFFFFF
        h[2] = (h[2] + c) & 0xFFFFFFFFFFFFFFFF
        h[3] = (h[3] + d) & 0xFFFFFFFFFFFFFFFF
        h[4] = (h[4] + e) & 0xFFFFFFFFFFFFFFFF
        h[5] = (h[5] + f) & 0xFFFFFFFFFFFFFFFF
        h[6] = (h[6] + g) & 0xFFFFFFFFFFFFFFFF
        h[7] = (h[7] + hh) & 0xFFFFFFFFFFFFFFFF

    # Возвращение хэш-значения
    return b''.join([x.to_bytes(8, 'little') for x in h])


'''
# Пример использования
message = b'Hello, world!'
hash_value = stribog(message)
print(hash_value.hex())
'''