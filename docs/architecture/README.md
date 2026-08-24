# Documentação de Arquitectura

## 1. Objectivo

A pasta `docs/architecture/` contém a documentação técnica que descreve a arquitectura da plataforma, os seus principais componentes, as relações entre eles e os princípios utilizados para organizar o sistema.

Esta documentação existe para tornar a arquitectura compreensível sem ser necessário analisar previamente o código-fonte.

O seu propósito é permitir que uma pessoa que entre no projecto consiga compreender:

- quais são os principais componentes do sistema;
- qual é a responsabilidade de cada componente;
- como os componentes comunicam entre si;
- onde são processadas as principais regras de negócio;
- como os dados circulam pelo sistema;
- quais são as fronteiras entre frontend, backend, persistência e serviços externos;
- quais são as principais restrições técnicas;
- quais os princípios que devem ser respeitados durante a implementação.

A documentação deve acompanhar a evolução real do sistema. Não deve representar uma arquitectura idealizada que não corresponde à implementação existente.

---

## 2. Âmbito

Esta área documenta aspectos estruturais e técnicos da solução, incluindo:

- arquitectura geral da plataforma;
- componentes e responsabilidades;
- fronteiras entre sistemas;
- fluxos de comunicação;
- integração com serviços externos;
- persistência de dados;
- autenticação e autorização;
- mecanismos de segurança relevantes para a arquitectura;
- comunicação entre frontend e backend;
- infraestrutura necessária para executar a aplicação;
- decisões estruturais que afectem a organização do sistema;
- diagramas arquitecturais;
- restrições e pressupostos técnicos.

Não deve ser utilizada para documentar directamente:

- código-fonte específico;
- instruções detalhadas de configuração do ambiente de desenvolvimento;
- contratos completos de endpoints;
- requisitos funcionais individuais;
- decisões arquitecturais isoladas.

Esses conteúdos pertencem a outras áreas do repositório.

---

# 3. Estrutura

A documentação arquitectural será organizada da seguinte forma:

```text
docs/
└── architecture/
    ├── README.md
    └── diagrams/
````

À medida que a arquitectura evoluir, poderão ser adicionados documentos específicos.

Exemplo:

```text
docs/
└── architecture/
    ├── README.md
    ├── system-context.md
    ├── container-architecture.md
    ├── data-architecture.md
    ├── security-architecture.md
    ├── integration-architecture.md
    └── diagrams/
        ├── system-context.md
        ├── container-diagram.md
        └── data-flow.md
```

A criação de novos documentos deve ocorrer apenas quando existir conteúdo arquitectural real que justifique a separação.

Não devem ser criados documentos vazios apenas para preencher a estrutura da pasta.

---

# 4. Relação com outras áreas de documentação

A arquitectura não deve ser documentada como uma área isolada.

Este repositório utiliza diferentes tipos de documentação, cada um com uma responsabilidade específica.

| Área                 | Responsabilidade            | Pergunta principal                                       |
| -------------------- | --------------------------- | -------------------------------------------------------- |
| `docs/architecture/` | Arquitectura do sistema     | Como o sistema está organizado?                          |
| `docs/adr/`          | Decisões arquitecturais     | Porque foi tomada determinada decisão?                   |
| `docs/api/`          | Contratos de API            | Como os sistemas comunicam com a API?                    |
| `docs/development/`  | Processo de desenvolvimento | Como trabalhamos no projecto?                            |
| `docs/product/`      | Contexto do produto         | O que estamos a construir e para quem?                   |
| `specs/functional/`  | Requisitos funcionais       | O que o sistema deve fazer?                              |
| `specs/technical/`   | Requisitos técnicos         | Que condições técnicas devem ser respeitadas?            |
| `specs/acceptance/`  | Critérios de aceitação      | Como determinamos que uma funcionalidade está concluída? |
| Código               | Implementação               | Como o sistema executa o comportamento definido?         |

Estas áreas devem complementar-se e não duplicar-se.

---

# 5. Arquitectura versus ADR

Uma distinção importante deve ser mantida entre documentação arquitectural e Architecture Decision Records.

## Arquitectura

A documentação arquitectural descreve o estado estrutural do sistema.

Por exemplo:

> O frontend comunica com o backend através de uma API HTTP. O backend é responsável pelas regras de negócio e comunica com PostgreSQL para persistência dos dados.

Isto descreve **como o sistema está organizado**.

## ADR

Um ADR documenta uma decisão específica que levou à adopção dessa arquitectura.

Por exemplo:

> Foi escolhido PostgreSQL em vez de MongoDB porque o domínio possui relações transaccionais entre eventos, reservas, lugares e bilhetes, onde consistência e integridade referencial são importantes.

Isto documenta **porque uma determinada decisão foi tomada**.

Consequentemente:

```text
Architecture documentation
        │
        │ descreve
        ▼
