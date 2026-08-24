# Guia de Desenvolvimento

## 1. Objectivo

A pasta `docs/development/` contém a documentação necessária para compreender e executar o processo técnico de desenvolvimento da plataforma.

Esta documentação complementa o `CONTRIBUTING.md`.

Enquanto o `CONTRIBUTING.md` define as regras gerais para contribuir para o projecto, esta área documenta o funcionamento técnico do ambiente de desenvolvimento, incluindo:

- preparação do ambiente local;
- estrutura do repositório;
- utilização das branches;
- execução da aplicação;
- execução de testes;
- validações automáticas;
- processo de criação de Pull Requests;
- convenções de desenvolvimento;
- ferramentas utilizadas pelo projecto;
- procedimentos de diagnóstico.

O objectivo é permitir que um developer consiga preparar o ambiente e começar a trabalhar no projecto sem depender de instruções transmitidas informalmente.

---

# 2. Princípios de desenvolvimento

O desenvolvimento da plataforma deve seguir os seguintes princípios:

### 2.1. Código executável antes de optimizações

Durante o desenvolvimento, deve ser dada prioridade à implementação de fluxos completos e verificáveis antes da introdução de optimizações ou funcionalidades secundárias.

Uma funcionalidade parcialmente sofisticada não deve substituir uma implementação simples que consiga completar correctamente o fluxo necessário.

### 2.2. Alterações pequenas e verificáveis

Cada alteração deve possuir um âmbito claro.

Uma Pull Request deve evitar combinar alterações não relacionadas, como:

```text
feature + refactorização extensa + alteração de infraestrutura
````

sem uma razão técnica clara.

Alterações menores são mais fáceis de:

* rever;
* testar;
* diagnosticar;
* reverter;
* associar a uma decisão ou requisito.

### 2.3. Validação antes da integração

Uma alteração não deve ser integrada simplesmente porque funciona no ambiente local do developer.

Sempre que aplicável, deve passar pelos mecanismos de validação definidos pelo projecto:

* lint;
* testes;
* type checking;
* validações de segurança;
* validações de build;
* outras verificações configuradas no CI.

---

# 3. Estrutura de branches

O projecto utiliza uma estratégia baseada em integração através da branch `develop`.

A estrutura conceptual é:

```text
main
  │
  └── develop
        │
        ├── feature/...
        ├── fix/...
        ├── refactor/...
        └── chore/...
```

## 3.1. `main`

A branch `main` representa o estado estável do projecto.

Não deve ser utilizada para desenvolvimento directo.

Alterações devem chegar à `main` através de Pull Requests provenientes da branch de integração.

---

## 3.2. `develop`

A branch `develop` representa o estado de integração do desenvolvimento.

É a branch utilizada para combinar alterações provenientes das diferentes áreas do projecto antes da sua promoção para `main`.

A `develop` também deve ser protegida.

Isto é importante porque a existência de uma branch de integração não significa que qualquer alteração possa ser introduzida directamente.

---

## 3.3. Branches de trabalho

Cada alteração deve ser desenvolvida numa branch própria.

Exemplos:

```text
feature/event-discovery
feature/event-management
feature/ticket-purchase
feature/ticket-validation

fix/duplicate-ticket-validation

refactor/reservation-service

chore/configure-ci
```

A branch deve possuir um nome curto, descritivo e relacionado com o trabalho realizado.

---

# 4. Fluxo de desenvolvimento

O fluxo normal é:

```text
1. Identificar requisito ou problema
            │
            ▼
2. Criar branch de trabalho
            │
            ▼
3. Implementar alteração
            │
            ▼
4. Executar validações locais
            │
            ▼
5. Criar commits
            │
            ▼
6. Push da branch
            │
            ▼
7. Abrir Pull Request
            │
            ▼
8. CI executa validações
            │
            ▼
9. Code review
            │
            ▼
10. Merge para develop
            │
            ▼
11. Validação de integração
            │
            ▼
