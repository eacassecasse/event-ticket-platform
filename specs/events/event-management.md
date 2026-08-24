# Especificação de Gestão de Eventos

**Estado:** `approved`  
**Versão:** `1.0`  
**Última actualização:** `2026-08-24`

---

# 1. Objectivo

Esta especificação define o comportamento dos eventos geridos pela Plataforma de Eventos e Ingressos.

Um evento representa uma ocorrência concreta que pode ser disponibilizada para aquisição de ingressos pelos Clientes.

O evento pode ter como origem um conteúdo seleccionado a partir de uma API externa, conforme definido na Especificação de Descoberta de Eventos, mas a ocorrência concreta pertence à plataforma e é gerida pelo Organizador.

Esta especificação define:

- criação;
- consulta;
- edição;
- publicação;
- disponibilidade;
- capacidade;
- preço;
- localização;
- ciclo de vida;
- propriedade;
- regras de alteração;
- condições que permitem ou impedem determinadas operações.

---

# 2. Âmbito

Esta especificação cobre:

- criação de eventos;
- identificação de eventos;
- associação a conteúdos externos;
- propriedade do evento;
- dados do evento;
- capacidade;
- preço;
- data e hora;
- local;
- estado do evento;
- publicação;
- consulta de eventos publicados;
- edição;
- validação dos dados;
- regras de disponibilidade.

Esta especificação não cobre:

- reservas;
- pagamento;
- emissão de ingressos;
- validação de ingressos;
- envio de correio electrónico;
- reembolsos.

Essas responsabilidades pertencem a outros domínios.

---

# 3. Conceito de evento

Um evento é uma ocorrência concreta que pode ser frequentada por Clientes.

Exemplo:

```text
Evento
│
├── Título
├── Descrição
├── Data
├── Hora
├── Local
├── Capacidade
├── Preço
├── Estado
├── Organizador
└── Conteúdo externo
````

O evento deve possuir uma identidade própria dentro da plataforma.

O identificador utilizado pela API externa não deve ser utilizado como identificador principal do evento.

---

# 4. Relação com o catálogo externo

Um evento pode ter sido criado a partir de um conteúdo obtido através de:

* Ticketmaster;
* TMDb.

A relação conceptual é:

```text
Conteúdo externo
       │
       │ utilizado como referência
       ▼
    Evento
       │
       ├── Data própria
       ├── Hora própria
       ├── Local próprio
       ├── Capacidade própria
       └── Preço próprio
```

O conteúdo externo descreve o que está a ser apresentado.

O evento descreve quando, onde e em que condições essa apresentação ocorrerá.

---

# 5. Identidade do evento

Cada evento deve possuir um identificador único gerado pela plataforma.

Esse identificador:

* não deve depender do identificador externo;
* deve permanecer estável durante o ciclo de vida do evento;
* deve ser utilizado nas relações internas;
* deve ser utilizado pela API para identificar o evento.

---

# 6. Dados obrigatórios

Para que um evento possa ser publicado, deve possuir pelo menos:

* título;
* descrição ou informação equivalente suficiente para apresentação;
* data;
* hora;
* local;
* capacidade;
* preço;
* Organizador responsável.

Quando o evento for criado a partir de um conteúdo externo, deve manter a referência à respectiva fonte e identificador externo quando estes estiverem disponíveis.

---

# 7. Data e hora

A data e hora do evento representam o momento em que o evento ocorrerá.

A aplicação deve validar que:

* a data possui formato válido;
* a hora possui formato válido;
* a combinação data/hora é válida;
* um evento publicado não pode ser configurado para um momento já passado.

A aplicação deve tratar explicitamente o fuso horário utilizado pelo sistema.

Para o contexto inicial da aplicação, deve ser utilizada uma política de fuso horário consistente em toda a plataforma.

---

# 8. Local

O evento deve possuir informação suficiente para permitir ao Cliente identificar onde ocorrerá.

O local poderá ser representado inicialmente por:

```text
Nome do local
Morada
Cidade
```

O modelo poderá ser expandido posteriormente para suportar:

* coordenadas geográficas;
* sectores;
* edifícios;
* salas;
* mapas.

Essas extensões não são necessárias para o MVP.

---

# 9. Capacidade

A capacidade representa o número máximo de ingressos que podem ser vendidos para o evento.

Exemplo:

```text
Capacidade = 500
```

significa que, no máximo, 500 ingressos podem ser confirmados para esse evento.

A capacidade deve ser um número inteiro positivo.

Valores iguais a zero ou negativos não são válidos para um evento publicável.

---

# 10. Disponibilidade

A disponibilidade representa a quantidade de ingressos que ainda pode ser adquirida.

Conceptualmente:

```text
Disponibilidade =
    Capacidade
    -
    Quantidade de ingressos confirmados
