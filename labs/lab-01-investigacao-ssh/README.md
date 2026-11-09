# 🚨 Caso Forense #001: Alerta no SOC — Ataque de Força Bruta SSH

> **Status:** 🔴 Incidente Crítico (Severidade: P1)  
> **Servidor Afetado:** `srv-prod-db` (Servidor de Banco de Dados de Produção)  
> **Evidência Coletada:** [`auth.log`](auth.log) (Log de autenticação do Linux)  
> **Atribuição:** Analista de SOC Nível 1 (Você)

---

## 📋 Contexto do Incidente

Na madrugada de hoje, o SIEM disparou um alarme com o seguinte resumo:
> *"Múltiplas falhas de autenticação SSH seguidas de comportamento anômalo no host `srv-prod-db`."*

O administrador da infraestrutura extraiu a fatia do arquivo de log do sistema (`/var/log/auth.log`) referente ao período suspeito e enviou para o SOC.

Sua missão é conduzir a **triagem forense inicial** deste log e responder com precisão às 4 perguntas cruciais que o coordenador do SOC precisa para responder ao cliente e acionar o time de contenção.

---

## 🎯 As 4 Perguntas de Investigação (Sua Missão)

Abra o arquivo [`labs/lab-01-investigacao-ssh/auth.log`](auth.log) e investigue:

1. **Identificação do Agressor:**
   * Qual é o **endereço IP externo** que realizou as tentativas massivas de força bruta?
2. **Conta Comprometida:**
   * O invasor conseguiu invadir alguma conta? Se sim, **qual foi o nome do usuário** que teve a senha quebrada?
3. **Janela Temporal do Acesso:**
   * Em qual **horário exato** o invasor conseguiu obter o primeiro login com sucesso (`Accepted password`)?
4. **Tentativa de Ação Pós-Exploração:**
   * O que o invasor tentou fazer no servidor logo após logar? *(Dica: procure por comandos que ele tentou rodar com privilégios de administrador via `sudo`)*.

---

## 🧠 Conceitos Teóricos do Analista (O que procurar no Log)

No Linux, o serviço de SSH registra seus eventos com padrões claros:
* **`Failed password for ... from <IP>`** ➔ Alguém errou a senha (ou tentou adivinhar).
* **`Invalid user <nome>`** ➔ O invasor tentou um usuário que nem sequer existe no sistema (ex.: `admin`, `oracle`, `deploy`).
* **`Accepted password for <usuario> from <IP>`** ➔ **SUCESSO!** O invasor (ou usuário legítimo) acertou a senha e abriu uma sessão no shell.
* **`sudo: ... COMMAND=...`** ➔ Qualquer comando que o usuário tentou executar com poderes de root após estar logado.

