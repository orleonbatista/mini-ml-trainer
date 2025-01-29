
# **Bonus**

## **Level01**

## **1. Analisando o Executável com `strings`**
A primeira abordagem para encontrar informações úteis em um binário é usar o comando `strings`, que exibe cadeias de caracteres legíveis armazenadas no arquivo binário.

```sh
strings level01
```

### **Saída relevante do comando `strings`**
```plaintext
...
Enter your secret password:
Well Done! This is the password: %s
This is not the password :(
...
1F00d{P1H
3c3_0f_CH
4k3}
...
```
Observamos que há algumas strings que parecem suspeitas:
- `"Enter your secret password:"`
- `"Well Done! This is the password: %s"`
- `"This is not the password :("`
- `"1F00d{P1H"`
- `"3c3_0f_CH"`
- `"4k3}"`

A sequência **"1F00d{P1H3c3_0f_C4k3}"** parece ser uma senha ou um token.

---

## **2. Rastreando Chamadas de Função com `ltrace`**
A ferramenta `ltrace` permite monitorar as chamadas de funções de bibliotecas dinâmicas feitas pelo executável. Executamos o comando:

```sh
ltrace ./level01
```

### **Saída relevante do `ltrace`**
```plaintext
printf("Enter your secret password: ") = 28
__isoc99_scanf(0x55e226478025, 0x7ffc117aecb0, 0, 0x55e226478024Enter your secret password: 123
) = 1
strcmp("123", "1F00d{P13c3_0f_C4k3}") = -20
puts("This is not the password :(")
```
O trecho `strcmp("123", "1F00d{P13c3_0f_C4k3}")` confirma que a senha esperada pelo programa é **`1F00d{P13c3_0f_C4k3}`**.

---

## **3. Testando a Senha Descoberta**
Agora que temos a senha, podemos testá-la executando o programa e inserindo `1F00d{P13c3_0f_C4k3}` como entrada.

```sh
./level01
```

### **Entrada**
```plaintext
Enter your secret password: 1F00d{P13c3_0f_C4k3}
```

### **Saída Esperada**
```plaintext
Well Done! This is the password: 1F00d{P13c3_0f_C4k3}
```

Isso confirma que encontramos a senha correta.

---

## **Resumo da Metodologia Utilizada**
| Passo | Ferramenta | Descrição |
|-------|-----------|-----------|
| 1 | `strings` | Extraiu strings legíveis do binário, revelando fragmentos da senha. |
| 2 | `ltrace` | Monitorou chamadas de funções, expondo a comparação da senha dentro do código. |
| 3 | **Execução** | Testamos a senha identificada para verificar sua autenticidade. |

---


## **Level02**

## **1. Analisando o Executável com Ghidra**
Para entender a lógica do binário, utilizei o **Ghidra**, uma ferramenta de engenharia reversa desenvolvida pela NSA ([https://ghidra-sre.org/](https://ghidra-sre.org/)).

No código descompilado, identifiquei que:

1. A senha precisa ter **exatamente 21 caracteres**:
   ```c
   sVar1 = strlen(local_28);
   if (sVar1 == 0x15) { // 0x15 == 21
   ```

2. O programa realiza um cálculo iterativo em cada caractere da senha:
   ```c
   local_30 = 0x1337;
   for (i = 0; i < 21; i++) {
       local_30 = local_30 ^ (local_28[i] * 0x1234);
   }
   ```

3. No final, ele verifica se `local_30` é igual a `0xa48b7`:
   ```c
   if (local_30 == 0xa48b7) {
       printf("Well Done! This is the password: %s\n", local_28);
   }
   ```
   Se a condição for atendida, o programa exibe a senha como correta.

---

## **2. Gerando a Senha com um Script Python**
Com base na análise do código, desenvolvi um script em **Python** para encontrar a senha correta. O script (`level02.py`) segue a lógica extraída:

1. **Gera todas as combinações possíveis de senhas de 21 caracteres**.
2. **Aplica a mesma lógica de cálculo do programa**.
3. **Testa diretamente no executável `level02` via subprocess**.

O código tenta otimizar as combinações restringindo-se a **caracteres alfanuméricos e símbolos comuns**.

### **Referência ao Script**
Consulte o código-fonte completo no arquivo [`level02.py`](level02.py).

---

## **3. Testando a Senha Descoberta**
Após a execução do script, encontramos a senha correta:  

```plaintext
AAAAAAAAAAAAAAAAAABY{
```

Testamos a senha diretamente no desafio:

```sh
./level02
```

### **Entrada**
```plaintext
Enter your secret password: AAAAAAAAAAAAAAAAAABY{
```

### **Saída Esperada**
```plaintext
Well Done! This is the password: AAAAAAAAAAAAAAAAAABY{
```

---

## **Resumo da Metodologia Utilizada**
| Passo | Ferramenta | Descrição |
|-------|-----------|-----------|
| 1 | `Ghidra` | Análise do código-fonte descompilado, identificação da lógica de senha. |
| 2 | `Python` | Implementação do script (`level02.py`) para encontrar a senha correta. |
| 3 | **Execução** | Teste direto no programa `level02` para validar a senha. |

---

## **Level03**

1. Analisando o Executável

Para entender a lógica do binário, utilizei ferramentas de engenharia reversa como Ghidra e GDB.

No código descompilado, identifiquei que:

O buffer de entrada tem apenas 10 bytes:

undefined local_12[10];

A função scanf não limita o tamanho da entrada do usuário:

__isoc99_scanf(&DAT_00102021, local_12);

Isso permite um buffer overflow, possibilitando a sobrescrita do endereço de retorno (RIP).

USAR COMO REFERENCIA NOS TESTES:
https://0xrick.github.io/binary-exploitation/bof5/
