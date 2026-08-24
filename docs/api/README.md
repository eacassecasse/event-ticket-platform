# Documentação da API

## 1. Objectivo

A pasta `docs/api/` contém a documentação técnica da API disponibilizada pelo backend da plataforma.

Esta documentação descreve o contrato através do qual aplicações clientes e outros sistemas comunicam com o backend.

O seu objectivo é permitir que um developer consiga compreender como utilizar a API sem precisar de conhecer previamente a implementação interna do backend.

A documentação deve responder, entre outras, às seguintes perguntas:

- Que recursos a API disponibiliza?
- Que operações podem ser realizadas?
- Que dados devem ser enviados?
- Que dados são devolvidos?
- Como funciona a autenticação?
- Que permissões são necessárias?
- Como são representados os erros?
- Que regras importantes devem ser respeitadas pelo consumidor?
- Como podem os endpoints ser testados?

---

# 2. Âmbito

Esta área documenta o contrato público da API, incluindo:

- endpoints;
- métodos HTTP;
- parâmetros;
- query parameters;
- request bodies;
- response bodies;
- códigos HTTP;
- autenticação;
- autorização;
- paginação;
- filtragem;
- ordenação;
- validação;
- erros;
- requisitos específicos de cada recurso;
- exemplos de utilização;
- versões da API.

Não deve ser utilizada para documentar detalhes internos que não façam parte do contrato da API.

Por exemplo, a documentação da API não deve depender de informações como:

- classes internas;
- nomes de funções privadas;
- implementação específica dos repositories;
- estrutura interna dos services;
- detalhes de ORM;
- decisões de infraestrutura que não afectem o consumidor da API.

Esses conteúdos pertencem à documentação de arquitectura ou desenvolvimento.

---

# 3. Princípio de contrato

A API deve ser tratada como um contrato entre o backend e os seus consumidores.

A relação é:

```text
┌────────────────────┐
│ API Consumer       │
│                    │
│ Web application    │
│ External client    │
└─────────┬──────────┘
          │
          │ HTTP
          │
          ▼
┌────────────────────┐
│ API Contract       │
│                    │
│ Requests           │
│ Responses          │
│ Errors             │
│ Authentication     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Backend            │
│                    │
│ Business logic     │
│ Persistence        │
│ Integrations       │
└────────────────────┘
````

Alterações ao contrato devem ser tratadas com cuidado porque podem afectar múltiplos consumidores.

---

# 4. Versionamento

A API será organizada por versões.

A primeira versão pública será identificada como:

```text
/v1
```

Exemplo:

```text
/api/v1/events
```

A versão representa o contrato da API e não necessariamente a versão do software.

Uma nova versão deve ser considerada quando uma alteração incompatível não puder ser introduzida de forma segura na versão existente.

Alterações compatíveis devem, sempre que possível, ser introduzidas na versão actual.

---

# 5. Estrutura conceptual dos recursos

A API deve utilizar recursos que representem entidades ou conceitos do domínio.

Para esta plataforma, os principais recursos incluem:

```text
events
reservations
tickets
users
auth
```

Poderão ser adicionados outros recursos à medida que os requisitos forem detalhados.

Os nomes dos recursos devem ser consistentes e utilizar substantivos em vez de representar directamente acções.

Preferir:

```text
GET /api/v1/events
```

em vez de:

```text
GET /api/v1/get-events
```

---

# 6. Métodos HTTP

A API deve utilizar os métodos HTTP de acordo com a intenção da operação.

| Método   | Utilização principal                                                                              |
| -------- | ------------------------------------------------------------------------------------------------- |
| `GET`    | Obter recursos                                                                                    |
| `POST`   | Criar recursos ou executar operações que não sejam adequadamente representadas como actualizações |
| `PUT`    | Substituir um recurso                                                                             |
| `PATCH`  | Alterar parcialmente um recurso                                                                   |
| `DELETE` | Remover ou desactivar um recurso                                                                  |

A escolha do método deve representar a semântica da operação e não apenas a conveniência da implementação.

---

# 7. Autenticação

A plataforma possui três papéis funcionais principais:

```text
Organizador
Cliente
Portaria
```

A API deve validar a identidade do utilizador antes de processar operações protegidas.

A autenticação e autorização são conceitos distintos:

```text
Autenticação
    │
    ▼
Quem é o utilizador?
    │
    ▼
Autorização
    │
    ▼
