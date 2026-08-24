# Especificações do Sistema

## 1. Objectivo

A pasta `specs/` contém as especificações formais utilizadas para transformar os requisitos do produto em comportamentos suficientemente precisos para orientar a arquitectura, a implementação e os testes da plataforma.

Uma especificação ocupa uma posição intermédia entre a necessidade do produto e o código.

A relação é:

```text
Necessidade do produto
        │
        ▼
docs/product/
        │
        ▼
specs/
        │
        ├──────────────┐
        ▼              ▼
Arquitectura       Testes
        │              │
        └──────┬───────┘
               ▼
          Implementação
````

O objectivo não é transformar toda a documentação numa descrição exaustiva do código.

O objectivo é definir, de forma verificável, **o comportamento que o sistema deve apresentar**.

---

# 2. O que é uma especificação

Uma especificação descreve um comportamento ou requisito de forma suficientemente precisa para que diferentes developers consigam chegar a implementações compatíveis.

Por exemplo:

> O Cliente pode reservar ingressos para um evento.

é um requisito funcional.

Uma especificação deverá tornar esse requisito mais preciso:

```text
Dado que um evento possui capacidade disponível,
quando um Cliente solicitar uma reserva válida,
então o sistema deve criar uma reserva associada ao Cliente
e reduzir a disponibilidade de acordo com as regras definidas.
```

A especificação deve permitir determinar:

* condição inicial;
* actor;
* acção;
* regras aplicáveis;
* resultado esperado;
* casos de erro;
* condições limite.

---

# 3. O que não pertence a `specs/`

A pasta `specs/` não deve ser utilizada como depósito genérico para qualquer documento técnico.

Os conteúdos devem ser encaminhados para a camada apropriada.

### Produto

Utilizar:

```text
docs/product/
```

quando o conteúdo responde principalmente a:

> O que o produto precisa de fazer e porquê?

---

### Arquitectura

Utilizar:

```text
docs/architecture/
```

quando o conteúdo responde principalmente a:

> Como o sistema será estruturado para satisfazer esses requisitos?

---

### Decisões arquitecturais

Utilizar:

```text
docs/adr/
```

quando o conteúdo responde principalmente a:

> Entre várias alternativas tecnicamente plausíveis, que decisão foi tomada e porquê?

---

### API

Utilizar:

```text
docs/api/
```

quando o conteúdo responde principalmente a:

> Como um consumidor externo comunica com a API?

---

### Desenvolvimento

Utilizar:

```text
docs/development/
```

quando o conteúdo responde principalmente a:

> Como os developers trabalham, executam, validam e mantêm o projecto?

---

### Especificações

Utilizar:

```text
specs/
```

quando o conteúdo responde principalmente a:

> Qual é o comportamento exacto que a implementação deve satisfazer?

---

# 4. Relação entre as camadas

As diferentes áreas não são concorrentes.

Cada uma possui uma responsabilidade diferente.

```text
┌─────────────────────────────┐
│       Product Docs          │
│                             │
│ Problema                    │
│ Objectivos                  │
│ Utilizadores                │
│ Requisitos                  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│          Specs              │
│                             │
│ Comportamento               │
│ Regras                      │
│ Estados                     │
│ Fluxos                      │
│ Critérios verificáveis      │
└──────────────┬──────────────┘
               │
               ├───────────────────┐
               ▼                   ▼
┌─────────────────────────┐ ┌──────────────────────┐
│      Architecture       │ │        Tests         │
│                         │ │                      │
│ Estrutura               │ │ Verificação          │
│ Componentes             │ │ dos comportamentos   │
│ Integrações             │ │ especificados        │
└────────────┬────────────┘ └──────────────────────┘
             │
             ▼
       Implementation
