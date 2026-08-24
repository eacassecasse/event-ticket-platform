# Especificação de Reservas

## Contexto e problema

A Plataforma de Eventos e Ingressos precisa permitir que um Cliente reserve ingressos para um evento antes de concluir o pagamento.

A reserva constitui a etapa que liga a intenção de compra do Cliente à disponibilidade real do evento. Como vários Clientes podem tentar adquirir ingressos simultaneamente, o sistema deve impedir que a capacidade seja ultrapassada e, quando forem utilizados lugares identificáveis, garantir que o mesmo lugar não possa ser atribuído a mais de uma reserva confirmada.

Esta especificação define o comportamento, ciclo de vida, regras de concorrência e integridade das reservas.

---

# 1. Objectivo

Esta especificação define:

- criação de reservas;
- associação entre Cliente, evento e ingressos;
- quantidade reservada;
- selecção de lugares, quando aplicável;
- estados da reserva;
- confirmação;
- expiração;
- cancelamento;
- relação com o pagamento;
- controlo da disponibilidade;
- prevenção de reservas concorrentes;
- prevenção de venda duplicada;
- regras de acesso;
- validações;
- critérios de aceitação.

---

# 2. Âmbito

Esta especificação cobre exclusivamente o processo de reserva.

Inclui:

- disponibilidade;
- criação da reserva;
- retenção temporária da capacidade;
- selecção de lugares;
- estado da reserva;
- confirmação;
- expiração;
- cancelamento;
- concorrência;
- integridade dos dados;
- autorização;
- integração conceptual com o pagamento.

Não inclui:

- processamento financeiro real;
- geração do QR Code;
- validação do ingresso na portaria;
- envio de correio electrónico;
- reembolso financeiro.

Essas responsabilidades são tratadas por outros domínios.

---

# 3. Conceito de reserva

Uma reserva representa uma intenção de aquisição de um ou mais ingressos para determinado evento.

Conceptualmente:

```text
Cliente
   │
   │ cria
   ▼
Reserva
   │
   ├── Evento
   ├── Quantidade
   ├── Lugares (quando aplicável)
   ├── Valor total
   ├── Estado
   └── Prazo de validade
````

A reserva não representa automaticamente uma compra concluída.

A compra só deve ser considerada concluída depois de a reserva passar pelas etapas necessárias de pagamento e confirmação.

---

# 4. Relação entre reserva e ingresso

A reserva e o ingresso são conceitos diferentes.

Uma reserva representa:

> "O Cliente pretende adquirir estes ingressos."

Um ingresso representa:

> "A aquisição foi confirmada e existe um direito de entrada no evento."

Assim:

```text
Reserva
   │
   │ pagamento confirmado
   ▼
Ingressos
```

Uma reserva não confirmada não deve gerar ingressos válidos.

---

# 5. Tipos de evento suportados

A plataforma pode suportar dois modelos de aquisição:

```text
1. Lugares numerados
2. Entrada geral / pista
```

## 5.1 Lugares numerados

Cada ingresso está associado a um lugar específico.

Exemplo:

```text
Sala
├── A1
├── A2
├── A3
├── A4
├── B1
├── B2
└── ...
```

O Cliente selecciona os lugares pretendidos.

Cada lugar pode pertencer a, no máximo, uma reserva activa ou confirmação final.

---

## 5.2 Entrada geral

Não existe um lugar individual.

O Cliente selecciona uma quantidade.

Exemplo:

```text
Evento
Capacidade: 500

