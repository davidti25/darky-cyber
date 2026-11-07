# 🐧 Semana 1: Linux Operacional para Cibersegurança

Bem-vindo à primeira semana da sua jornada prática! 

Este diretório serve como sua base de anotações e cheatsheet. Tudo o que você documentar aqui fará parte do seu **portfólio técnico no GitHub**.

---

## 🎯 Metas da Semana
- [ ] Conectar ao laboratório **OverTheWire Bandit** via SSH.
- [ ] Concluir os níveis 0 ao 5 (Navegação e arquivos).
- [ ] Concluir os níveis 6 ao 10 (Busca e filtragem com `find`, `grep` e `strings`).
- [ ] Concluir os níveis 11 ao 15 (Codificação base64, compressão e conexões de rede).
- [ ] Criar seu primeiro script de automação em Bash.

---

## 🛠️ Comandos Essenciais do Analista

### 1. Navegação e Arquivos
* `pwd` — Mostra o diretório atual (*Print Working Directory*).
* `ls -la` — Lista todos os arquivos, incluindo arquivos ocultos (iniciados com `.`) e permissões detalhadas.
* `cd <pasta>` — Muda de diretório.
* `cat <arquivo>` — Exibe o conteúdo de um arquivo na tela.
* `file <arquivo>` — Identifica o tipo real do arquivo (mesmo que a extensão tenha sido alterada).

### 2. Busca e Filtragem (Crucial para achar evidências)
* `grep -rn "palavra" .` — Busca recursivamente por um texto dentro de todos os arquivos da pasta atual.
* `find . -type f -size 1033c` — Encontra arquivos com tamanho exato (ex.: 1033 bytes).
* `strings <arquivo_binario>` — Extrai apenas os textos legíveis dentro de um executável ou arquivo binário.

### 3. Redirecionamento e Pipes (O poder do Unix)
* `|` (Pipe) — Passa a saída de um comando como entrada para o próximo (ex.: `cat arquivo | grep senha`).
* `>` — Redireciona a saída para um arquivo, sobrescrevendo.
* `>>` — Redireciona a saída para o fim de um arquivo, anexando.

---

## 🔒 Registro do Lab OverTheWire Bandit
Anote aqui a senha que você descobre em cada nível (para poder reconectar quando quiser):

| Nível | Comando de Conexão | Senha Encontrada | Conceito Aprendido |
| :--- | :--- | :--- | :--- |
| **bandit0** | `ssh bandit0@bandit.labs.overthewire.org -p 2220` | `bandit0` | Conexão SSH básica |
| **bandit1** | `ssh bandit1@bandit.labs.overthewire.org -p 2220` | *(aguardando)* | Lendo arquivo `readme` |
| **bandit2** | `ssh bandit2@bandit.labs.overthewire.org -p 2220` | *(aguardando)* | Arquivo com nome `-` |
| **bandit3** | `ssh bandit3@bandit.labs.overthewire.org -p 2220` | *(aguardando)* | Espaços no nome |
| **bandit4** | `ssh bandit4@bandit.labs.overthewire.org -p 2220` | *(aguardando)* | Arquivos ocultos |
| **bandit5** | `ssh bandit5@bandit.labs.overthewire.org -p 2220` | *(aguardando)* | Filtrando por propriedades |

