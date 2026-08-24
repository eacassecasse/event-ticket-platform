# Especificação de Pagamentos

## Contexto e problema

A Plataforma de Eventos e Ingressos precisa permitir que um Cliente conclua uma reserva através de um pagamento. O desafio determina que o pagamento seja simulado, devendo existir pelo menos um cenário de pagamento aprovado e outro de pagamento recusado.

Embora não exista uma transacção financeira real no MVP, o fluxo deve representar correctamente os principais estados de um pagamento e a sua relação com a reserva. A implementação deve também evitar que uma mesma operação de pagamento produza efeitos duplicados sobre a reserva ou sobre os ingressos.

---

# 1. Objectivo

Esta especificação define:

- criação de pagamentos;
- associação entre pagamento e reserva;
- estados do pagamento;
- aprovação;
- recusa;
- processamento simulado;
- relação entre pagamento e reserva;
- idempotência;
- prevenção de confirmações duplicadas;
- tratamento de falhas;
- autorização;
- validações;
- critérios de aceitação.

---

# 2. Âmbito

Esta especificação cobre exclusivamente o pagamento associado a uma reserva.

Inclui:

- criação de uma intenção de pagamento;
- processamento simulado;
- aprovação;
- recusa;
- estados;
- valor;
- moeda;
- referência da reserva;
- idempotência;
- integração com a confirmação da reserva.

Não inclui:

- processamento de dinheiro real;
- integração com bancos;
- armazenamento de dados de cartões reais;
- emissão de facturas;
- reembolsos;
- chargebacks;
- conciliação financeira.

Esses comportamentos estão fora do âmbito do MVP.

---

# 3. Princípio fundamental

O pagamento não deve determinar o preço da reserva.

A relação correcta é:

```text
Evento
   │
   │ define
   ▼
Preço
   │
   ▼
Reserva
   │
   │ determina
   ▼
Valor do pagamento
````

O Cliente não deve poder alterar o valor através do frontend.

O backend deve calcular e persistir o valor da reserva e utilizar esse valor como base para o pagamento.

---

# 4. Relação entre pagamento e reserva

Uma reserva pode ter um ou mais registos de tentativa de pagamento, dependendo da estratégia de implementação.

Conceptualmente:

```text
Reserva
   │
   ├── Pagamento 1 → DECLINED
   │
   └── Pagamento 2 → APPROVED
```

Isto permite representar uma primeira tentativa recusada seguida de uma nova tentativa válida.

A regra exacta de múltiplas tentativas deve permanecer simples no MVP.

---

# 5. Estado do pagamento

O pagamento deve possuir um estado explícito.

O conjunto mínimo é:

```text
PENDING
APPROVED
DECLINED
```

## 5.1 PENDING

O pagamento foi iniciado, mas ainda não possui um resultado final.

---

## 5.2 APPROVED

O pagamento foi aceite.

Uma reserva válida associada ao pagamento pode passar para:

```text
CONFIRMED
```

---

## 5.3 DECLINED

O pagamento foi recusado.

A reserva não deve ser confirmada como consequência desse pagamento.

---

# 6. Ciclo de vida

O fluxo normal é:

```text
PENDING
   │
   ├──► APPROVED
   │
   └──► DECLINED
```

Não devem existir transições arbitrárias.

Por exemplo:

```text
APPROVED → PENDING
```

não é permitido.

Da mesma forma:

```text
DECLINED → APPROVED
```

não deve representar uma alteração do mesmo pagamento.

Uma nova tentativa deve criar ou processar uma nova operação de pagamento segundo a estratégia definida.

---

# 7. Relação com a reserva

O pagamento está subordinado à reserva.

Fluxo:

```text
Reserva PENDING
       │
       ▼
Pagamento PENDING
       │
       ├──────────────┐
       │              │
       ▼              ▼
   APPROVED        DECLINED
       │
       ▼