Cliente solicita:
3 ingressos
```

O sistema deve verificar se existem pelo menos três unidades disponíveis.

---

# 6. Modelo escolhido para o MVP

Para reduzir o risco de implementação dentro do prazo de sete dias, o MVP deve suportar **um modelo completo de aquisição** antes de adicionar o segundo.

A implementação pode começar com:

```text
Entrada geral / pista
```

porque este modelo reduz a complexidade associada ao mapa de lugares e permite demonstrar correctamente:

* disponibilidade;
* concorrência;
* reserva;
* pagamento;
* emissão;
* validação.

O suporte para lugares numerados pode ser adicionado posteriormente sem alterar o conceito fundamental da reserva.

---

# 7. Estado da reserva

Cada reserva deve possuir um estado explícito.

O conjunto mínimo é:

```text
PENDING
CONFIRMED
EXPIRED
CANCELLED
```

## 7.1 PENDING

A reserva foi criada, mas o pagamento ainda não foi confirmado.

A capacidade correspondente deve permanecer temporariamente retida para evitar que outro Cliente a adquira.

---

## 7.2 CONFIRMED

O pagamento foi aceite e a reserva foi concluída.

Os ingressos podem ser emitidos.

A capacidade correspondente deixa de estar disponível para novas reservas.

---

## 7.3 EXPIRED

O prazo para concluir a reserva terminou sem confirmação de pagamento.

A capacidade retida deve ser libertada.

---

## 7.4 CANCELLED

A reserva foi explicitamente cancelada segundo as regras da aplicação.

A capacidade correspondente deve ser libertada quando aplicável.

---

# 8. Ciclo de vida

O ciclo normal é:

```text
PENDING
   │
   ├──► CONFIRMED
   │
   └──► EXPIRED
```

Uma reserva também pode seguir:

```text
PENDING
   │
   └──► CANCELLED
```

Uma reserva confirmada não deve voltar para `PENDING`.

Para o MVP, não deve existir uma transição:

```text
CONFIRMED ──► CANCELLED
```

sem uma regra explícita de negócio para cancelamento de uma compra confirmada.

---

# 9. Criação da reserva

Uma reserva pode ser criada apenas por um Cliente autenticado.

No momento da criação, o sistema deve validar:

1. o Cliente está autenticado;
2. o evento existe;
3. o evento está publicado;
4. o evento ainda aceita reservas;
5. a quantidade solicitada é válida;
6. existe disponibilidade suficiente;
7. os lugares seleccionados são válidos, quando aplicável;
8. os lugares não estão actualmente indisponíveis.

Se alguma destas condições falhar, a reserva não deve ser criada.

---

# 10. Evento elegível

Só podem ser criadas reservas para eventos no estado:

```text
PUBLISHED
```

Não podem ser criadas reservas para:

```text
DRAFT
CANCELLED
COMPLETED
```

Um evento publicado, mas esgotado, também não pode aceitar novas reservas.

---

# 11. Quantidade da reserva

Para entrada geral, a quantidade deve:

* ser um número inteiro;
* ser superior a zero;
* não ultrapassar o limite máximo permitido por reserva;
* não ultrapassar a disponibilidade actual.

Exemplo:

```text
Disponível: 10

Pedido de 4:
válido

Pedido de 10:
válido