12. Promoção para main
```

Nem todas as alterações exigem exactamente o mesmo conjunto de validações, mas nenhuma alteração deve ignorar os mecanismos de qualidade aplicáveis ao seu âmbito.

---

# 5. Criação de uma branch

As branches devem ser criadas a partir da branch de integração actualizada.

Antes de começar:

```bash
git switch develop
git pull --ff-only origin develop
```

Depois:

```bash
git switch -c feature/event-discovery
```

A branch deve ser publicada no repositório remoto:

```bash
git push -u origin feature/event-discovery
```

---

# 6. Commits

O projecto utiliza **Conventional Commits**.

As mensagens devem seguir a estrutura:

```text
<type>(<scope>): <description>
```

Exemplos:

```text
feat(events): add published event listing
fix(tickets): prevent duplicate validation
test(reservations): add concurrent booking coverage
docs(api): document ticket validation endpoint
chore(ci): add backend test workflow
refactor(auth): separate role authorization logic
```

A lista completa de tipos e regras encontra-se definida na configuração de Commitlint do repositório.

---

# 7. Commitizen

O projecto utiliza Commitizen para facilitar a criação de commits compatíveis com Conventional Commits.

Sempre que possível, os commits devem ser criados através de:

```bash
pnpm cz
```

O Commitizen reduz erros de formatação, mas não substitui a validação feita pelo Commitlint.

A responsabilidade pela qualidade semântica da mensagem continua a ser do developer.

---

# 8. Validação local

Antes de abrir uma Pull Request, o developer deve executar as validações relevantes.

Exemplos:

```bash
pnpm lint
pnpm test
```

Quando aplicável:

```bash
pnpm typecheck
pnpm build
```

Os comandos exactos disponíveis no projecto devem ser definidos nos respectivos `package.json`, `pyproject.toml` ou outros ficheiros de configuração.

Não devem ser documentados comandos que não existam efectivamente no repositório.

---

# 9. Pull Requests

Uma Pull Request deve:

* possuir um título claro;
* explicar o problema resolvido;
* descrever as alterações realizadas;
* indicar como a alteração foi validada;
* identificar limitações conhecidas;
* indicar alterações de documentação necessárias;
* indicar alterações de base de dados, quando aplicável;
* considerar impactos de segurança.

O template oficial encontra-se em:

```text
.github/pull_request_template.md
```

---

# 10. Relação entre Pull Requests e Issues

Quando uma alteração estiver associada a uma Issue, a Pull Request deve referenciá-la.

Por exemplo:

```text
Closes #42
```

Isto permite ao GitHub associar a implementação ao problema ou requisito correspondente e fechar automaticamente a Issue quando a Pull Request for integrada, quando a sintaxe utilizada possuir esse comportamento.

---

# 11. Revisão de código

A revisão deve verificar mais do que a compilação do código.

Dependendo da alteração, a revisão deve considerar:

* correcção funcional;
* clareza;
* estrutura;
* segurança;
* tratamento de erros;
* consistência com a arquitectura;
* cobertura de testes;
* impacto sobre dados existentes;
* impacto sobre integrações externas;
* observabilidade;
* documentação;
* compatibilidade com os requisitos.

Uma alteração não deve ser aprovada apenas porque os testes automatizados passam.

Os testes demonstram que determinados comportamentos foram verificados; não demonstram que todos os aspectos da alteração estão correctos.

---

# 12. Alterações arquitecturais

Quando uma alteração introduzir uma decisão arquitectural relevante, deve ser avaliada a necessidade de criar ou actualizar um Architecture Decision Record.

Os ADRs encontram-se em:

```text
docs/adr/
```

Uma decisão deve normalmente ser documentada quando:

* possui impacto significativo na estrutura do sistema;
* estabelece uma tecnologia principal;
* define um padrão reutilizado por vários componentes;
* introduz uma restrição relevante;
* possui alternativas tecnicamente plausíveis;
* possui consequências difíceis de reverter;
* poderá ser questionada no futuro.

---

# 13. Alterações à base de dados

Alterações ao modelo de dados devem ser acompanhadas pelas respectivas migrações.

Uma alteração ao código que dependa de uma alteração estrutural da base de dados não deve ser considerada completa se a migração necessária não estiver incluída.

Antes da integração, devem ser considerados:

* criação da migração;
* execução da migração;
* compatibilidade com dados existentes;
* actualização de dados de teste;
* rollback, quando aplicável;
* impacto sobre ambientes existentes.

---

# 14. Variáveis de ambiente

Credenciais e configurações específicas de cada ambiente não devem ser armazenadas no Git.

É permitido versionar:

```text
.env.example
```

Não é permitido versionar ficheiros contendo valores reais, como:

```text
.env
.env.local
.env.production
```

Os valores necessários devem ser fornecidos através de variáveis de ambiente ou mecanismos apropriados de gestão de secrets.

---

# 15. Dependências

As dependências devem ser adicionadas apenas quando existir uma necessidade técnica clara.

Antes de adicionar uma dependência, deve ser considerada:

* finalidade;
* maturidade;
* manutenção;
* licença;
* segurança;
* tamanho;
* impacto no desempenho;
* existência de alternativas;
* necessidade real da dependência.

Não deve ser adicionada uma biblioteca simplesmente porque oferece uma funcionalidade conveniente que pode ser implementada de forma simples sem introduzir dependência adicional.

---

# 16. Código gerado por ferramentas de IA

A utilização de ferramentas de Inteligência Artificial é permitida e faz parte do processo de desenvolvimento deste desafio.

Contudo, código gerado por IA continua a ser responsabilidade do developer.

Antes de integrar código produzido ou assistido por IA, o developer deve:

1. compreender o código;
2. verificar as suas premissas;
3. validar o comportamento;
4. verificar segurança;
5. executar os testes relevantes;
6. adaptar o resultado às convenções do projecto;
7. remover código desnecessário ou genérico.

O projecto mantém uma documentação específica sobre a utilização de IA e as decisões tomadas durante o desenvolvimento.

---

# 17. Testes

Os testes devem existir nos pontos onde fornecem valor real para a estabilidade da aplicação.

Prioridade inicial:

1. regras de negócio;
2. autenticação e autorização;
3. reservas;
4. prevenção de venda duplicada;
5. pagamento simulado;
6. geração e validação de bilhetes;
7. utilização única de bilhetes;
8. integrações críticas.

Os testes não devem ser escritos apenas para aumentar uma percentagem de cobertura.

O objectivo é detectar regressões e verificar comportamentos importantes.

---

# 18. Integrações externas

As integrações com serviços externos devem ser isoladas de forma a evitar que a lógica de negócio dependa directamente da implementação de um fornecedor.

Por exemplo:

```text
Application
     │
     ▼