Estado arquitectural actual

        ▲
        │ influenciado por
        │
        ▼
ADRs
Decisões e respectivas justificações
```

Os dois tipos de documentação devem permanecer relacionados, mas não devem ser confundidos.

---

# 6. Arquitectura versus especificações

As especificações definem o comportamento ou as condições que o sistema deve cumprir.

A arquitectura define a estrutura técnica utilizada para satisfazer essas condições.

Por exemplo:

### Especificação funcional

> Um cliente deve conseguir reservar um lugar disponível para um evento.

### Especificação técnica

> O sistema deve impedir que duas reservas confirmadas adquiram simultaneamente o mesmo lugar.

### Arquitectura

> A API utiliza uma operação transaccional sobre PostgreSQL e uma restrição de unicidade para garantir a integridade da disponibilidade dos lugares.

### Código

Implementa efectivamente essa estratégia.

A relação pode ser representada assim:

```text
Requisito
    │
    ▼
Especificação
    │
    ▼
Arquitectura
    │
    ▼
Implementação
    │
    ▼
Testes
```

Nenhuma destas camadas deve ser considerada substituta das restantes.

---

# 7. Princípio de consistência entre documentação e implementação

A documentação arquitectural deve representar o sistema real.

Quando uma alteração de código modifica uma característica arquitectural relevante, a documentação correspondente deve ser avaliada.

Exemplos:

* introdução de um novo serviço;
* alteração da estratégia de persistência;
* introdução de uma nova integração externa;
* alteração significativa do mecanismo de autenticação;
* alteração da comunicação entre frontend e backend;
* introdução de processamento assíncrono;
* alteração relevante da infraestrutura;
* alteração da estratégia de deployment.

Não é necessário actualizar a documentação para cada alteração de implementação.

A regra é:

> **Se a alteração muda a forma como o sistema está estruturalmente organizado ou as fronteiras entre os seus componentes, a documentação arquitectural deve ser revista.**

---

# 8. Diagramas

Os diagramas devem ser utilizados quando uma representação visual tornar a arquitectura mais fácil de compreender.

Devem privilegiar clareza sobre quantidade.

Dependendo da necessidade, podem ser utilizados diagramas para representar:

* contexto do sistema;
* componentes;
* containers;
* fluxo de dados;
* comunicação entre serviços;
* modelo de dados;
* autenticação;
* deployment;
* integrações externas.

Os diagramas não devem existir apenas para cumprir uma expectativa documental.

Cada diagrama deve responder a uma pergunta concreta.

Por exemplo:

### Diagrama de contexto

> Com que sistemas e actores externos a plataforma interage?

### Diagrama de containers

> Quais são os principais componentes executáveis da plataforma e como comunicam?

### Diagrama de fluxo de dados

> Como os dados percorrem o sistema durante uma operação específica?

---

# 9. Convenções para diagramas

Quando possível, os diagramas devem utilizar uma notação consistente.

Os elementos devem possuir nomes que correspondam aos nomes utilizados no código e na documentação.

Por exemplo, se o componente é denominado:

```text
Backend API
```

não deve ser denominado noutro diagrama:

```text
Server
```

sem uma razão técnica para essa diferença.

Quando um diagrama representar um fluxo específico, devem ser identificados:

* origem;
* destino;
* protocolo ou mecanismo de comunicação, quando relevante;
* dados relevantes;
* condições ou decisões importantes;
* sistemas externos envolvidos.

---

# 10. Documentação de alterações arquitecturais

Uma alteração arquitectural significativa deve normalmente envolver três elementos:

```text
Alteração proposta
       │
       ├── ADR
       │
       ├── Arquitectura actualizada
       │
       └── Implementação
```

O ADR explica a decisão.

A documentação arquitectural representa o resultado.

O código implementa o resultado.

Os testes verificam o comportamento esperado.

---

# 11. Quando criar um ADR

Uma alteração deve ser considerada para um ADR quando representar uma decisão que:

* tenha impacto significativo na arquitectura;
* afecte vários componentes;
* estabeleça uma tecnologia principal;
* estabeleça um padrão estrutural;
* introduza uma restrição importante;
* tenha alternativas tecnicamente plausíveis;
* seja difícil ou dispendiosa de reverter;
* possa ser questionada no futuro;
* tenha consequências relevantes para segurança, desempenho, manutenção ou escalabilidade.

Exemplos para este projecto podem incluir:

* escolha do framework backend;
* escolha da tecnologia frontend;
* escolha do PostgreSQL;
* estratégia de autenticação;
* estratégia de geração e validação de bilhetes;
* estratégia de prevenção de venda duplicada;
* escolha do fornecedor externo de eventos;
* estratégia de deployment.

Decisões pequenas e reversíveis não necessitam necessariamente de ADR.

---

# 12. Estado actual versus estado futuro

A documentação deve distinguir claramente entre:

* arquitectura actualmente implementada;
* arquitectura planeada;
* funcionalidades ainda não implementadas.

Não devem ser descritas como existentes funcionalidades que apenas estão planeadas.

Quando uma funcionalidade ainda não estiver implementada, deve ser indicada explicitamente.

Exemplo:

```text
Estado: Planeado