Pedido de 11:
rejeitado
```

---

# 12. Limite por reserva

A aplicação deve possuir um limite máximo configurável de ingressos por reserva.

Para o MVP, recomenda-se um valor simples e explícito, por exemplo:

```text
MAX_TICKETS_PER_RESERVATION = 10
```

Este valor deve ser configurável e não espalhado pelo código como um número literal.

---

# 13. Lugares numerados

Quando o evento utilizar lugares numerados, uma reserva deve conter os lugares seleccionados pelo Cliente.

Exemplo:

```text
Reserva
├── Lugar A1
├── Lugar A2
└── Lugar A3
```

Cada lugar deve possuir uma identificação inequívoca dentro do evento.

O sistema não deve considerar apenas o número do lugar isoladamente.

A identidade deve ser contextualizada pelo evento.

Assim:

```text
Evento A / A1
```

e:

```text
Evento B / A1
```

são lugares diferentes.

---

# 14. Regra de exclusividade do lugar

Um lugar não pode estar simultaneamente reservado de forma válida por duas reservas activas.

Exemplo:

```text
Cliente A → Lugar A10
Cliente B → Lugar A10
```

O sistema deve permitir que apenas uma das operações seja bem-sucedida.

---

# 15. Concorrência

A concorrência é uma preocupação central desta funcionalidade.

Considere:

```text
Disponibilidade = 1
```

e dois pedidos simultâneos:

```text
Cliente A → 1 ingresso
Cliente B → 1 ingresso
```

Não é aceitável que ambos recebam:

```text
PENDING
```

se isso resultar numa capacidade reservada de 2.

O sistema deve garantir atomicidade na operação que verifica e consome a disponibilidade.

---

# 16. Regra fundamental de integridade

A seguinte condição deve ser verdadeira:

```text
capacidade_confirmada
+
capacidade_reservada
<=
capacidade_total
```

Onde:

* `capacidade_total` representa a capacidade configurada do evento;
* `capacidade_reservada` representa unidades actualmente retidas por reservas `PENDING`;
* `capacidade_confirmada` representa unidades pertencentes a reservas `CONFIRMED`.

Esta regra deve ser preservada mesmo perante pedidos concorrentes.

---

# 17. Exemplo de concorrência

Considere:

```text
Capacidade: 100
Confirmados: 95
Pendentes: 3
Disponibilidade efectiva: 2
```

Dois Clientes solicitam simultaneamente:

```text
Cliente A → 2
Cliente B → 2
```

Resultado válido:

```text
Cliente A → PENDING
Cliente B → rejeitado
```

Não é válido:

```text
Cliente A → PENDING
Cliente B → PENDING
```

porque isso criaria:

```text
95 + 3 + 2 + 2 = 102
```

unidades comprometidas.

---

# 18. Protecção no nível da base de dados

A verificação de disponibilidade não deve depender exclusivamente de lógica no frontend.

Também não deve depender exclusivamente de uma sequência de consultas não protegidas no backend.

A implementação deve utilizar mecanismos transaccionais apropriados para impedir condições de corrida.

A estratégia exacta será definida na implementação, mas deverá utilizar pelo menos:

* transacções;
* operações atómicas;
* locks apropriados quando necessários;
* constraints de integridade;
* índices/constraints para impedir duplicações.

---

# 19. Retenção temporária

Uma reserva `PENDING` deve possuir um prazo de validade.

Exemplo:

```text
Criada:       14:00:00
Expira:       14:10:00
```

Durante esse período, a capacidade fica temporariamente retida.

Se o pagamento não for confirmado dentro do prazo:

```text
PENDING
   │
   ▼
EXPIRED
```

A capacidade deve ser libertada.

---

# 20. Duração da retenção

A duração deve ser configurável.

Para o MVP, pode ser utilizado:

```text
RESERVATION_EXPIRATION_MINUTES = 10
```

A configuração deve estar centralizada.

Não deve ser necessário alterar código de domínio para modificar a duração.

---

# 21. Expiração

Uma reserva é considerada expirada quando:

```text
current_time > expires_at
```

e o pagamento ainda não foi confirmado.

O sistema deve impedir que uma reserva expirada seja confirmada posteriormente.

---

# 22. Tratamento de reservas expiradas

A implementação deve garantir que reservas expiradas deixam de consumir disponibilidade.

O mecanismo exacto pode ser:

* processamento periódico;
* limpeza durante consultas;
* verificação no momento de uma nova reserva;
* combinação dos mecanismos anteriores.

Para o MVP, não é necessário implementar uma infraestrutura de processamento distribuído.

Contudo, a lógica de domínio deve tratar correctamente uma reserva cujo prazo já terminou.

---

# 23. Pagamento

A reserva deve estar ligada ao pagamento através de uma relação explícita.

Fluxo conceptual:

```text
Cliente
   │
   ▼
Reserva PENDING
   │
   ▼
Pagamento
   │
   ├── APROVADO ──► Reserva CONFIRMED
   │
   └── RECUSADO ──► Reserva continua PENDING
