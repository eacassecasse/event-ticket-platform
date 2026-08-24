# Guia de Contribuição

## 1. Objectivo deste documento

Este documento define as regras e práticas para contribuir para o desenvolvimento da plataforma.

O seu objectivo é garantir que todas as alterações introduzidas no projecto sejam:

- compreensíveis;
- tecnicamente consistentes;
- testáveis;
- documentadas quando necessário;
- rastreáveis através do histórico do Git;
- compatíveis com as regras de integração contínua;
- seguras;
- suficientemente pequenas para serem analisadas e validadas.

Estas regras aplicam-se a todas as alterações ao repositório, independentemente de serem alterações de código, documentação, configuração, testes ou infraestrutura.

O projecto encontra-se em desenvolvimento acelerado devido ao prazo de sete dias do desafio. Esta condição não elimina as regras de engenharia definidas neste documento; significa apenas que as decisões devem privilegiar uma implementação simples, correcta e verificável em vez de complexidade desnecessária.

---

# 2. Princípios de desenvolvimento

As contribuições devem seguir, por ordem de prioridade, os seguintes princípios:

1. **Correcção**
2. **Segurança**
3. **Manutenibilidade**
4. **Testabilidade**
5. **Clareza**
6. **Experiência do utilizador**
7. **Desempenho**
8. **Velocidade de implementação**

A velocidade de desenvolvimento é importante neste desafio, mas não deve ser obtida através da introdução deliberada de código difícil de compreender, comportamento não testado ou decisões que comprometam a integridade do sistema.

## 2.1 Simplicidade antes de complexidade

A arquitectura deve resolver o problema apresentado sem introduzir componentes que não tenham uma finalidade clara.

Por exemplo, não devem ser introduzidos sistemas distribuídos, filas de mensagens, serviços adicionais, bases de dados secundárias ou mecanismos de infraestrutura apenas porque são utilizados em sistemas empresariais maiores.

Uma tecnologia ou componente deve existir porque resolve um problema concreto do projecto.

---

# 3. Estrutura de branches

O repositório utiliza uma estratégia baseada numa branch principal estável e numa branch de integração.

```text
main
  │
  └── develop
        │
        ├── feature/*
        ├── fix/*
        ├── docs/*
        └── chore/*
````

## 3.1 `main`

A branch `main` representa o estado estável e potencialmente entregável da aplicação.

Não são permitidos commits directos nesta branch.

Todas as alterações devem entrar através de Pull Requests.

---

## 3.2 `develop`

A branch `develop` é utilizada para integrar alterações concluídas antes da sua promoção para `main`.

Também não são permitidos commits directos nesta branch.

As alterações devem ser introduzidas através de Pull Requests.

---

## 3.3 Branches de funcionalidade

Utilize:

```text
feature/<descricao>
```

Exemplos:

```text
feature/event-discovery
feature/event-creation
feature/ticket-reservation
feature/qr-ticket
```

Uma branch de funcionalidade deve representar uma alteração coerente e relativamente isolada.

---

## 3.4 Branches de correcção

Utilize:

```text
fix/<descricao>
```

Exemplos:

```text
fix/duplicate-ticket-validation
fix/reservation-capacity
fix/authentication-token
```

---

## 3.5 Branches de documentação

Utilize:

```text
docs/<descricao>
```

Exemplos:

```text
docs/update-readme
docs/architecture-overview
docs/api-authentication
```

---

## 3.6 Branches de manutenção

Utilize:

```text
chore/<descricao>
```

Exemplos:

```text
chore/update-dependencies
chore/configure-ci
chore/docker-development
```

---

# 4. Ciclo normal de desenvolvimento

Uma alteração deve seguir, de forma geral, este fluxo:

```text
develop
   │
   ▼
Criar branch de trabalho
   │
   ▼
Implementar alteração
   │
   ▼
Executar validações locais
   │
   ▼
Criar commits
   │
   ▼
Push para GitHub
   │
   ▼
Abrir Pull Request
   │
   ▼
CI/CD
   │
   ▼
Revisão
   │
   ▼
Merge
   │
   ▼
Eliminar branch
```

Exemplo:

```bash
git checkout develop
git pull origin develop