```

Uma especificação não deve definir desnecessariamente a implementação.

---

# 5. Princípio de independência da implementação

Sempre que possível, as especificações devem descrever comportamento observável em vez de detalhes específicos do código.

Por exemplo, preferir:

```text
Quando dois clientes tentarem reservar simultaneamente
o último ingresso disponível, apenas uma reserva poderá
ser confirmada.
```

em vez de:

```text
Use SELECT ... FOR UPDATE dentro de uma transacção
SQLAlchemy.
```

A primeira definição é uma regra do sistema.

A segunda é uma possível implementação.

A implementação poderá posteriormente mudar sem invalidar a regra funcional.

---

# 6. Quando uma especificação deve ser criada

Uma especificação deve ser criada quando um requisito possuir complexidade suficiente para beneficiar de uma definição explícita.

É particularmente recomendada quando existir:

* mais de um actor;
* vários estados;
* regras de negócio;
* condições de erro;
* concorrência;
* dependência entre operações;
* integração externa;
* requisitos de segurança;
* comportamento que precise de testes;
* possibilidade de interpretações diferentes.

Não é necessário criar uma especificação extensa para cada pequena alteração visual.

---

# 7. Estrutura da especificação

As especificações devem, quando aplicável, utilizar uma estrutura semelhante a:

```text
Título
Contexto
Objectivo
Actores
Pré-condições
Fluxo principal
Fluxos alternativos
Regras de negócio
Estados
Validações
Erros
Critérios de aceitação
Casos limite
Dependências
Questões em aberto
Referências
```

Nem todas as secções precisam de existir em todas as especificações.

A estrutura deve ser adaptada à natureza do comportamento documentado.

---

# 8. Identificação

As especificações devem possuir nomes claros e estáveis.

Exemplos:

```text
specs/
├── authentication/
├── event-management/
├── event-discovery/
├── reservations/
├── payments/
├── tickets/
└── ticket-validation/
```

Os nomes devem representar conceitos do domínio e não detalhes de implementação.

Evitar:

```text
specs/
├── fastapi-routes/
├── sqlalchemy-models/
└── react-components/
```

Esses conceitos pertencem à implementação ou à arquitectura.

---

# 9. Organização recomendada

A estrutura inicial será:

```text
specs/
├── README.md
├── authentication/
├── event-discovery/
├── event-management/
├── reservations/
├── payments/
├── tickets/
└── ticket-validation/
```

Esta estrutura pode evoluir à medida que o domínio for melhor compreendido.

Não devem ser criadas dezenas de pastas vazias apenas para antecipar possíveis funcionalidades.

---

# 10. Especificação de autenticação

A especificação de autenticação deve definir, entre outros aspectos:

* processo de autenticação;
* credenciais;
* sessão ou token;
* utilizadores autenticados;
* expiração;
* comportamento perante credenciais inválidas;
* comportamento perante utilizadores inexistentes;
* relação com autorização.

A especificação não deve determinar prematuramente uma biblioteca específica.

---

# 11. Especificação de autorização

A autorização deve definir as permissões associadas aos diferentes papéis.

Os papéis actualmente previstos são:

```text
Organizador
Cliente
Portaria
```

A especificação deve estabelecer:

* operações permitidas;
* operações proibidas;
* acesso a recursos próprios;
* acesso a recursos de terceiros;
* comportamento quando não existe permissão.

---

# 12. Especificação de descoberta de eventos

Esta especificação deve definir o comportamento de consulta de eventos publicados.

Deve considerar:

* eventos disponíveis;
* pesquisa;
* filtros;
* informação apresentada;
* ordenação;
* paginação;
* ausência de resultados;
* eventos indisponíveis;
* integração com a fonte externa.

A especificação deve distinguir claramente entre:

```text
Catálogo externo
```

e:

```text
Eventos publicados na plataforma
```

---

# 13. Especificação de gestão de eventos

Esta especificação deve definir o ciclo de vida de um evento.

Deve considerar:

```text
Criação
   │
   ▼
Configuração
   │
   ▼
Publicação
   │
   ▼
Disponível
   │
   ▼
Encerramento
```

Os estados definitivos devem ser definidos na especificação e não inferidos apenas a partir da implementação.

Deve também definir quem pode:

* criar;
* editar;
* publicar;
* cancelar;
* consultar;
* encerrar um evento.

---

# 14. Especificação de reservas

A reserva é uma das áreas mais críticas do sistema.

A especificação deve definir:

* quem pode reservar;
* o que pode ser reservado;
* quantidade máxima;
* disponibilidade;
* duração da reserva, se existir;
* estados da reserva;
* pagamento;
* confirmação;
* falha;
* cancelamento, se implementado;
* comportamento perante concorrência.

A regra fundamental é:

> O sistema nunca deve confirmar uma reserva que viole a disponibilidade real do evento.

---

# 15. Especificação de pagamento

A aplicação utiliza pagamento simulado.

A especificação deve definir pelo menos:

```text
Pagamento solicitado
        │
        ├── aprovado
        │
        └── recusado
```

Deve definir o impacto de cada resultado sobre:

* reserva;
* disponibilidade;
* ingresso;
* estado da compra.

Um pagamento recusado não deve resultar num ingresso utilizável.

---

# 16. Especificação de ingressos

A especificação deve definir:

* quando um ingresso é criado;
* a quem pertence;
* a que evento pertence;
* identificador;
* estado;
* representação através de QR Code;
* partilha;
* condições de validade.

A especificação também deve definir quais os dados que podem ser expostos ao utilizador e quais devem permanecer protegidos.

---

# 17. Especificação de validação

A validação deve definir o comportamento da Portaria.

O processo conceptual é:

```text
Código recebido
      │
      ▼