```

O pagamento recusado não deve resultar numa confirmação de reserva.

---

# 24. Pagamento recusado

Quando o pagamento simulado for recusado:

```text
Pagamento = DECLINED
```

a reserva não deve passar para:

```text
CONFIRMED
```

A aplicação pode permitir ao Cliente tentar novamente enquanto a reserva permanecer válida.

Se o prazo terminar:

```text
PENDING → EXPIRED
```

---

# 25. Pagamento aprovado

Quando o pagamento for aprovado:

```text
Pagamento = APPROVED
```

a aplicação deve:

1. verificar novamente a validade da reserva;
2. confirmar que ainda está dentro do prazo;
3. confirmar que não foi cancelada;
4. alterar a reserva para `CONFIRMED`;
5. tornar a capacidade definitivamente consumida;
6. permitir a emissão dos ingressos.

A operação deve ser transaccional.

---

# 26. Idempotência

A confirmação de uma reserva deve ser idempotente.

Se o mesmo pedido de confirmação for processado duas vezes, não deve:

* criar dois conjuntos de ingressos;
* consumir duas vezes a capacidade;
* gerar duas confirmações financeiras;
* produzir estados inconsistentes.

Exemplo:

```text
Primeira execução:
PENDING → CONFIRMED

Segunda execução:
CONFIRMED → CONFIRMED
```

A segunda execução não deve repetir os efeitos da primeira.

---

# 27. Cancelamento

Uma reserva `PENDING` pode ser cancelada pelo Cliente antes da confirmação.

Fluxo:

```text
PENDING
   │
   ▼
CANCELLED
```

Quando isso ocorrer, a capacidade retida deve ser libertada.

---

# 28. Cancelamento de reserva confirmada

O cancelamento de uma reserva já confirmada depende das regras de negócio relativas a reembolso.

Como o reembolso não é requisito obrigatório do desafio, o MVP não deve introduzir um fluxo complexo de cancelamento pós-pagamento.

Caso seja implementado, deve existir uma especificação própria para:

* elegibilidade;
* reembolso;
* invalidação de ingressos;
* devolução ao stock.

---

# 29. Disponibilidade

A disponibilidade apresentada ao Cliente deve considerar reservas `PENDING` válidas.

Exemplo:

```text
Capacidade: 100
Confirmados: 50
Pendentes válidos: 20

Disponível:
100 - 50 - 20 = 30
```

Uma reserva expirada não deve continuar a reduzir a disponibilidade.

---

# 30. Reserva e disponibilidade

A criação de uma reserva deve:

```text
1. verificar disponibilidade;
2. reservar a capacidade;
3. criar a reserva;
4. definir expires_at;
5. confirmar a transacção.
```

Estas operações devem ser tratadas como uma unidade lógica.

Se uma delas falhar, o sistema não deve deixar capacidade parcialmente consumida.

---

# 31. Falha durante a criação

Se ocorrer uma falha depois de a capacidade ter sido temporariamente bloqueada, mas antes da reserva ser persistida correctamente, a transacção deve ser revertida.

O sistema não pode deixar:

```text
capacidade consumida
+
reserva inexistente
```

---

# 32. Falha durante confirmação

Da mesma forma, uma confirmação parcialmente executada não pode produzir:

```text
Reserva CONFIRMED
+
pagamento inconsistente
+
ingressos inexistentes
```

A arquitectura deve definir claramente o limite transaccional da operação.

---

# 33. Cliente e propriedade da reserva

Uma reserva pertence ao Cliente que a criou.

Um Cliente só pode consultar as suas próprias reservas.

Exemplo:

```text
Cliente A
   └── Reserva A

Cliente B
   └── Reserva B