git checkout -b feature/event-discovery
```

Depois da implementação:

```bash
git status
git add .
pnpm cz
```

Finalmente:

```bash
git push -u origin feature/event-discovery
```

---

# 5. Commits

O projecto utiliza **Conventional Commits**.

As mensagens de commit devem permitir compreender rapidamente a natureza da alteração sem ser necessário abrir os ficheiros modificados.

A forma recomendada de criar um commit é:

```bash
pnpm cz
```

O Commitizen apresenta perguntas que ajudam a construir uma mensagem compatível com as regras do projecto.

---

## 5.1 Estrutura de um commit

O formato geral é:

```text
tipo(âmbito): descrição
```

Exemplo:

```text
feat(events): adicionar criação de eventos
```

O âmbito é opcional:

```text
docs: actualizar instruções de instalação
```

---

## 5.2 Tipos de commit

| Tipo       | Utilização                                                  |
| ---------- | ----------------------------------------------------------- |
| `feat`     | Introdução de uma nova funcionalidade                       |
| `fix`      | Correcção de um comportamento incorrecto                    |
| `docs`     | Alteração exclusivamente documental                         |
| `style`    | Formatação sem alteração de comportamento                   |
| `refactor` | Reestruturação do código sem alteração funcional pretendida |
| `perf`     | Melhoria de desempenho                                      |
| `test`     | Criação ou alteração de testes                              |
| `build`    | Alterações relacionadas com dependências ou compilação      |
| `ci`       | Alterações relacionadas com CI/CD                           |
| `chore`    | Manutenção técnica                                          |
| `revert`   | Reversão de uma alteração anterior                          |

---

## 5.3 Exemplos

Válidos:

```text
feat(events): adicionar criação de eventos
feat(auth): implementar autenticação por JWT
fix(tickets): impedir validação duplicada
test(reservations): adicionar teste de capacidade
docs(readme): actualizar instruções de execução
ci(github): adicionar verificação de segurança
chore(dependencies): actualizar dependências
refactor(tickets): separar geração e validação de códigos
```

Inválidos:

```text
updated stuff
fix
changes
final version
new code
update
```

Mensagens genéricas dificultam a compreensão do histórico e não devem ser utilizadas.

---

# 6. Commitizen e Commitlint

O projecto utiliza duas ferramentas com responsabilidades diferentes.

## Commitizen

O Commitizen ajuda o autor a criar uma mensagem de commit correcta através de uma interface interactiva:

```bash
pnpm cz
```

## Commitlint

O Commitlint verifica se a mensagem criada respeita as regras do Conventional Commits.

Esta validação é executada automaticamente através do hook `commit-msg` do Git.

A relação entre os componentes é:

```text
Commitizen
    │
    ▼
Mensagem de commit
    │
    ▼
Git commit
    │
    ▼
Husky
    │
    ▼
Commitlint
    │
    ├── válida → commit aceite
    │
    └── inválida → commit rejeitado