O que pode este utilizador fazer?
```

Um utilizador autenticado não deve automaticamente possuir acesso a todos os recursos.

---

# 8. Autorização

As permissões devem ser determinadas de acordo com o papel e o contexto da operação.

Exemplo conceptual:

| Operação                        | Organizador | Cliente | Portaria |
| ------------------------------- | ----------: | ------: | -------: |
| Consultar eventos publicados    |         Sim |     Sim |      Sim |
| Criar evento                    |         Sim |     Não |      Não |
| Gerir evento próprio            |         Sim |     Não |      Não |
| Reservar ingresso               |         Não |     Sim |      Não |
| Consultar os próprios ingressos |         Não |     Sim |      Não |
| Validar ingresso                |         Não |     Não |      Sim |

A tabela representa a intenção funcional e deve ser actualizada quando os requisitos forem alterados.

A implementação efectiva da autorização pertence ao backend.

---

# 9. Request

Cada endpoint deve documentar claramente os dados que aceita.

Quando aplicável, devem ser documentados:

* headers;
* path parameters;
* query parameters;
* request body;
* tipos de dados;
* campos obrigatórios;
* campos opcionais;
* limites;
* valores permitidos;
* regras de validação.

Exemplo conceptual:

```http
POST /api/v1/reservations
Content-Type: application/json
Authorization: Bearer <token>
```

```json
{
  "event_id": "event-id",
  "quantity": 2
}
```

O exemplo serve apenas para demonstrar a estrutura documental. O contrato definitivo deve reflectir os schemas implementados.

---

# 10. Response

Cada endpoint deve documentar a resposta esperada.

Devem ser indicados:

* código HTTP;
* estrutura da resposta;
* campos;
* tipos;
* significado dos valores;
* campos opcionais;
* condições especiais.

Exemplo conceptual:

```http
HTTP/1.1 201 Created
Content-Type: application/json
```

```json
{
  "id": "reservation-id",
  "status": "confirmed"
}
```

Os exemplos devem permanecer sincronizados com a implementação.

---

# 11. Códigos HTTP

A API deve utilizar códigos HTTP semanticamente apropriados.

Exemplos:

| Código                      | Significado                                                                                  |
| --------------------------- | -------------------------------------------------------------------------------------------- |
| `200 OK`                    | Operação concluída                                                                           |
| `201 Created`               | Recurso criado                                                                               |
| `204 No Content`            | Operação concluída sem conteúdo de resposta                                                  |
| `400 Bad Request`           | Pedido inválido                                                                              |
| `401 Unauthorized`          | Autenticação necessária ou inválida                                                          |
| `403 Forbidden`             | Utilizador autenticado sem permissão                                                         |
| `404 Not Found`             | Recurso não encontrado                                                                       |
| `409 Conflict`              | Conflito com o estado actual do recurso                                                      |
| `422 Unprocessable Content` | Dados estruturalmente válidos, mas que não podem ser processados devido às regras aplicáveis |
| `429 Too Many Requests`     | Limite de pedidos excedido                                                                   |
| `500 Internal Server Error` | Erro interno inesperado                                                                      |

A aplicação não deve utilizar códigos de erro apenas para comunicar uma mensagem conveniente.

O código deve representar correctamente a natureza da situação.

---

# 12. Erros

As respostas de erro devem possuir uma estrutura consistente.

Um exemplo conceptual:

```json
{
  "error": {
    "code": "TICKET_ALREADY_USED",
    "message": "The ticket has already been validated."
  }
}
```

Os códigos internos devem ser estáveis e adequados para utilização programática.

As mensagens destinam-se principalmente à compreensão humana.

Os consumidores não devem depender da comparação exacta de mensagens textuais para determinar o tipo de erro.

---

# 13. Erros de domínio

Erros relacionados com regras de negócio devem ser distinguidos de erros técnicos.

Exemplos:

```text
Lugar já reservado
Ingresso já utilizado
Ingresso pertence a outro evento
Evento encerrado
Pagamento recusado
Utilizador sem permissão
```

Estes casos não representam necessariamente falhas técnicas do servidor.

Devem ser tratados como estados ou conflitos do domínio e documentados como tal.

---

# 14. Reservas e concorrência

A reserva de ingressos possui uma característica crítica: dois clientes não podem adquirir o mesmo lugar ou ultrapassar a capacidade disponível.

Consequentemente, a API não deve depender exclusivamente de verificações realizadas no frontend.

O backend deve garantir a integridade da operação.

Conceptualmente:

```text
Client A ──────┐
               │
               ▼
           Backend
               │
               ▼
         Transaction
               │
               ▼
          Database
               │
               ├── Resource available → reserve
               │
               └── Resource unavailable → conflict