```

O Cliente A não pode consultar ou manipular a Reserva B.

---

# 34. Organizador e reservas

O Organizador não deve poder manipular arbitrariamente as reservas dos Clientes.

Pode existir uma consulta administrativa de reservas associadas aos seus eventos, mas as operações financeiras ou de alteração de estado devem respeitar regras específicas.

Para o MVP, recomenda-se que o Organizador tenha acesso apenas à informação necessária para gerir o evento.

---

# 35. Portaria

O utilizador da Portaria não deve manipular reservas.

A Portaria trabalha com ingressos emitidos.

O fluxo será:

```text
Reserva CONFIRMED
        │
        ▼
     Ingresso
        │
        ▼
     Portaria
```

A validação do ingresso pertence ao domínio de validação.

---

# 36. Dados mínimos da reserva

Uma reserva deve possuir, conceptualmente:

```text
Reservation
├── id
├── customer_id
├── event_id
├── status
├── quantity
├── total_amount
├── currency
├── expires_at
├── created_at
└── updated_at
```

Quando houver lugares numerados:

```text
Reservation
└── ReservationSeats
       ├── seat_id
       ├── reservation_id
       └── ...
```

Os nomes exactos das tabelas e campos serão definidos durante a implementação.

---

# 37. Valor total

O valor total deve ser determinado pelo backend.

Não se deve confiar no valor enviado pelo frontend.

Exemplo:

```text
Preço unitário: 500 MZN
Quantidade: 3

Total:
500 × 3 = 1500 MZN
```

O frontend pode enviar a quantidade, mas o backend deve obter o preço aplicável do evento e calcular o total.

---

# 38. Protecção contra manipulação de preço

Um Cliente não deve conseguir enviar:

```json
{
  "quantity": 3,
  "total_amount": 1
}
```

e obter uma reserva de 1 MZN.

O backend deve ignorar qualquer total calculado pelo cliente e calcular o valor com base nos dados persistidos.

---

# 39. Snapshot do preço

Quando a reserva for criada, o preço utilizado deve ser preservado na própria reserva.

Isto evita que alterações futuras do evento alterem retroactivamente o valor de uma reserva existente.

Exemplo:

```text
Evento:
Preço actual = 500 MZN

Reserva criada:
Preço unitário = 500 MZN
```

Mesmo que o preço do evento fosse posteriormente alterado segundo regras permitidas, a reserva já criada deve manter o seu valor.

---

# 40. Moeda

A reserva deve armazenar explicitamente a moeda utilizada.

Exemplo:

```text
currency = MZN
```

O sistema não deve inferir a moeda apenas através do contexto da aplicação.

---

# 41. API conceptual

A API deverá suportar operações equivalentes a:

```text
POST   /reservations
GET    /reservations
GET    /reservations/{reservation_id}