```

Exemplo:

```text
Capacidade: 500
Vendidos:   137
Disponíveis: 363
```

A disponibilidade não deve ser definida manualmente pelo utilizador.

Deve ser determinada pelo estado das reservas e ingressos aplicáveis.

---

# 11. Preço

O preço representa o valor de um ingresso.

O preço deve:

* ser numérico;
* não ser negativo;
* possuir precisão adequada à moeda utilizada;
* utilizar uma moeda explicitamente definida pela aplicação.

Para o MVP, deve ser utilizada uma única moeda.

O preço de um evento não deve depender de uma API externa.

---

# 12. Estado do evento

Um evento deve possuir um estado de ciclo de vida.

O conjunto mínimo é:

```text
DRAFT
PUBLISHED
CANCELLED
COMPLETED
```

### DRAFT

O evento está a ser preparado.

Não está disponível para compra pública.

### PUBLISHED

O evento está disponível para consulta e aquisição de ingressos.

### CANCELLED

O evento foi cancelado.

Não devem ser permitidas novas reservas.

### COMPLETED

O evento já terminou.

Não devem ser permitidas novas reservas ou validações de entrada.

---

# 13. Estado inicial

Um evento deve ser criado inicialmente no estado:

```text
DRAFT
```

A criação não deve publicar automaticamente o evento.

Isto permite ao Organizador verificar os dados antes de disponibilizar o evento aos Clientes.

---

# 14. Publicação

Um evento só pode passar de `DRAFT` para `PUBLISHED` quando cumprir todos os requisitos obrigatórios.

Fluxo:

```text
DRAFT
  │
  │ publicar
  ▼
PUBLISHED
```

Se existirem dados obrigatórios em falta ou inválidos, a publicação deve ser rejeitada.

---

# 15. Cancelamento

Um evento publicado pode ser cancelado pelo Organizador responsável, de acordo com as regras de negócio.

Fluxo:

```text
PUBLISHED
     │
     │ cancelar
     ▼
CANCELLED
```

Depois de cancelado:

* não podem ser realizadas novas reservas;
* o evento deixa de estar disponível para aquisição;
* os ingressos existentes devem manter informação suficiente para identificar que o evento foi cancelado.

O tratamento de reembolsos não pertence a esta especificação.

---

# 16. Conclusão do evento

Depois de o evento ocorrer, o sistema poderá classificá-lo como:

```text
COMPLETED
```

A transição deverá ocorrer quando o evento tiver terminado.

Para o MVP, esta transição pode ser realizada através de uma operação administrativa ou mecanismo simples definido pela implementação.

Não é necessário implementar um sistema automático complexo de agendamento.

---

# 17. Transições de estado

As transições permitidas são:

```text
DRAFT
  │
  └──► PUBLISHED
          │
          ├──► CANCELLED
          │
          └──► COMPLETED