```

A implementação concreta desta garantia pertence à arquitectura do backend e à camada de persistência.

---

# 15. Pagamento simulado

O pagamento utilizado neste desafio não representa uma transacção financeira real.

A API deve, contudo, representar claramente os estados necessários para o fluxo.

Por exemplo:

```text
pending
approved
declined
```

Os estados definitivos devem ser definidos na especificação funcional e implementados de forma consistente no backend.

O frontend não deve assumir que um pagamento foi concluído apenas porque o pedido foi enviado.

---

# 16. Bilhetes

Cada ingresso deve possuir um identificador que permita à aplicação identificar o ingresso durante a validação.

O mecanismo utilizado para representar o ingresso através de QR Code não deve permitir que um utilizador simplesmente altere dados visíveis e produza um ingresso aceite pelo sistema.

A validação deve ocorrer no backend.

Conceptualmente:

```text
QR Code
   │
   ▼
Portaria
   │
   ▼
API
   │
   ├── ingresso inexistente
   ├── assinatura inválida
   ├── evento incorrecto
   ├── ingresso já utilizado
   │
   └── ingresso válido
```

O QR Code é um mecanismo de transporte da informação. A decisão de validade pertence ao backend.

---

# 17. Validação de ingressos

A operação de validação deve garantir que o mesmo ingresso não possa ser utilizado duas vezes.

A resposta deve distinguir, quando aplicável:

```text
VALID
INVALID
ALREADY_USED
WRONG_EVENT
```

Os nomes definitivos devem ser definidos no contrato implementado.

Uma validação não deve ser considerada bem-sucedida simplesmente porque o código possui um formato válido.

O backend deve verificar o estado real do ingresso.

---

# 18. Idempotência

Operações que possam ser repetidas devido a retries de rede devem ser analisadas quanto ao seu comportamento.

Particular atenção deve ser dada a:

* criação de reservas;
* confirmação de pagamento;
* geração de bilhetes;
* validação de ingressos.

Quando uma operação não puder ser repetida de forma segura, deve existir uma estratégia explícita para evitar duplicação ou inconsistência.

---

# 19. Paginação

Endpoints que possam devolver grandes conjuntos de recursos devem utilizar paginação.

Exemplo conceptual:

```text
GET /api/v1/events?page=1&page_size=20
```

A resposta pode incluir:

```json
{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 100
}
```

A estrutura definitiva deve ser definida no contrato da API.

---

# 20. Filtragem e pesquisa

Quando um endpoint disponibilizar pesquisa ou filtragem, os parâmetros devem possuir nomes consistentes e comportamento documentado.

Exemplo:

```text
GET /api/v1/events?search=cinema
```

ou:

```text
GET /api/v1/events?date=2026-08-30
```

Os filtros suportados devem ser explicitamente documentados.

O backend deve validar os valores recebidos antes de os utilizar.

---

# 21. Integrações externas

A plataforma pode utilizar APIs externas como:

* Ticketmaster Discovery API;
* TMDb.

A comunicação com esses serviços deve ser tratada como uma integração externa e não como parte do domínio interno.

Conceptualmente:

```text
                    ┌──────────────────┐
                    │ Ticketmaster     │
                    └────────▲─────────┘
                             │
                             │
┌──────────────┐      ┌──────┴───────┐
│ Web          │─────▶│ Backend API  │
└──────────────┘      └──────┬───────┘
                             │
                    ┌────────▼────────┐
                    │ TMDb            │
                    └─────────────────┘
```

A API interna não deve expor directamente o contrato do fornecedor externo sem necessidade.

O backend deve adaptar os dados externos ao modelo utilizado pela plataforma.

---

# 22. Dependência de fornecedores externos

Os consumidores da API devem depender do contrato da aplicação e não directamente do fornecedor externo.

Por exemplo, uma resposta de um fornecedor externo pode possuir campos que não fazem parte do domínio da plataforma.

O backend deve realizar a transformação necessária:

```text
External API
     │
     ▼
Integration layer
     │
     ▼
Internal model
     │
     ▼
Application API
     │
     ▼
