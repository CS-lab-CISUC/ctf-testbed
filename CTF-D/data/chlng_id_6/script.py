import os
import random

# Nome do ficheiro binário
filename = 'hidden_flag.cslab'

# Flag secreta
flag = b'CSLAB{H1dD3N_Beh1nD_3v3ryt1ng}'

# Gera dados aleatórios para "camuflar" a flag
def generate_random_bytes(size):
    return os.urandom(size)

# Tamanho total do ficheiro (em bytes)
file_size = 1024

# Posição aleatória para inserir a flag
flag_position = random.randint(0, file_size - len(flag))

# Cria o ficheiro binário
with open(filename, 'wb') as f:
    f.write(generate_random_bytes(flag_position))  # bytes antes da flag
    f.write(flag)                                   # a flag em si
    f.write(generate_random_bytes(file_size - flag_position - len(flag)))  # bytes após a flag

print(f'Ficheiro "{filename}" criado com sucesso!')
print(f'A flag está escondida. Boa sorte a encontrá-la!')