```

Não devem ser permitidas transições arbitrárias.

Por exemplo:

```text
CANCELLED ──► PUBLISHED
```

não deve ser permitido sem uma decisão explícita de negócio que introduza essa possibilidade.

Para o MVP, eventos cancelados permanecem cancelados.

---

# 18. Propriedade do evento

Cada evento deve possuir um Organizador responsável.

O Organizador que criou o evento deve ser considerado o seu proprietário.

Um Organizador só pode:

* consultar os seus eventos;
* editar os seus eventos;
* publicar os seus eventos;
* cancelar os seus eventos.

Não pode alterar eventos pertencentes a outro Organizador.

Esta regra complementa a autorização baseada em papéis definida na Especificação de Autenticação e Autorização.

---

# 19. Edição de eventos

Um evento em estado `DRAFT` pode ser editado pelo seu Organizador.

Podem ser alterados:

* título;
* descrição;
* data;
* hora;
* local;
* capacidade;
* preço;
* referência ao conteúdo, quando permitido pela implementação.

---

# 20. Edição de eventos publicados

Eventos em estado `PUBLISHED` devem possuir regras mais restritivas.

Alterações que possam afectar reservas existentes devem ser evitadas ou explicitamente controladas.

Para o MVP, recomenda-se:

* permitir alterações de informação descritiva;
* permitir alterações de preço apenas quando não existirem reservas confirmadas;
* não permitir redução da capacidade abaixo da quantidade já confirmada;
* não permitir alterações que tornem o evento inválido.

---

# 21. Capacidade e reservas existentes

A capacidade não pode ser reduzida para um valor inferior à quantidade de ingressos já confirmados.

Exemplo:

```text
Capacidade actual: 500
Ingressos confirmados: 300
```

Uma alteração para:

```text
Capacidade: 250
```

deve ser rejeitada.

Uma alteração para:

```text
Capacidade: 350
```

é tecnicamente possível, desde que todas as restantes regras sejam cumpridas.

---

# 22. Preço e reservas existentes

Se existirem reservas confirmadas, a alteração do preço deve ser tratada com cuidado.

Para o MVP:

> O preço de um evento publicado não deve ser alterado depois de existirem reservas confirmadas.

Isto evita ambiguidades sobre o valor que um Cliente deve pagar.

---

# 23. Consulta pública

Apenas eventos no estado:

```text
PUBLISHED
```

devem aparecer na área pública de descoberta de eventos.

Eventos em:

```text
DRAFT
CANCELLED
COMPLETED
```

não devem aparecer como eventos disponíveis para aquisição.

---

# 24. Consulta de eventos do Organizador

O Organizador deve conseguir consultar os eventos sob a sua responsabilidade, independentemente do estado.

Exemplo:

```text
Organizador
│
├── Evento A — DRAFT
├── Evento B — PUBLISHED
├── Evento C — CANCELLED
└── Evento D — COMPLETED
```

O Cliente, por outro lado, deve consultar apenas os eventos que lhe são disponibilizados pela experiência pública.

---

# 25. Disponibilidade para compra

Um evento publicado pode deixar de ter disponibilidade mesmo permanecendo no estado:

```text
PUBLISHED
```

Por exemplo:

```text
Capacidade: 100
Confirmados: 100
Disponíveis: 0
```

Nesse caso, o evento continua publicado, mas não pode aceitar novas reservas.

A interface deve comunicar claramente que o evento está esgotado.

---

# 26. Concorrência

A capacidade deve ser protegida contra reservas concorrentes.

O sistema não pode confiar apenas em:

```text
if available >= requested:
    create_reservation()
