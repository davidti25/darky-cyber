# 🔍 Guia de Triagem do Analista: Comandos Essenciais & Mnemônica

Este guia serve como referência rápida para o analista de segurança durante uma triagem inicial de sistema (*Live Response / System Triage*).

---

## 🧠 Como Lembrar dos Comandos: Desconstruindo as Siglas

### 1. Auditoria de Portas: `sudo ss -tulpn`
* **`ss`** = **S**ocket **S**tatistics (Estatísticas de Conexões).
* **`-t`** = Protocolo **T**CP.
* **`-u`** = Protocolo **U**DP.
* **`-l`** = Estado **L**istening (escutando ativamente conexões).
* **`-p`** = **P**rocesso associado (nome do programa e PID).
* **`-n`** = Resolução **N**umérica (mostra a porta em número, ex.: `443` em vez de `https`).

> **Quando usar:** Sempre que suspeitar de portas abertas indevidamente, trojans, backdoors ou para verificar se um servidor web/banco de dados subiu com sucesso.

---

### 2. Investigação de Processos: `ps aux`
* **`ps`** = **P**rocess **S**tatus (Estado dos Processos).
* **`a`** = **A**ll: lista processos de todos os usuários do sistema.
* **`u`** = **U**ser: exibe colunas detalhadas de dono, `%CPU` e `%MEM`.
* **`x`** = Processos em background que não possuem terminal anexado (serviços e daemons).

> **Comando turbinado (Top 10 mais pesados):**
> ```bash
> ps aux --sort=-%mem | head -n 10
> ```
> **Quando usar:** Para identificar mineradores de criptomoeda, processos disfarçados ou softwares travando a máquina.

---

### 3. Identificação de Privilégio: `whoami` e `id`
* **`whoami`** = **Who am I?** (Quem sou eu?).
* **`id`** = Mostra o UID (ID do usuário), GID (ID do grupo principal) e grupos complementares (ex.: se pertence ao grupo `sudo`).

> **Quando usar:** Ao acessar qualquer ambiente, para saber imediatamente se você opera com privilégio mínimo ou com privilégio total de administração (`root` / UID 0).

---

### 4. Reconhecimento de Versão e Kernel: `uname -a`
* **`uname`** = **U**NIX **Name**.
* **`-a`** = **A**ll: imprime nome do sistema operacional, hostname, versão exata do kernel e arquitetura de hardware (`x86_64`).

> **Quando usar:** Para comparar a versão do kernel com bases de vulnerabilidades conhecidas (CVEs) para checar se a máquina está suscetível a exploração de elevação de privilégios.

---

### 5. Reconhecimento de Rede: `ip a`
* **`ip`** = Utilitário de configuração e roteamento IP.
* **`a`** = Abreviação de **a**ddress (endereços associados às interfaces).

> **Quando usar:** Para identificar os IPs atribuídos à máquina, verificar se há interfaces em modo promíscuo ou validar a sub-rede em que o host reside.

