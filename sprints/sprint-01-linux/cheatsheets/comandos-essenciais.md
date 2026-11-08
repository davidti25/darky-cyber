# 🐧 Cheatsheet: Comandos Essenciais de Terminal Linux

> Guia prático de referência rápida para operações em terminal, investigação forense básica e auditoria de sistema.  
> Desenvolvido durante a **Sprint 01** do projeto [Darky Cyber](../../README.md).

---

## 1. 📂 Navegação e Sistema de Arquivos

| Comando | Descrição | Exemplo Prático |
| :--- | :--- | :--- |
| `pwd` | Exibe o caminho absoluto do diretório atual (*Print Working Directory*). | `pwd` |
| `ls -la` | Lista todos os arquivos (incluindo ocultos iniciados por `.`) com permissões e tamanhos. | `ls -la` |
| `cd <caminho>` | Alterna entre diretórios. `cd ..` volta um nível; `cd ~` vai para a *home*. | `cd /var/log` |
| `file <arquivo>` | Analisa a assinatura mágica e informa o formato real do arquivo (independente da extensão). | `file suspeito.bin` |
| `cat <arquivo>` | Concatena e exibe o conteúdo do arquivo na tela. | `cat /etc/passwd` |

---

## 2. 🔍 Busca e Investigação de Arquivos

| Comando | Descrição | Exemplo Prático |
| :--- | :--- | :--- |
| `grep -rn "texto" .` | Busca recursiva por uma string em todos os arquivos a partir da pasta atual. | `grep -rn "password" /etc/` |
| `find <dir> -name <padrão>` | Localiza arquivos por nome ou padrão. | `find / -name "*.conf" 2>/dev/null` |
| `find . -size 1033c` | Localiza arquivos pelo tamanho exato em bytes (`c` = bytes). | `find . -type f -size 1033c` |
| `strings <arquivo>` | Extrai sequências de caracteres imprimíveis de arquivos binários. | `strings malware.bin \| grep -i http` |

---

## 3. ⚙️ Redirecionamentos, Operadores e Pipes

* `|` (**Pipe**): Envia a saída padrão (`stdout`) de um comando diretamente como entrada (`stdin`) para o próximo.
  ```bash
  cat senhas.txt | grep "admin"
  ```
* `>` (**Sobrescrever**): Direciona a saída para um arquivo, substituindo todo o conteúdo anterior.
  ```bash
  echo "nova_linha" > registro.txt
  ```
* `>>` (**Anexar**): Adiciona a saída ao final do arquivo sem apagar o que já existe.
  ```bash
  echo "evento_detectado" >> auditoria.log
  ```
* `2>/dev/null` (**Descarte de Erros**): Envia as mensagens de erro (`stderr`) para o "buraco negro" do Linux, mantendo o terminal limpo de mensagens de "Acesso Negado".
  ```bash
  find / -type f -perm -4000 2>/dev/null
  ```

---

## 4. 🔒 Manipulação de Arquivos com Nomes Especiais

* **Arquivo com traço inicial (`-`)**: O bash interpreta traço como parâmetro/flag. Para ler, especifique o caminho relativo:
  ```bash
  cat ./-
  ```
* **Arquivo com espaços no nome**: Envolva entre aspas ou escape com barra invertida:
  ```bash
  cat "spaces in this filename"
  # ou
  cat spaces\ in\ this\ filename
  ```