```

quando múltiplos pedidos podem ser processados simultaneamente.

A confirmação da reserva deve ser protegida por mecanismos transaccionais adequados no backend e na base de dados.

O objectivo é garantir:

```text
ingressos_confirmados <= capacidade
```

em qualquer momento.

---

# 27. Integridade da capacidade

A aplicação deve garantir que:

```text
0 <= ingressos_confirmados <= capacidade
```

Nunca deve existir um estado persistido em que:

```text
ingressos_confirmados > capacidade
```

A regra deve ser protegida no nível apropriado da arquitectura.

---

# 28. Eliminação

Para preservar o histórico da plataforma, eventos que já tenham sido publicados ou que possuam reservas não devem ser eliminados fisicamente.

A utilização de estados como:

```text
CANCELLED
COMPLETED
```

permite preservar o histórico.

A eliminação física poderá ser considerada posteriormente para dados que não possuam dependências.

---

# 29. Identificação pública

O identificador público do evento deve permitir que o frontend:

* apresente detalhes;
* crie links;
* consulte disponibilidade;
* inicie uma reserva.

O identificador não deve expor informação sensível sobre o Organizador.

---

# 30. URL partilhável

Um evento publicado deve poder ser identificado através de um endereço estável.

Exemplo conceptual:

```text
/events/{event_id}
```

O link deve continuar a identificar o evento enquanto este existir no sistema.

---

# 31. Validação

Antes da criação ou publicação, o sistema deve validar:

### Identificação

* identificador único;
* Organizador válido.

### Informação

* título válido;
* descrição válida quando obrigatória;
* local válido.

### Data

* data válida;
* hora válida;
* evento não iniciado.

### Capacidade

* inteiro positivo.

### Preço

* valor não negativo;
* moeda válida.

### Estado

* transição permitida.

---

# 32. Regras de publicação

A publicação deve ser rejeitada quando:

* o título estiver vazio;
* a data for inválida;
* a data já tiver passado;
* o local estiver incompleto;
* a capacidade for inválida;
* o preço for inválido;
* o Organizador não existir ou não estiver autorizado;
* a transição de estado não for permitida.

---

# 33. Regras de acesso

A autorização deve seguir:

```text
                    Evento
                       │
            ┌──────────┴──────────┐
            │                     │
       Público                Organizador
            │                     │
            ▼                     ▼
      PUBLISHED            Próprios eventos
```

Um Cliente não deve conseguir consultar dados privados de eventos em `DRAFT`.

Um Organizador não deve conseguir alterar eventos de outro Organizador.

---

# 34. API conceptual

A API deverá suportar comportamentos equivalentes a:

```text
POST   /events
GET    /events
GET    /events/{event_id}

GET    /organizer/events
GET    /organizer/events/{event_id}

PATCH  /organizer/events/{event_id}

POST   /organizer/events/{event_id}/publish
POST   /organizer/events/{event_id}/cancel
```

Os endpoints concretos serão definidos durante a implementação.

A interface deve respeitar as regras de autorização e ciclo de vida desta especificação.

---

# 35. Modelo conceptual

O modelo mínimo pode ser representado como:

```text
Organizer
    │
    │ 1
    │
    │ N
    ▼
  Event
    │
    ├── external_source
    ├── external_id
    ├── title
    ├── description
    ├── date
    ├── time
    ├── venue
    ├── capacity
    ├── price
    └── status