Reserva CONFIRMED
```

A aprovação do pagamento não deve confirmar uma reserva que já tenha expirado ou sido cancelada.

---

# 8. Validade da reserva

Antes de confirmar uma reserva através de um pagamento aprovado, o backend deve verificar:

1. a reserva existe;
2. pertence ao Cliente autenticado;
3. está no estado `PENDING`;
4. ainda não expirou;
5. não foi cancelada;
6. o valor do pagamento corresponde ao valor esperado;
7. o pagamento ainda não produziu uma confirmação anterior.

Se alguma condição falhar, a confirmação deve ser rejeitada.

---

# 9. Pagamento simulado

O MVP deve utilizar um processador de pagamento simulado.

O simulador não deve tentar reproduzir a complexidade de um provedor financeiro real.

O objectivo é demonstrar correctamente:

```text
Cliente
   │
   ▼
Reserva
   │
   ▼
Pagamento
   │
   ├── aprovado
   │
   └── recusado
```

---

# 10. Cenários mínimos do simulador

O simulador deve permitir pelo menos:

```text
APPROVED
DECLINED
```

A interface pode apresentar opções equivalentes a:

```text
Pagamento aprovado
Pagamento recusado
```

O comportamento deve ser determinístico durante a demonstração.

---

# 11. Não utilizar dados financeiros reais

A aplicação não deve solicitar nem armazenar:

* número real de cartão;
* CVV;
* PIN;
* dados bancários reais;
* credenciais financeiras.

O pagamento é exclusivamente simulado.

Qualquer formulário de pagamento deve deixar claro que se trata de uma simulação.

---

# 12. Valor do pagamento

O valor deve ser obtido a partir da reserva.

Exemplo:

```text
Preço unitário: 500 MZN
Quantidade: 3

Valor da reserva:
1500 MZN

Valor do pagamento:
1500 MZN
```

O frontend não deve poder substituir o valor por outro.

---

# 13. Moeda

O pagamento deve armazenar explicitamente a moeda.

Exemplo:

```text
currency = MZN
```

O pagamento deve utilizar a mesma moeda da reserva.

Uma tentativa de pagamento com moeda diferente deve ser rejeitada.

---

# 14. Integridade do valor

O backend deve verificar:

```text
payment.amount == reservation.total_amount
```

Não deve existir uma situação em que:

```text
Reserva:
1500 MZN

Pagamento:
100 MZN

Resultado:
Reserva CONFIRMED
```

---

# 15. Idempotência

O processamento do pagamento deve ser idempotente.

Se a mesma operação for submetida várias vezes, o resultado final deve permanecer consistente.

Exemplo:

```text
Primeira chamada:
Pagamento PENDING → APPROVED

Segunda chamada:
Pagamento APPROVED → APPROVED
```

A segunda chamada não deve:

* confirmar novamente a reserva;
* criar novos ingressos;
* consumir novamente a capacidade;
* criar uma segunda cobrança lógica.

---

# 16. Chave de idempotência

A API deve possuir um mecanismo para identificar uma operação de pagamento repetida.

Uma opção é utilizar uma chave de idempotência fornecida pelo cliente.

Exemplo conceptual:

```text
Idempotency-Key:
payment-attempt-abc123
```

A mesma chave utilizada novamente para a mesma operação deve produzir o mesmo resultado lógico.

A implementação exacta será definida durante o desenvolvimento.

---

# 17. Uma reserva e múltiplas tentativas

Durante o período em que uma reserva permanece `PENDING`, o Cliente pode tentar efectuar o pagamento novamente depois de uma recusa.

Exemplo:

```text
Reserva
   │
   ├── Pagamento 1 → DECLINED
   │
   └── Pagamento 2 → APPROVED
```

A reserva só deve passar para `CONFIRMED` depois de uma tentativa aprovada válida.

---

# 18. Pagamento aprovado

Quando o pagamento for aprovado:

```text
Pagamento:
APPROVED
```

e a reserva estiver válida:

```text
Reserva:
PENDING
```

o sistema deve confirmar a reserva.

Resultado:

```text
Pagamento APPROVED
        │
        ▼