Identificar ingresso
      │
      ▼
Verificar autenticidade
      │
      ▼
Verificar evento
      │
      ▼
Verificar estado
      │
      ▼
Resultado
```

Os resultados devem distinguir pelo menos:

```text
Válido
Inválido
Já utilizado
Evento errado
```

Quando a validação for bem-sucedida, o sistema deve tornar o ingresso indisponível para uma segunda utilização.

---

# 18. Critérios de aceitação

Cada especificação funcional deve possuir critérios de aceitação verificáveis.

Devem preferir-se afirmações objectivamente testáveis.

Exemplo:

```text
Dado um evento com um ingresso disponível,
quando o Cliente efectuar uma reserva válida,
então o sistema deve criar uma reserva para esse Cliente.
```

Outro exemplo:

```text
Dado um ingresso já validado,
quando a Portaria tentar validá-lo novamente,
então o sistema deve rejeitar a validação e indicar que o ingresso já foi utilizado.
```

---

# 19. Casos limite

As especificações devem considerar situações que possam produzir comportamentos diferentes do fluxo normal.

Exemplos:

* evento sem disponibilidade;
* evento inexistente;
* evento não publicado;
* pagamento recusado;
* ingresso inexistente;
* ingresso inválido;
* ingresso já utilizado;
* ingresso de outro evento;
* dois clientes a reservar simultaneamente;
* fornecedor externo indisponível;
* resposta inválida do fornecedor externo;
* utilizador sem permissão.

Os casos limite devem ser tratados antes de serem descobertos acidentalmente durante a implementação.

---

# 20. Dependências

Quando uma especificação depender de outro comportamento, essa dependência deve ser explicitada.

Exemplo:

```text
Ticket validation
        │
        ├── Authentication
        ├── Authorization
        ├── Ticket lifecycle
        └── Event lifecycle
```

Isto facilita determinar o impacto de alterações.

---

# 21. Relação com testes

Os testes devem validar comportamentos definidos nas especificações.

A relação ideal é:

```text
Specification
      │
      ▼
Acceptance criteria
      │
      ▼
Test cases
      │
      ▼
Automated tests
```

Uma especificação importante que não possua qualquer forma de validação deve ser analisada.

Não significa que todos os critérios precisem necessariamente de um teste automatizado, mas deve existir uma forma definida de confirmar o comportamento.

---

# 22. Relação com a API

A especificação funcional deve definir o comportamento antes de definir necessariamente o endpoint.

Por exemplo:

```text
Specification:
"Cliente pode reservar ingressos."
```

Depois:

```text
API:
POST /api/v1/reservations
```

A API é uma forma de expor o comportamento.

Não deve ser utilizada como substituto da definição do comportamento.

---

# 23. Relação com a interface

A especificação deve definir o comportamento que o utilizador precisa de obter.

Não deve obrigatoriamente definir:

* cor;
* tipografia;
* biblioteca de componentes;
* estrutura exacta do DOM;
* nomes de componentes React.

Esses aspectos pertencem ao design e à implementação frontend.

Exemplo:

```text
Especificação:
"Portaria deve conseguir validar através da câmara
ou introduzir manualmente o código."

Implementação:
"Componente QRScanner + formulário manual."
```

A segunda decisão pode mudar sem alterar a primeira.

---

# 24. Relação com ADRs

Uma especificação pode originar uma decisão arquitectural.

Por exemplo:

```text
Specification
     │
     ▼
Requirement:
prevent duplicate ticket validation
     │
     ▼
Technical alternatives
     │
     ▼
ADR
     │
     ▼
Architecture decision
```

O ADR deve explicar a decisão técnica.

A especificação continua a explicar o comportamento que precisa de ser satisfeito.

---

# 25. Questões em aberto

Uma especificação pode conter questões que ainda não foram resolvidas.

Estas devem ser explicitamente identificadas.

Exemplo:

```markdown
## Questões em aberto

