# 📑 Relatório de Análise Forense: Incidente SSH #001

* **Data da Análise:** 08/11/2026
* **Analista Responsável:** David Brasil (Darky Cyber)
* **Ambiente Analisado:** Servidor Linux (`srv-prod-db`)
* **Arquivo Fonte:** `auth.log`

---

## 1. 🔍 Resumo Executivo
*(Preencher com uma breve descrição do que aconteceu em poucas frases)*

---

## 2. 🛡️ Indicadores de Comprometimento (IoCs)

| Tipo de Indicador | Valor Encontrado | Descrição / Observação |
| :--- | :--- | :--- |
| **IP do Atacante** | `[Preencher]` | Origem do ataque de força bruta |
| **Usuário Comprometido** | `[Preencher]` | Conta que teve a senha quebrada |
| **Timestamp do Acesso** | `[Preencher]` | Data e hora exata do login inicial |
| **Vetor de Ataque** | SSH Brute Force (Porta 22) | Dicionário de credenciais comuns |

---

## 3. 🚨 Evidências Técnicas Extraídas do Log
*(Copie e cole aqui as linhas-chave do `auth.log` que comprovam o ataque e a invasão)*

```text
[Cole as linhas de evidência aqui]
```

---

## 4. 🛑 Ações Pós-Exploração Detectadas
*(O que o invasor tentou fazer com o comando `sudo`?)*

---

## 5. 💡 Recomendações Defensivas (Blue Team)
*(O que a empresa deve implementar para evitar que isso aconteça novamente?)*
* [ ] Desabilitar login SSH com senha e exigir chaves criptográficas (`SSH Keys`).
* [ ] Instalar e configurar **Fail2ban** para bloquear IPs automaticamente após 3 tentativas inválidas.
* [ ] Alterar a porta padrão do SSH (porta 22) para mitigar varreduras automáticas de scanners de internet.
* [ ] Restringir o acesso SSH via firewall (apenas IPs internos da VPN).