Integration interface
     │
     ▼
External provider
```

Isto permite que a aplicação mantenha uma separação clara entre:

* regras internas;
* comunicação externa;
* tratamento de respostas;
* tratamento de erros;
* configuração de credenciais.

---

# 19. Tratamento de erros

Os erros devem ser tratados de forma explícita.

A aplicação deve evitar:

* expor stack traces ao utilizador;
* devolver informação interna desnecessária;
* ignorar erros silenciosamente;
* depender de mensagens de erro de fornecedores externos como contrato interno.

As respostas da API devem utilizar uma estrutura consistente.

Os detalhes específicos do contrato HTTP devem ser documentados em:

```text
docs/api/
```

---

# 20. Observabilidade

Sempre que tecnicamente aplicável, os componentes devem produzir informação suficiente para diagnosticar problemas.

A observabilidade pode incluir:

* logs estruturados;
* identificação de requests;
* registo de erros;
* métricas;
* informação sobre integrações externas.

Não devem ser registados:

* passwords;
* tokens;
* API keys;
* dados financeiros sensíveis;
* informação pessoal desnecessária.

---

# 21. Desenvolvimento local

O ambiente local deve aproximar-se do ambiente de execução da aplicação tanto quanto razoavelmente possível.

Quando Docker Compose estiver configurado, deverá ser utilizado para fornecer os serviços de infraestrutura necessários ao desenvolvimento.

A configuração deverá permitir que um developer novo consiga:

1. obter o repositório;
2. instalar dependências;
3. configurar variáveis de ambiente;
4. iniciar os serviços necessários;
5. preparar a base de dados;
6. executar a aplicação;
7. executar os testes.

Os procedimentos concretos devem ser documentados no `README.md` principal e, quando possuírem detalhe técnico adicional, nesta área.

---

# 22. Dados de desenvolvimento

O projecto deve fornecer dados de teste suficientes para permitir a avaliação dos fluxos principais sem configuração manual extensa.

Para o desafio, devem existir pelo menos:

* um utilizador Organizador;
* dois utilizadores Cliente;
* um utilizador de Portaria;
* pelo menos um evento publicado;
* ingressos disponíveis para o evento.

As credenciais de desenvolvimento devem ser claramente identificadas como credenciais de teste e nunca reutilizadas em ambientes reais.

---

# 23. Definition of Done

Uma alteração pode ser considerada pronta para integração quando:

* o comportamento esperado está implementado;
* os requisitos aplicáveis estão satisfeitos;
* os testes relevantes passam;
* o lint e outras validações aplicáveis passam;
* não existem secrets no código;
* a documentação necessária foi actualizada;
* as migrações necessárias foram incluídas;
* a Pull Request foi preenchida correctamente;
* as limitações conhecidas estão documentadas;
* as decisões arquitecturais relevantes foram registadas.

Esta lista complementa, mas não substitui, os critérios de aceitação específicos de cada funcionalidade.

---

# 24. Diagnóstico de problemas

Quando uma validação falhar, o developer deve procurar identificar a origem antes de aplicar alterações aleatórias à configuração.

Uma sequência recomendada é:

```text
1. Identificar o comando que falhou
2. Ler a mensagem de erro completa
3. Determinar o componente responsável
4. Reproduzir localmente
5. Verificar alterações recentes
6. Corrigir a causa
7. Executar novamente a validação
8. Confirmar que a correcção não introduziu regressões
```

Não devem ser utilizados mecanismos para simplesmente ignorar uma validação sem compreender a razão da falha.

---

# 25. Fonte de verdade

Quando existirem instruções contraditórias, deve ser considerada a seguinte ordem de referência:

1. requisitos do desafio;
2. especificações versionadas;
3. ADRs aceites;
4. documentação arquitectural;
5. documentação de desenvolvimento;
6. implementação actual.

Quando existir uma contradição entre documentação e implementação, a situação deve ser analisada e corrigida. Não deve ser assumido automaticamente que a implementação é a fonte correcta.

---

# 26. Evolução deste documento

Este documento deve evoluir juntamente com o processo técnico do projecto.

Novos procedimentos só devem ser adicionados quando:

* forem efectivamente utilizados;
* resolverem um problema concreto;
* forem relevantes para futuros developers;
* ou forem necessários para manter consistência no processo.

A documentação não deve antecipar ferramentas ou processos que ainda não existem apenas para preencher uma estrutura prevista.

O princípio é:

> Documentar o processo que o projecto realmente utiliza e actualizar a documentação quando esse processo mudar.