A aplicação poderá futuramente utilizar processamento assíncrono
para determinadas operações. Esta capacidade ainda não faz parte
da implementação actual.
```

Isto evita que a documentação se torne enganadora.

---

# 13. Responsabilidade pela actualização

A pessoa que introduz uma alteração arquitectural é responsável por garantir que a documentação afectada foi avaliada.

Isto não significa necessariamente que toda alteração de código exija alteração documental.

A responsabilidade consiste em determinar se a alteração afecta a arquitectura documentada.

Durante uma Pull Request, o revisor deve verificar:

* se a alteração possui impacto arquitectural;
* se existe ADR quando necessário;
* se a documentação arquitectural continua correcta;
* se os diagramas afectados continuam válidos.

---

# 14. Revisão arquitectural

As alterações arquitecturais relevantes devem ser revistas através de Pull Request.

Quando uma alteração exigir uma nova decisão arquitectural, o ADR deve ser criado ou actualizado juntamente com a alteração correspondente.

Uma alteração arquitectural não deve ser considerada concluída apenas porque o código compila ou os testes passam.

Quando aplicável, a conclusão deve considerar:

1. decisão documentada;
2. arquitectura documentada;
3. implementação realizada;
4. testes relevantes;
5. documentação de API actualizada;
6. impacto de segurança avaliado;
7. impacto operacional avaliado.

---

# 15. Relação com o código-fonte

A documentação deve apontar para componentes concretos do repositório sempre que isso melhorar a compreensão.

Por exemplo:

```text
apps/api/
apps/web/
infrastructure/
```

Quando a localização de um componente estiver definida, a documentação pode referenciá-la directamente.

Evitar referências genéricas como:

> "o backend trata desta operação".

Preferir:

> "A operação é tratada pelo serviço responsável pela gestão de reservas em `apps/api/...`."

Os caminhos devem ser actualizados quando a estrutura do código for alterada.

---

# 16. Princípio de fonte de verdade

Cada informação deve possuir uma fonte de verdade claramente identificável.

Exemplo:

| Informação              | Fonte de verdade                  |
| ----------------------- | --------------------------------- |
| Requisitos funcionais   | `specs/functional/`               |
| Critérios de aceitação  | `specs/acceptance/`               |
| Decisões arquitecturais | `docs/adr/`                       |
| Arquitectura actual     | `docs/architecture/`              |
| Contratos da API        | `docs/api/` e implementação       |
| Dependências            | `package.json`, `pyproject.toml`  |
| Migrações               | sistema de migrações da aplicação |
| CI/CD                   | `.github/workflows/`              |
| Infraestrutura          | `infrastructure/`                 |

A duplicação de informação deve ser evitada.

Quando uma informação precisar de aparecer em mais do que um local, deve existir uma referência para a fonte de verdade sempre que possível.

---

# 17. Critério de qualidade

Uma documentação arquitectural é considerada adequada quando uma pessoa tecnicamente competente, mas que não participou directamente no desenvolvimento, consegue responder às seguintes perguntas sem analisar todo o código:

1. O que constitui a plataforma?
2. Quais são os seus principais componentes?
3. Qual é a responsabilidade de cada componente?
4. Como os componentes comunicam?
5. Onde são processadas as regras de negócio?
6. Onde são persistidos os dados?
7. Quais são as principais integrações externas?
8. Como são tratados autenticação e autorização?
9. Quais são as principais decisões arquitecturais?
10. Onde encontrar informação mais detalhada sobre cada área?

A documentação deve ser suficientemente técnica para suportar decisões de engenharia, mas suficientemente clara para que uma pessoa que esteja a conhecer o projecto pela primeira vez consiga compreender a arquitectura sem conhecimento prévio do sistema.

---

# 18. Regra final

A documentação arquitectural deve permanecer:

* actualizada;
* verificável;
* coerente com a implementação;
* tecnicamente precisa;
* independente de conhecimento informal;
* organizada por responsabilidade;
* suficientemente detalhada para suportar manutenção futura.

O objectivo não é produzir o maior volume possível de documentação.

O objectivo é garantir que **as decisões estruturais e o funcionamento arquitectural da plataforma podem ser compreendidos, verificados e mantidos por outras pessoas sem depender do conhecimento original do autor**.