```

O Commitizen é, portanto, uma ferramenta de auxílio.

O Commitlint é o mecanismo de validação.

Uma mensagem criada manualmente continua a estar sujeita às mesmas regras.

---

# 7. Pull Requests

Todas as alterações destinadas a `develop` ou `main` devem ser submetidas através de Pull Request.

Não devem ser efectuados commits directamente nessas branches.

Cada Pull Request deve apresentar claramente:

* o problema que está a ser resolvido;
* a solução implementada;
* as principais alterações;
* os testes realizados;
* eventuais limitações;
* alterações de documentação;
* eventuais implicações de segurança.

O template oficial encontra-se em:

```text
.github/pull_request_template.md
```

---

# 8. Tamanho e âmbito dos Pull Requests

Uma Pull Request deve representar uma alteração coerente.

Evite misturar alterações não relacionadas.

Por exemplo, uma Pull Request para implementar reservas não deve incluir simultaneamente:

* uma alteração completa do sistema de autenticação;
* uma reformulação visual não relacionada;
* actualizações aleatórias de dependências;
* alterações de infraestrutura sem relação com a funcionalidade.

Quando alterações diferentes são tecnicamente dependentes, essa relação deve ser explicada na Pull Request.

---

# 9. Validação local antes do Pull Request

Antes de abrir uma Pull Request, o autor deve executar as verificações aplicáveis à alteração.

Dependendo do estado do projecto, estas podem incluir:

```bash
pnpm lint
pnpm test
```

e, para o backend:

```bash
uv run pytest
```

Os comandos definitivos serão documentados no README à medida que a infraestrutura de desenvolvimento for implementada.

Uma Pull Request não deve ser aberta sabendo que existem erros locais que podem ser detectados através das ferramentas disponíveis no projecto.

---

# 10. Integração Contínua

O GitHub Actions é utilizado para validar automaticamente as alterações submetidas ao repositório.

O pipeline será responsável, conforme a fase de desenvolvimento, por verificar:

* qualidade do código;
* formatação;
* lint;
* tipos;
* testes;
* build;
* dependências;
* vulnerabilidades conhecidas;
* exposição acidental de segredos;
* outras verificações de segurança aplicáveis.

Uma Pull Request não deve ser integrada enquanto as verificações obrigatórias estiverem a falhar.

---

# 11. Testes

As alterações de comportamento devem ser acompanhadas por testes adequados.

A estratégia de testes deverá incluir, conforme a funcionalidade:

```text
Testes unitários
       │
       ▼
Testes de integração
       │
       ▼
Testes End-to-End
```

## 11.1 Testes unitários

Validam unidades pequenas e isoladas do código.

Exemplos:

* regras de cálculo;
* validação de dados;
* geração de identificadores;
* regras de negócio.

## 11.2 Testes de integração

Validam a comunicação entre componentes.

Exemplos:

* API + PostgreSQL;
* autenticação + base de dados;
* reservas + controlo de capacidade;
* validação de bilhetes + persistência.

## 11.3 Testes End-to-End

Validam fluxos completos do ponto de vista do utilizador.

Exemplo:

```text
Cliente
  ↓
Consulta evento
  ↓
Reserva bilhete
  ↓
Pagamento simulado
  ↓
Recebe bilhete
  ↓
Portaria lê QR
  ↓