Reserva CONFIRMED
```

A operação deve ser tratada como uma unidade lógica.

---

# 19. Pagamento recusado

Quando o simulador determinar:

```text
DECLINED
```

a reserva não deve ser confirmada.

Resultado:

```text
Pagamento DECLINED
        │
        ▼
Reserva PENDING
```

A reserva pode continuar disponível para nova tentativa enquanto não expirar.

---

# 20. Reserva expirada

Se o Cliente tentar pagar uma reserva expirada:

```text
Reserva:
EXPIRED
```

o pagamento não deve resultar em confirmação.

O sistema deve comunicar que a reserva já não é válida.

Não deve ser possível utilizar um pagamento aprovado para recuperar automaticamente uma reserva expirada.

---

# 21. Reserva cancelada

Uma reserva:

```text
CANCELLED
```

não pode ser confirmada através de um pagamento.

Qualquer tentativa deve ser rejeitada.

---

# 22. Pagamento depois da expiração

Considere:

```text
14:00 — Reserva criada
14:10 — Reserva expira
14:11 — Pagamento aprovado
```

O pagamento aprovado não deve confirmar a reserva.

O backend deve validar o estado e o prazo da reserva no momento da confirmação.

---

# 23. Transacção de confirmação

A operação lógica:

```text
Pagamento aprovado
        │
        ├── actualizar pagamento
        ├── confirmar reserva
        └── permitir emissão de ingresso
```

deve possuir limites transaccionais claros.

O sistema não deve produzir:

```text
Pagamento APPROVED
Reserva PENDING
```

quando o pagamento já tiver sido aceite para uma reserva válida.

Também não deve produzir:

```text
Reserva CONFIRMED
Pagamento DECLINED
```

---

# 24. Falha durante confirmação

Se ocorrer uma falha durante o processamento, a implementação deve evitar estados parcialmente persistidos.

Por exemplo, não deve existir:

```text
Reserva CONFIRMED
Pagamento não registado
```

nem:

```text
Pagamento APPROVED
Reserva ainda utilizável por outro Cliente
```

A estratégia concreta dependerá da arquitectura e da base de dados utilizada.

---

# 25. Emissão do ingresso

O pagamento não deve gerar directamente a apresentação visual do ingresso.

A responsabilidade deve ser separada:

```text
Pagamento
   │
   ▼
Reserva CONFIRMED
   │
   ▼
Ticket Issuance
   │
   ▼
Ingresso
```

Isto mantém o pagamento desacoplado do mecanismo de geração de QR Code.

---

# 26. Segurança

Como o pagamento é simulado, a segurança principal está na autorização e integridade do fluxo.

O sistema deve impedir que um Cliente:

* pague uma reserva de outro Cliente;
* altere o valor;
* altere a moeda;
* confirme directamente uma reserva;
* marque um pagamento como aprovado através de dados manipulados no frontend.

O estado `APPROVED` deve ser produzido exclusivamente pelo backend/simulador.

---

# 27. Autoridade sobre o estado

O frontend nunca deve ser a autoridade sobre o resultado do pagamento.

Não é válido:

```json
{
  "status": "APPROVED"
}
```

como mecanismo para determinar o resultado real.

O backend deve executar o simulador e determinar o estado.

---

# 28. API conceptual

A API pode possuir operações equivalentes a:

```text
POST /reservations/{reservation_id}/payments
GET  /payments/{payment_id}
```

Para uma nova tentativa:

```text
POST /reservations/{reservation_id}/payments
```

pode criar uma nova tentativa.

Os endpoints concretos serão definidos durante a implementação.

---

# 29. Pedido conceptual

O cliente deve fornecer apenas os dados necessários para iniciar o pagamento.

Exemplo:

```json
{
  "method": "SIMULATED"
}
```

O backend obtém:

```text
customer_id
reservation_id
amount
currency
```

a partir dos dados persistidos.

---

# 30. Resposta conceptual

Uma resposta pode possuir:

```json
{
  "id": "payment-123",
  "reservation_id": "reservation-123",
  "status": "APPROVED",
  "amount": 1500,
  "currency": "MZN"
}
```

A representação final será definida na implementação.

---

# 31. Erros

A API deve diferenciar pelo menos:

```text
RESERVATION_NOT_FOUND
RESERVATION_NOT_OWNED
RESERVATION_EXPIRED
RESERVATION_CANCELLED
RESERVATION_ALREADY_CONFIRMED
INVALID_PAYMENT_AMOUNT
INVALID_PAYMENT_CURRENCY
PAYMENT_ALREADY_PROCESSED
PAYMENT_DECLINED
PAYMENT_NOT_FOUND
```

Os nomes exactos podem variar na implementação.

O significado deve permanecer claro.

---

# 32. Regra de autorização

Um Cliente só pode iniciar pagamentos para as suas próprias reservas.

O sistema não deve confiar apenas no:

```text
reservation_id
```

fornecido pelo cliente.

A autorização deve verificar a relação:

```text
Authenticated User
        │
        ▼