- A reserva expira automaticamente?
- O ingresso pode ser transferido?
- O Organizador pode cancelar um evento já publicado?
```

Não devem ser preenchidas através de suposições.

Quando uma questão for resolvida, a especificação deve ser actualizada.

Se a resolução envolver uma decisão arquitectural relevante, poderá também ser necessário criar um ADR.

---

# 26. Estado da especificação

As especificações podem possuir estados.

Recomenda-se:

```text
draft
review
approved
implemented
deprecated
```

### `draft`

A especificação ainda está a ser elaborada.

### `review`

A especificação está pronta para revisão.

### `approved`

O comportamento foi acordado e pode orientar a implementação.

### `implemented`

O comportamento foi implementado e validado.

### `deprecated`

A especificação deixou de representar o comportamento actual, mas é mantida para referência histórica.

---

# 27. Alterações às especificações

Uma especificação não deve ser alterada silenciosamente quando a alteração modificar um comportamento já acordado.

Quando necessário, deve ser possível determinar:

* o que mudou;
* porquê;
* quando;
* quem aprovou;
* que implementação foi afectada;
* que testes foram alterados.

Para alterações arquitecturais significativas, deve ser considerada a criação ou actualização de um ADR.

---

# 28. Rastreabilidade

Quando aplicável, uma especificação deve permitir rastrear a relação entre:

```text
Requisito
   │
   ▼
Especificação
   │
   ├── ADR
   │
   ├── API
   │
   ├── UI
   │
   └── Testes
```

Esta rastreabilidade não deve transformar o projecto numa burocracia documental.

Deve existir principalmente para requisitos importantes ou de risco elevado.

---

# 29. Qualidade das especificações

Uma boa especificação deve ser:

### Clara

Duas pessoas devem conseguir interpretar o comportamento de forma semelhante.

### Verificável

Deve ser possível determinar se o comportamento foi implementado correctamente.

### Completa

Os cenários relevantes não devem depender de suposições escondidas.

### Independente da implementação

Não deve restringir a implementação sem necessidade.

### Consistente

Não deve contradizer outras especificações ou requisitos aprovados.

### Rastreável

Quando necessário, deve ser possível relacioná-la com requisitos, decisões e testes.

---

# 30. O que uma especificação não deve fazer

Uma especificação não deve:

* descrever cada linha de código;
* reproduzir classes;
* reproduzir ficheiros;
* definir nomes internos sem necessidade;
* prescrever uma biblioteca quando o comportamento não depende dela;
* documentar configurações de ambiente;
* substituir testes;
* substituir ADRs;
* substituir a documentação da API.

---

# 31. Estrutura inicial do directório

A estrutura inicial será:

```text
specs/
├── README.md
├── authentication/
├── event-discovery/
├── event-management/
├── reservations/
├── payments/
├── tickets/
└── ticket-validation/
```

As pastas serão preenchidas à medida que cada domínio for especificado.

Não devem ser criadas especificações fictícias apenas para preencher a estrutura.

---

# 32. Ordem de elaboração

A ordem recomendada para este projecto é:

```text
1. Authentication & Authorization
             │
             ▼
2. Event Discovery
             │
             ▼
3. Event Management
             │
             ▼
4. Reservations
             │
             ▼
5. Payments
             │
             ▼
6. Tickets
             │
             ▼
7. Ticket Validation
```

Esta ordem reduz dependências circulares e permite construir o fluxo principal progressivamente.

---

# 33. Princípio de desenvolvimento

A especificação deve ser suficientemente detalhada para reduzir ambiguidade, mas suficientemente flexível para permitir decisões técnicas durante a implementação.

O objectivo é evitar os dois extremos:

```text
Pouca especificação
       │
       ▼
Ambiguidade
       │
       ▼
Implementações incompatíveis
```

e:

```text
Especificação excessivamente prescritiva
       │
       ▼
Implementação artificialmente limitada
```

O equilíbrio correcto é:

```text
Comportamento preciso
        +
Regras explícitas
        +
Implementação suficientemente livre
```

---

# 34. Fonte de verdade

Para questões relacionadas com o comportamento do produto, deve ser considerada a seguinte hierarquia:

```text
Requisitos aprovados
        │
        ▼
Especificações aprovadas
        │
        ▼
Implementação
        │
        ▼
Testes
```

Quando for detectada uma inconsistência, ela deve ser analisada em vez de simplesmente alterar a documentação ou o código para eliminar a diferença.

A decisão sobre qual comportamento deve prevalecer deve ser explícita.

---

# 35. Princípio final

As especificações existem para tornar o comportamento esperado suficientemente claro antes de este ser transformado em código.

Uma especificação bem escrita deve permitir que um developer:

1. compreenda o comportamento;
2. compreenda as regras;
3. identifique os casos normais;
4. identifique os casos de erro;
5. saiba o que precisa de ser validado;
6. escolha uma implementação adequada;
7. saiba quando a implementação está concluída.

A especificação não substitui a engenharia.

Ela cria uma referência comum para que produto, arquitectura, desenvolvimento e testes estejam a resolver o mesmo problema.