POST   /reservations/{reservation_id}/cancel
POST   /reservations/{reservation_id}/payment
```

Os endpoints exactos serão definidos durante a implementação.

---

# 42. Criação conceptual

Exemplo de pedido:

```json
{
  "event_id": "event-123",
  "quantity": 2
}
```

O servidor deve determinar:

```text
customer_id
event
unit_price
total_amount
currency
expires_at
status
```

Não devem ser aceites pelo cliente campos que possam comprometer a integridade do domínio.

---

# 43. Resposta conceptual

Uma resposta de criação pode possuir:

```json
{
  "id": "reservation-123",
  "event_id": "event-123",
  "status": "PENDING",
  "quantity": 2,
  "unit_price": 500,
  "total_amount": 1000,
  "currency": "MZN",
  "expires_at": "2026-08-24T14:10:00Z"
}
```

A representação concreta será definida durante a implementação.

---

# 44. Erros

A API deve diferenciar pelo menos:

```text
EVENT_NOT_FOUND
EVENT_NOT_AVAILABLE
EVENT_SOLD_OUT
INVALID_QUANTITY
RESERVATION_EXPIRED
RESERVATION_NOT_FOUND
RESERVATION_NOT_OWNED
RESERVATION_ALREADY_CONFIRMED
RESERVATION_ALREADY_CANCELLED
PAYMENT_DECLINED
```

Os códigos internos podem ser diferentes, desde que o significado permaneça claro.

---

# 45. Casos limite

## 45.1 Último ingresso

Se existir apenas um ingresso disponível, apenas uma reserva concorrente poderá obtê-lo.

---

## 45.2 Reserva exactamente igual à disponibilidade

Se:

```text
Disponível = 5
Pedido = 5
```

a reserva pode ser criada.

Depois disso:

```text
Disponível = 0
```

---

## 45.3 Pedido superior à disponibilidade

Se:

```text
Disponível = 5
Pedido = 6
```

a operação deve ser rejeitada.

---

## 45.4 Reserva expirada durante pagamento

Se o pagamento for iniciado antes da expiração, mas concluído depois do prazo, o sistema deve verificar novamente a validade antes de confirmar a reserva.

---

## 45.5 Dupla confirmação

Se o mesmo pagamento ou pedido de confirmação for processado duas vezes, apenas uma confirmação efectiva deve ocorrer.

---

## 45.6 Duplo cancelamento

Cancelar uma reserva já cancelada não deve criar novos efeitos.

A operação pode retornar o estado actual da reserva ou uma resposta equivalente.

---

## 45.7 Cliente diferente

Um Cliente não pode confirmar, cancelar ou consultar uma reserva pertencente a outro Cliente.

---

# 46. Segurança

A implementação deve proteger:

* identificação da reserva;
* identificação do Cliente;
* dados do pagamento;
* dados do evento;
* autorização das operações.

O identificador da reserva não deve ser tratado como prova suficiente de autorização.

Mesmo que um Cliente descubra o identificador de outra reserva, não deve conseguir aceder aos respectivos dados.

---

# 47. Observabilidade

As operações de reserva devem produzir informação suficiente para diagnosticar:

* criação;
* confirmação;
* expiração;
* cancelamento;
* falhas de disponibilidade;
* falhas de concorrência;
* falhas de pagamento.

Os logs não devem conter dados sensíveis desnecessários.

---

# 48. Testes

A implementação deve incluir testes para:

### Criação

* reserva válida;
* evento inexistente;
* evento não publicado;
* quantidade inválida;
* evento esgotado.

### Disponibilidade

* reserva dentro da capacidade;
* reserva igual à capacidade disponível;
* reserva acima da capacidade;
* várias reservas sequenciais.

### Concorrência

* duas reservas para a última unidade;
* múltiplas reservas simultâneas;
* concorrência em lugares numerados.

### Estado

* `PENDING → CONFIRMED`;
* `PENDING → EXPIRED`;
* `PENDING → CANCELLED`;
* tentativa de confirmação após expiração;
* confirmação duplicada;
* cancelamento duplicado.

### Segurança

* Cliente acede à própria reserva;
* Cliente não acede à reserva de outro Cliente;
* manipulação do preço;
* manipulação da quantidade;
* manipulação do identificador do Cliente.

---

# 49. Critérios de aceitação

## AC-01 — Criar reserva

**Dado** um Cliente autenticado,

**quando** seleccionar um evento publicado e uma quantidade válida,

**então** deve ser criada uma reserva `PENDING`.

---

## AC-02 — Reservar disponibilidade

**Dado** um evento com disponibilidade suficiente,

**quando** uma reserva for criada,

**então** a quantidade correspondente deve ficar temporariamente indisponível para outros Clientes.

---

## AC-03 — Evento esgotado

**Dado** um evento sem disponibilidade,

**quando** um Cliente tentar reservar,

**então** a operação deve ser rejeitada.

---

## AC-04 — Expiração

**Dado** uma reserva `PENDING` cujo prazo terminou,

**quando** o sistema verificar a reserva,

**então** esta deve ser tratada como `EXPIRED` e a disponibilidade deve ser libertada.

---

## AC-05 — Pagamento aprovado

**Dado** uma reserva `PENDING` ainda válida,

**quando** o pagamento for aprovado,

**então** a reserva deve passar para `CONFIRMED`.

---

## AC-06 — Pagamento recusado

**Dado** uma reserva `PENDING`,

**quando** o pagamento for recusado,

**então** a reserva não deve passar para `CONFIRMED`.

---

## AC-07 — Último ingresso

**Dado** que existe apenas uma unidade disponível,

**quando** dois Clientes tentarem reservá-la simultaneamente,

**então** apenas uma reserva deve ser aceite.

---

## AC-08 — Preço

**Dado** um evento com preço definido,

**quando** o Cliente criar uma reserva,

**então** o backend deve calcular o valor total com base no preço persistido.

---

## AC-09 — Segurança

**Dado** uma reserva pertencente ao Cliente A,

**quando** o Cliente B tentar aceder-lhe,

**então** a operação deve ser rejeitada.

---

## AC-10 — Idempotência

**Dado** uma reserva já confirmada,

**quando** a confirmação for submetida novamente,

**então** o sistema não deve criar efeitos duplicados.

---

# 50. Regras de integridade

A implementação deve garantir permanentemente:

```text
1. Uma reserva pertence a exactamente um Cliente.
2. Uma reserva pertence a exactamente um evento.
3. Uma reserva possui um estado válido.
4. Uma reserva PENDING possui um prazo de validade.
5. Uma reserva CONFIRMED não pode voltar para PENDING.
6. Uma reserva EXPIRED não pode ser confirmada.
7. Uma reserva CANCELLED não pode ser confirmada.
8. A capacidade comprometida não pode exceder a capacidade do evento.
9. O preço da reserva é determinado pelo backend.
10. Um Cliente não pode manipular reservas de outro Cliente.
11. Um lugar não pode ser confirmado para dois Clientes no mesmo evento.
12. A confirmação deve ser idempotente.
```

---

# 51. Confirmação

A conformidade desta especificação deve ser validada através de:

1. testes unitários;
2. testes de integração;
3. testes de API;
4. testes de concorrência;
5. testes de autorização;
6. testes de transacções;
7. execução manual do fluxo completo;
8. demonstração de que a capacidade nunca é ultrapassada.

A validação deve incluir pelo menos um cenário em que dois Clientes tentam adquirir simultaneamente a última unidade disponível.

---

# 52. Dependências

Esta especificação depende de:

* Autenticação e Autorização;
* Descoberta de Eventos;
* Gestão de Eventos.

É utilizada posteriormente por:

* Pagamentos;
* Ingressos;
* Validação de Ingressos.

---

# 53. Fluxo completo

O fluxo esperado é:

```text
Cliente
   │
   ▼