Frontend
```

Esta separação reduz a dependência directa do frontend em relação ao fornecedor.

---

# 23. Segurança

A documentação da API não deve revelar:

* secrets;
* API keys;
* tokens reais;
* credenciais;
* informação interna desnecessária;
* detalhes que facilitem ataques sem benefício legítimo para o consumidor.

Exemplos de requests devem utilizar placeholders:

```text
<token>
<api-key>
<event-id>
<reservation-id>
```

---

# 24. Rate limiting

Quando o backend aplicar rate limiting, os consumidores devem ser informados sobre:

* quais endpoints são limitados;
* limites aplicáveis;
* comportamento quando o limite é excedido;
* headers relevantes, quando existentes.

Uma resposta de excesso de pedidos deve utilizar:

```text
429 Too Many Requests
```

quando essa situação corresponder efectivamente ao limite configurado.

---

# 25. Compatibilidade

Alterações ao contrato devem ser classificadas como compatíveis ou incompatíveis.

Exemplos geralmente compatíveis:

* adicionar um campo opcional;
* adicionar um novo endpoint;
* adicionar uma nova opção que não invalide consumidores existentes.

Exemplos potencialmente incompatíveis:

* remover um campo;
* alterar o tipo de um campo;
* alterar o significado de um valor;
* tornar obrigatório um campo anteriormente opcional;
* remover um endpoint;
* alterar a semântica de uma operação.

Alterações incompatíveis devem ser tratadas de acordo com a estratégia de versionamento definida pelo projecto.

---

# 26. OpenAPI

Quando a implementação utilizar OpenAPI, o schema gerado pela aplicação deve ser considerado uma representação técnica importante do contrato.

A documentação manual em `docs/api/` deve complementar o schema, não contradizê-lo.

A relação deve ser:

```text
API implementation
       │
       ▼
OpenAPI schema
       │
       ├── API documentation
       ├── Client tooling
       └── Validation
```

Quando a documentação manual e o schema apresentarem informações diferentes, a inconsistência deve ser corrigida.

---

# 27. Organização futura

À medida que o número de endpoints crescer, a documentação poderá ser dividida por domínio.

Exemplo:

```text
docs/
└── api/
    ├── README.md
    ├── authentication.md
    ├── events.md
    ├── reservations.md
    ├── tickets.md
    └── users.md
```

A divisão deve ocorrer quando a quantidade de informação justificar a separação.

Não devem ser criados ficheiros individuais para recursos que ainda possuam documentação pequena.

---

# 28. Testes do contrato

Quando possível, os contratos documentados devem ser verificados através de testes.

A validação pode incluir:

* schema validation;
* testes de endpoint;
* testes de autorização;
* testes de códigos HTTP;
* testes de resposta;
* testes de casos de erro;
* testes de integração.

O objectivo é reduzir a possibilidade de a documentação afirmar um comportamento que a API já não implementa.

---

# 29. Fonte de verdade

A API possui várias representações relacionadas:

```text
Requisitos
    │
    ▼
Especificação
    │
    ▼
API contract
    │
    ├── OpenAPI
    │
    ├── docs/api/
    │
    └── Tests
          │
          ▼
      Implementation
```

Cada camada possui uma finalidade diferente.

Os requisitos definem a necessidade.

A especificação define o comportamento esperado.

O contrato define como esse comportamento é exposto aos consumidores.

O OpenAPI representa formalmente o contrato.

A documentação explica o contrato.

Os testes verificam o comportamento implementado.

---

# 30. Critérios de qualidade

A documentação de um endpoint deve permitir que um developer externo à equipa determine:

1. para que serve o endpoint;
2. quem pode utilizá-lo;
3. como autenticar;
4. que parâmetros são necessários;
5. que dados devem ser enviados;
6. que resposta será devolvida;
7. quais os códigos HTTP possíveis;
8. quais os erros possíveis;
9. quais as regras de negócio relevantes;
10. se existem efeitos secundários importantes.

Se essas informações não puderem ser determinadas, a documentação deve ser considerada incompleta.

---

# 31. Regra de actualização

Uma alteração à API deve considerar simultaneamente:

```text
Código
  +
Schema
  +
Testes
  +
Documentação
```

Uma alteração não deve ser considerada documentalmente concluída quando apenas o código foi alterado.

Quando o contrato mudar, a documentação correspondente deve ser revista na mesma alteração ou numa alteração explicitamente relacionada.

---

# 32. Princípio final

A documentação da API deve ser suficientemente detalhada para permitir a integração de um consumidor sem acesso ao código interno do backend.

Ao mesmo tempo, não deve transformar-se numa cópia extensa da implementação.

A documentação deve explicar **o contrato e o comportamento observável da API**, enquanto a arquitectura e o código explicam como esse comportamento é produzido.