Bilhete validado
```

Nem todas as alterações exigem os três níveis de teste. A escolha deve ser proporcional ao risco e ao comportamento alterado.

---

# 12. Segurança

A segurança deve ser considerada durante a implementação e não apenas no final do projecto.

É proibido adicionar ao repositório:

* passwords;
* tokens;
* API keys;
* credenciais de bases de dados;
* chaves privadas;
* segredos de serviços externos.

As configurações sensíveis devem utilizar variáveis de ambiente.

Exemplo:

```text
DATABASE_URL
JWT_SECRET
TICKETMASTER_API_KEY
TMDB_API_KEY
```

Os valores reais destas variáveis nunca devem ser versionados.

Deve ser disponibilizado um ficheiro de exemplo, quando necessário:

```text
.env.example
```

sem valores secretos reais.

---

# 13. Autenticação e autorização

A aplicação possui três papéis principais:

```text
Organizador
Cliente
Portaria
```

A autenticação identifica quem está a utilizar a aplicação.

A autorização determina aquilo que esse utilizador pode fazer.

As duas responsabilidades não devem ser confundidas.

Por exemplo, estar autenticado não significa automaticamente ter autorização para criar ou editar eventos.

As verificações de autorização devem ser realizadas no backend.

O frontend pode ocultar funcionalidades que o utilizador não pode utilizar, mas essa ocultação nunca deve ser considerada uma medida de segurança suficiente.

---

# 14. Integridade das reservas

As operações relacionadas com reservas e bilhetes devem proteger a integridade dos dados.

Em particular, o sistema deve impedir:

* venda duplicada do mesmo lugar;
* ultrapassagem da capacidade disponível;
* utilização duplicada do mesmo bilhete;
* validação de um bilhete num evento diferente;
* alteração não autorizada do estado de uma reserva.

Quando uma operação depender de condições concorrentes, a solução deve ser implementada de forma a garantir consistência ao nível da base de dados e do backend.

---

# 15. Alterações de arquitectura

As alterações que afectem decisões estruturais do sistema devem ser documentadas através de um **Architecture Decision Record (ADR)**.

Os ADR encontram-se em:

```text
docs/adr/
```

Uma alteração pode justificar um ADR quando, por exemplo:

* introduz uma tecnologia estrutural;
* altera a arquitectura da aplicação;
* altera a estratégia de persistência;
* altera o modelo de autenticação;
* introduz uma dependência externa relevante;
* altera uma decisão arquitectural anterior.

O template oficial dos ADR deve ser utilizado para novas decisões.

---

# 16. Documentação

A documentação é considerada parte do produto.

Quando uma alteração modifica o comportamento que um developer, operador ou utilizador precisa de conhecer, a documentação correspondente deve ser actualizada.

Exemplos:

### Alteração da API

Actualizar:

```text
docs/api/
```

### Alteração arquitectural

Actualizar:

```text
docs/architecture/
```

### Alteração do processo de desenvolvimento

Actualizar:

```text
docs/development/
```

### Alteração funcional

Actualizar:

```text
specs/
```

ou a documentação de produto correspondente.

---

# 17. Especificações

As funcionalidades devem ser implementadas com base nas especificações existentes.

As especificações podem descrever:

* requisitos funcionais;
* regras de negócio;
* fluxos;
* critérios de aceitação;
* comportamentos esperados;
* restrições técnicas.

Quando a implementação revelar que uma especificação está incorrecta ou incompleta, a especificação deve ser actualizada de forma explícita.

Não devemos alterar silenciosamente o comportamento definido sem actualizar a documentação correspondente.

---

# 18. Utilização de Inteligência Artificial

A utilização de ferramentas de Inteligência Artificial é permitida e faz parte do processo de desenvolvimento deste desafio.

No entanto, o código produzido com assistência de IA continua sujeito às mesmas regras aplicadas ao código escrito manualmente.

O responsável pela contribuição deve conseguir:

* explicar o código submetido;
* justificar as principais decisões;
* identificar limitações;
* validar o comportamento;
* corrigir resultados incorrectos produzidos pela ferramenta.

A utilização de IA deve ser documentada no projecto.

O registo deverá indicar, pelo menos:

* ferramenta utilizada;
* finalidade;
* parte do projecto em que foi utilizada;
* tipo de assistência recebida;
* validação ou alterações realizadas pelo developer.

A documentação correspondente será mantida em:

```text
docs/development/ai-usage.md
```

---

# 19. Dependências

A introdução de uma nova dependência deve ter uma justificação técnica.

Antes de adicionar uma biblioteca, considere:

* problema que resolve;
* maturidade do projecto;
* manutenção;
* licença;
* segurança;
* tamanho e impacto;
* alternativas existentes;
* necessidade real dentro do projecto.

Evite adicionar uma biblioteca quando algumas linhas de código simples e facilmente testáveis resolverem o mesmo problema sem introduzir complexidade significativa.

As dependências devem ser actualizadas de forma controlada.

---

# 20. Alterações à base de dados

As alterações ao modelo persistente devem ser realizadas através do sistema de migrações utilizado pelo backend.

Uma alteração ao modelo da base de dados deve considerar:

1. alteração do modelo;
2. criação da migração;
3. execução da migração;
4. actualização dos dados de teste, quando necessário;
5. testes;
6. documentação, caso o comportamento público seja alterado.

As migrações devem ser versionadas no Git.

Não devem ser feitas alterações manuais à estrutura da base de dados de desenvolvimento como substituição permanente das migrações.

---

# 21. Dados de teste

O projecto deve disponibilizar dados de teste suficientes para que outra pessoa consiga executar os principais fluxos sem ter de criar manualmente todos os dados.

Os dados semeados devem incluir, pelo menos:

* um organizador;
* dois clientes;
* um utilizador de portaria;
* pelo menos um evento publicado;
* bilhetes disponíveis.

As credenciais de teste não devem ser credenciais reais.

As credenciais e instruções para os utilizadores de demonstração devem ser documentadas no README.

---

# 22. Revisão de código

Uma revisão de código deve procurar mais do que erros de sintaxe.

Quando aplicável, devem ser avaliados:

### Comportamento

A alteração faz aquilo que foi especificado?

### Segurança

É possível executar uma operação sem a autorização necessária?

### Dados

A alteração pode criar inconsistências?

### Concorrência

Duas operações simultâneas podem produzir um resultado incorrecto?

### Testes

O comportamento importante está coberto?

### Manutenção

Outro developer consegue compreender e alterar o código posteriormente?

### Experiência do utilizador

Os estados de sucesso, erro, carregamento e ausência de dados são tratados?

---

# 23. Tratamento de erros

Os erros devem ser tratados de forma explícita.

A aplicação deve evitar:

* mensagens técnicas directamente apresentadas ao utilizador;
* respostas inconsistentes da API;
* erros silenciosos;
* exposição de informações sensíveis;
* estados parcialmente concluídos sem tratamento.

As mensagens destinadas ao utilizador devem explicar o que aconteceu e, quando possível, o que pode fazer a seguir.

Os detalhes técnicos devem permanecer nos mecanismos apropriados de logging e diagnóstico.

---

# 24. Registo e observabilidade

As operações relevantes do backend devem ser suficientemente observáveis para permitir compreender problemas durante o desenvolvimento e execução da aplicação.

Quando apropriado, devem ser registados:

* identificador do pedido;
* operação executada;
* resultado;
* erro;
* contexto técnico necessário para investigação.

Não devem ser registados:

* passwords;
* tokens;
* chaves privadas;
* dados sensíveis desnecessários.

---

# 25. Pull Request de documentação

Alterações exclusivamente documentais continuam a utilizar Pull Requests e Conventional Commits.

Exemplo:

```text
docs(architecture): documentar fluxo de reservas
```

Não é necessário introduzir código apenas para justificar uma alteração documental.

---

# 26. Checklist antes de abrir uma Pull Request

Antes de submeter uma Pull Request, confirme:

* [ ] A branch foi criada a partir da branch correcta.
* [ ] A alteração possui um âmbito claramente definido.
* [ ] O código está formatado.
* [ ] O lint não apresenta erros.
* [ ] Os testes aplicáveis foram executados.
* [ ] Foram adicionados ou actualizados testes quando necessário.
* [ ] A documentação foi actualizada quando necessário.
* [ ] Não existem segredos ou credenciais no código.
* [ ] A mensagem de commit segue Conventional Commits.
* [ ] O histórico da branch não contém commits desnecessários.
* [ ] O comportamento alterado foi verificado manualmente quando aplicável.
* [ ] As limitações conhecidas estão documentadas.
* [ ] A Pull Request explica claramente o que foi alterado e porquê.

---

# 27. Processo de integração

Uma Pull Request pode ser integrada quando:

1. a alteração está concluída;
2. os testes aplicáveis passam;
3. o CI passa;
4. os requisitos de revisão são cumpridos;
5. os conflitos foram resolvidos;
6. a documentação necessária foi actualizada;
7. não existem problemas de segurança conhecidos introduzidos pela alteração.

O merge deve utilizar a estratégia definida nas regras do repositório GitHub.

Após a integração, a branch de trabalho deve ser eliminada quando já não for necessária.

---

# 28. Regra para o desafio de sete dias

O prazo reduzido exige uma gestão rigorosa da prioridade.

A ordem de implementação deve privilegiar:

```text
Fluxo funcional completo
        ↓
Correcção
        ↓
Testes essenciais
        ↓
Segurança
        ↓
Documentação
        ↓
Experiência do utilizador
        ↓
Melhorias opcionais
```

Uma funcionalidade parcialmente implementada não deve ser priorizada em detrimento de um fluxo obrigatório que ainda não funciona de ponta a ponta.

O objectivo principal é entregar uma aplicação pequena, coerente e funcional, acompanhada por decisões técnicas que possam ser explicadas e verificadas.

---

# 29. Filosofia de contribuição

Uma boa contribuição não é necessariamente a que adiciona mais código.

É a que resolve correctamente um problema, mantém o sistema compreensível e deixa informação suficiente para que outra pessoa consiga perceber:

* o que foi alterado;
* porque foi alterado;
* como funciona;
* como foi validado;
* quais são as suas limitações.

Este princípio é particularmente importante neste desafio, onde o processo de engenharia e a capacidade de justificar decisões fazem parte da avaliação.