Customer
        │
        ▼
Reservation.customer_id
```

---

# 33. Organizador

O Organizador não deve iniciar pagamentos em nome de Clientes através da API normal.

O Organizador gere eventos, não transacções dos Clientes.

---

# 34. Portaria

A Portaria não possui qualquer responsabilidade sobre pagamentos.

O fluxo da Portaria começa depois da emissão do ingresso:

```text
Pagamento
   │
   ▼
Ingresso
   │
   ▼
Portaria
```

---

# 35. Modelo conceptual

O pagamento pode ser representado por:

```text
Payment
├── id
├── reservation_id
├── amount
├── currency
├── status
├── method
├── idempotency_key
├── created_at
└── updated_at
```

Se forem suportadas múltiplas tentativas:

```text
Reservation
      │
      ├── Payment Attempt 1
      ├── Payment Attempt 2
      └── ...
```

---

# 36. Relação com a reserva

A relação mínima é:

```text
Customer
   │
   ▼
Reservation
   │
   │ 1..N
   ▼
Payment
```

O pagamento nunca deve existir sem uma reserva válida associada.

---

# 37. Observabilidade

O sistema deve registar eventos suficientes para diagnosticar:

* pagamento iniciado;
* pagamento aprovado;
* pagamento recusado;
* pagamento rejeitado por reserva expirada;
* pagamento rejeitado por autorização;
* confirmação duplicada;
* falhas de processamento.

Os logs não devem incluir dados financeiros sensíveis.

---

# 38. Testes

A implementação deve incluir testes para:

### Fluxo aprovado

* criar pagamento;
* aprovar pagamento;
* confirmar reserva;
* garantir que não existem efeitos duplicados.

### Fluxo recusado

* criar pagamento;
* recusar pagamento;
* garantir que reserva permanece `PENDING`.

### Expiração

* tentar pagar reserva expirada;
* garantir que não é confirmada.

### Cancelamento

* tentar pagar reserva cancelada;
* garantir que é rejeitado.

### Valor

* valor correcto;
* tentativa de manipulação do valor;
* moeda incorrecta.

### Autorização

* Cliente paga a própria reserva;
* Cliente tenta pagar reserva de outro Cliente.

### Idempotência

* mesma operação submetida duas vezes;
* confirmação repetida;
* criação repetida com a mesma chave de idempotência.

---

# 39. Critérios de aceitação

## AC-01 — Pagamento aprovado

**Dado** uma reserva `PENDING` válida,

**quando** o pagamento simulado for aprovado,

**então** o pagamento deve ficar `APPROVED` e a reserva deve passar para `CONFIRMED`.

---

## AC-02 — Pagamento recusado

**Dado** uma reserva `PENDING` válida,

**quando** o pagamento simulado for recusado,

**então** o pagamento deve ficar `DECLINED` e a reserva não deve ser confirmada.

---

## AC-03 — Reserva expirada

**Dado** uma reserva expirada,

**quando** o Cliente tentar efectuar o pagamento,

**então** a operação deve ser rejeitada.

---

## AC-04 — Valor

**Dado** uma reserva de 1500 MZN,

**quando** o pagamento for processado,

**então** o valor utilizado deve ser 1500 MZN.

---

## AC-05 — Manipulação do frontend

**Dado** que o Cliente altere o valor enviado pelo frontend,

**quando** o backend processar o pagamento,

**então** deve ignorar o valor manipulado e utilizar o valor persistido da reserva.

---

## AC-06 — Idempotência

**Dado** um pagamento já aprovado,

**quando** a mesma operação for processada novamente,

**então** não devem ser criados efeitos adicionais.

---

## AC-07 — Autorização

**Dado** uma reserva pertencente ao Cliente A,

**quando** o Cliente B tentar iniciar um pagamento,

**então** a operação deve ser rejeitada.

---

## AC-08 — Pagamento após expiração

**Dado** um pagamento aprovado depois de a reserva ter expirado,

**quando** o backend tentar confirmar a reserva,

**então** a reserva não deve passar para `CONFIRMED`.

---

# 40. Regras de integridade

A implementação deve garantir:

```text
1. Todo pagamento pertence a uma reserva.
2. O pagamento utiliza o valor persistido da reserva.
3. A moeda do pagamento corresponde à moeda da reserva.
4. O frontend não determina o resultado do pagamento.
5. APPROVED é um estado terminal do pagamento.
6. DECLINED é um estado terminal daquela tentativa.
7. Uma reserva expirada não pode ser confirmada.
8. Uma reserva cancelada não pode ser confirmada.
9. Um Cliente só pode pagar as suas próprias reservas.
10. A confirmação deve ser idempotente.
11. O pagamento aprovado deve resultar numa reserva confirmada apenas quando esta for válida.
12. O pagamento não deve emitir directamente o ingresso.
```

---

# 41. Confirmação

A conformidade desta especificação deve ser verificada através de:

1. testes unitários;
2. testes de integração;
3. testes de API;
4. testes de autorização;
5. testes de idempotência;
6. testes de estados;
7. execução manual dos cenários aprovado e recusado;
8. execução do fluxo completo reserva → pagamento → confirmação.

---

# 42. Dependências

Esta especificação depende de:

* Autenticação e Autorização;
* Gestão de Eventos;
* Reservas.

É utilizada posteriormente por:

* Emissão de Ingressos;
* Validação de Ingressos.

---

# 43. Fluxo completo

O fluxo de pagamento esperado é:

```text
Cliente
   │
   ▼
