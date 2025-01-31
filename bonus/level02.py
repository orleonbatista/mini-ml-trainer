import itertools
import subprocess

def calculate_local_30(password):
    local_30 = 0x1337
    for char in password:
        local_30 ^= (ord(char) * 0x1234)
    return local_30

def validate_password(password):
    target_value = 0xa48b7
    calculated_value = calculate_local_30(password)
    return calculated_value == target_value

def test_password_with_level02(password):
    try:
        process = subprocess.run(
            ['./level02'], input=password, text=True, capture_output=True
        )
        output = process.stdout + process.stderr
        if "Well Done!" in output:
            return True, output
        else:
            return False, output
    except FileNotFoundError:
        print("Erro: Certifique-se de que o binário 'level02' está no mesmo diretório e tem permissão de execução.")
        return False, ""

def find_and_test_password():
    target_value = 0xa48b7
    password_length = 21

    valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+{}[];:'\"<>,.?/|"

    for candidate in itertools.product(valid_chars, repeat=password_length):
        candidate_password = ''.join(candidate)
        if calculate_local_30(candidate_password) == target_value:
            print(f"Testando senha: {candidate_password}")
            valid, output = test_password_with_level02(candidate_password)
            if valid:
                return candidate_password, output

    return None, None

if __name__ == "__main__":
    password, output = find_and_test_password()
    if password:
        print(f"Senha aceita pelo level02: {password}")
        print("Saída do programa:")
        print(output)
    else:
        print("Nenhuma senha encontrada que funcione no level02.")