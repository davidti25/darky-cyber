# 🛡️ Write-up: OverTheWire Bandit (Níveis 0 ao 5)

> **Desafio:** [OverTheWire Wargames - Bandit](https://overthewire.org/wargames/bandit/)  
> **Objetivo:** Adquirir fluência em terminal Linux, navegação, leitura de arquivos com caracteres especiais e investigação inicial.  
> **Portfólio:** [Darky Cyber](../../README.md) | Sprint 01

---

## 📌 Bandit Nível 0 ➔ Nível 1

* **Objetivo:** Conectar via SSH ao servidor de desafio e capturar a senha armazenada no arquivo `readme`.
* **Comando de Conexão:**
  ```bash
  ssh bandit0@bandit.labs.overthewire.org -p 2220
  # Senha: bandit0
  ```
* **Comandos Utilizados:**
  ```bash
  ls -la
  cat readme
  ```
* **Conceito Aprendido:** Conexão remota segura via SSH em porta não-padrão (`2220`) e leitura de arquivos de texto simples.
* **Flag / Senha Bandit 1:** *(Aguardando resolução)*

---

## 📌 Bandit Nível 1 ➔ Nível 2

* **Objetivo:** Ler a senha armazenada em um arquivo chamado `-` localizado no diretório home.
* **Desafio Técnico:** O comando `cat -` interpreta o hífen como entrada padrão (`stdin`), ficando preso esperando digitação.
* **Solução:**
  ```bash
  cat ./-
  ```
* **Conceito Aprendido:** Referenciamento relativo explícito de caminhos (`./`) para contornar interpretação de flags no shell.
* **Flag / Senha Bandit 2:** *(Aguardando resolução)*

---

## 📌 Bandit Nível 2 ➔ Nível 3

* **Objetivo:** Ler a senha contida em um arquivo cujo nome contém espaços (`spaces in this filename`).
* **Solução:**
  ```bash
  cat "spaces in this filename"
  # ou usando escape:
  cat spaces\ in\ this\ filename
  ```
* **Conceito Aprendido:** Tratamento de espaços e caracteres especiais em nomes de arquivos (*quoting* e *escaping*).
* **Flag / Senha Bandit 3:** *(Aguardando resolução)*

---

## 📌 Bandit Nível 3 ➔ Nível 4

* **Objetivo:** Encontrar a senha escondida dentro do diretório `inhere`.
* **Desafio Técnico:** O arquivo está oculto (inicia com um ponto `.`).
* **Solução:**
  ```bash
  cd inhere
  ls -la
  cat .hidden
  ```
* **Conceito Aprendido:** Arquivos ocultos no Linux e a importância da flag `-a` no comando `ls`.
* **Flag / Senha Bandit 4:** *(Aguardando resolução)*

---

## 📌 Bandit Nível 4 ➔ Nível 5

* **Objetivo:** Identificar o único arquivo legível por humanos dentro de vários arquivos no diretório `inhere`.
* **Solução:**
  ```bash
  cd inhere
  file ./*
  cat <arquivo-identificado-como-ASCII-text>
  ```
* **Conceito Aprendido:** Identificação de tipos reais de arquivo com o comando `file` baseado no cabeçalho binário (magic bytes).
* **Flag / Senha Bandit 5:** *(Aguardando resolução)*