Reserva PENDING
   │
   ▼
Inicia pagamento
   │
   ▼
Pagamento PENDING
   │
   ├──────────────────┐
   │                  │
   ▼                  ▼
APPROVED            DECLINED
   │                  │
   ▼                  ▼
Reserva             Reserva
CONFIRMED           permanece
   │                PENDING
   ▼
Emissão
do ingresso
```

Se a reserva expirar:

```text
Reserva PENDING
       │
       ▼
Reserva EXPIRED
       │
       └──► pagamentos posteriores rejeitados
```

---

# 44. Resultado esperado

No final desta funcionalidade, a plataforma deve permitir que um Cliente:

1. inicie um pagamento para uma reserva válida;
2. receba um resultado simulado de aprovação ou recusa;
3. tenha a reserva confirmada apenas quando o pagamento for aprovado;
4. tente novamente depois de uma recusa enquanto a reserva permanecer válida;
5. não consiga pagar uma reserva de outro Cliente;
6. não consiga alterar o valor;
7. não consiga alterar o resultado do pagamento através do frontend;
8. não consiga confirmar uma reserva expirada;
9. não produza efeitos duplicados ao repetir uma operação de pagamento.

A confirmação bem-sucedida da reserva será o ponto de entrada para a especificação de emissão de ingressos.