```

As relações com:

* reservas;
* ingressos;
* pagamentos;

serão definidas nas respectivas especificações.

---

# 36. Critérios de aceitação

## AC-01 — Criar evento

**Dado** um Organizador autenticado,

**quando** fornecer os dados necessários,

**então** o sistema deve criar um evento no estado `DRAFT`.

---

## AC-02 — Publicar evento

**Dado** um evento válido em `DRAFT`,

**quando** o Organizador o publicar,

**então** o evento deve passar para `PUBLISHED`.

---

## AC-03 — Publicação inválida

**Dado** um evento com dados obrigatórios inválidos,

**quando** o Organizador tentar publicá-lo,

**então** a publicação deve ser rejeitada.

---

## AC-04 — Consulta pública

**Dado** um evento em `PUBLISHED`,

**quando** um Cliente consultar os eventos,

**então** o evento deve aparecer.

---

## AC-05 — Evento em rascunho

**Dado** um evento em `DRAFT`,

**quando** um Cliente consultar os eventos públicos,

**então** o evento não deve aparecer.

---

## AC-06 — Isolamento de Organizador

**Dado** um evento pertencente ao Organizador A,

**quando** o Organizador B tentar alterá-lo,

**então** a operação deve ser rejeitada.

---

## AC-07 — Capacidade

**Dado** um evento com capacidade 100,

**quando** existirem 100 ingressos confirmados,

**então** o sistema não deve aceitar uma nova reserva.

---

## AC-08 — Capacidade concorrente

**Dado** que existem poucos lugares disponíveis,

**quando** múltiplos Clientes tentarem reservar simultaneamente,

**então** o sistema deve garantir que a capacidade não seja ultrapassada.

---

## AC-09 — Cancelamento

**Dado** um evento publicado,

**quando** o Organizador autorizado o cancelar,

**então** o evento deve passar para `CANCELLED` e novas reservas devem ser impedidas.

---

## AC-10 — Evento concluído

**Dado** um evento que já terminou,

**quando** for marcado como concluído,

**então** deve passar para `COMPLETED` e deixar de aceitar novas reservas.

---

# 37. Casos limite

## 37.1 Capacidade igual a zero

Um evento com capacidade zero não deve ser publicado.

---

## 37.2 Preço negativo

Um preço negativo deve ser rejeitado.

---

## 37.3 Data passada

Um evento não deve ser publicado para uma data já passada.

---

## 37.4 Capacidade inferior às reservas

Uma redução de capacidade que torne inválidas as reservas existentes deve ser rejeitada.

---

## 37.5 Dois pedidos simultâneos

A aplicação deve impedir que duas reservas consumam o mesmo lugar lógico ou ultrapassem a capacidade.

---

## 37.6 Evento cancelado

Um evento cancelado não deve aceitar novas reservas.

---

## 37.7 Evento concluído

Um evento concluído não deve aceitar novas reservas.

---

## 37.8 Organizador inexistente

Um evento não pode ser criado sem um Organizador válido.

---

## 37.9 Evento sem conteúdo externo

A aplicação pode permitir eventos sem uma referência externa, desde que esta opção seja compatível com o fluxo escolhido.

O requisito obrigatório é que o evento seja operacionalmente completo.

---

# 38. Testes

A implementação deve possuir testes para:

* criação;
* validação;
* publicação;
* cancelamento;
* conclusão;
* consulta pública;
* consulta pelo Organizador;
* isolamento entre Organizadores;
* capacidade;
* alteração da capacidade;
* alteração do preço;
* datas inválidas;
* estados inválidos;
* eventos esgotados;
* concorrência de reservas.

Os testes de capacidade e concorrência são particularmente importantes porque representam uma regra de integridade do domínio.

---

# 39. Confirmação

A conformidade com esta especificação deve ser confirmada através de:

1. testes automatizados do ciclo de vida;
2. testes de autorização;
3. testes de validação;
4. testes de capacidade;
5. testes de concorrência;
6. testes de consulta pública;
7. testes de isolamento entre Organizadores;
8. execução do fluxo completo através da aplicação.

---

# 40. Questões em aberto

As seguintes decisões serão definidas durante a implementação:

* representação exacta do local;
* estratégia exacta para alteração automática para `COMPLETED`;
* mecanismo de identificação pública;
* estratégia de armazenamento dos dados provenientes do catálogo externo;
* política de cancelamento de reservas;
* eventual suporte futuro para sectores e lugares numerados.

Estas decisões não devem alterar as regras fundamentais desta especificação.

---

# 41. Referências

* Especificação de Autenticação e Autorização.
* Especificação de Descoberta de Eventos.
* Especificação de Reservas.
* Especificação de Pagamentos.
* Especificação de Ingressos.
* Especificação de Validação de Ingressos.
* Requisitos funcionais do desafio Elite Dev.