Consulta eventos publicados
   │
   ▼
Selecciona evento
   │
   ▼
Selecciona quantidade/lugares
   │
   ▼
Cria reserva
   │
   ▼
PENDING
   │
   ▼
Pagamento
   │
   ├───────────────┐
   │               │
APROVADO        RECUSADO
   │               │
   ▼               ▼
CONFIRMED       permanece
   │             PENDING
   │               │
   ▼               ▼
Emissão       nova tentativa
de ingresso
```

Se o prazo terminar:

```text
PENDING
   │
   ▼
EXPIRED
   │
   ▼
Disponibilidade libertada
```

---

# 54. Resultado esperado

No final desta funcionalidade, a plataforma deve permitir que um Cliente:

1. consulte um evento publicado;
2. veja a disponibilidade;
3. seleccione uma quantidade ou lugares;
4. crie uma reserva;
5. tenha a disponibilidade temporariamente retida;
6. efectue um pagamento simulado;
7. receba confirmação quando o pagamento for aprovado;
8. não consiga reservar mais capacidade do que a disponível;
9. não consiga adquirir um lugar já reservado por outro Cliente;
10. não consiga manipular o preço ou a identidade da reserva.

A implementação desta especificação constitui a base para a emissão de ingressos e para o fluxo de validação na portaria.