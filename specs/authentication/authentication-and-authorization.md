# Especificação de Autenticação e Autorização

**Estado:** `approved`  
**Versão:** `1.0`  
**Última actualização:** `2026-08-22`

---

## 1. Objectivo

Esta especificação define o comportamento de autenticação e autorização da Plataforma de Eventos e Ingressos.

O sistema possui três tipos de utilizadores com responsabilidades distintas:

- **Organizador** — cria e gere eventos;
- **Cliente** — consulta eventos, reserva ingressos, realiza o pagamento simulado e consulta os seus ingressos;
- **Portaria** — valida ingressos no momento da entrada no evento.

A autenticação determina **quem é o utilizador**.

A autorização determina **o que esse utilizador pode fazer**.

Estas duas responsabilidades devem ser tratadas separadamente.

---

# 2. Âmbito

Esta especificação cobre:

- autenticação de utilizadores;
- identificação do utilizador autenticado;
- atribuição de papéis;
- autorização baseada em papéis;
- acesso a recursos protegidos;
- rejeição de credenciais inválidas;
- rejeição de operações não autorizadas;
- comportamento perante utilizadores não autenticados.

Esta especificação não cobre:

- recuperação de palavra-passe;
- alteração de palavra-passe;
- verificação de endereço de correio electrónico;
- autenticação multifactor;
- login através de terceiros;
- registo público de utilizadores.

Essas funcionalidades não fazem parte do âmbito mínimo definido para este desafio.

---

# 3. Actores

## 3.1 Organizador

O Organizador é responsável pela criação e gestão dos eventos disponibilizados na plataforma.

Deve conseguir, dentro do âmbito do desafio:

- autenticar-se;
- criar eventos;
- consultar os seus eventos;
- editar os seus eventos;
- publicar eventos;
- gerir a disponibilidade dos seus eventos dentro das regras definidas pelo sistema.

O Organizador não deve conseguir executar operações exclusivas do Cliente ou da Portaria.

---

## 3.2 Cliente

O Cliente representa o utilizador final que pretende adquirir ingressos.

Deve conseguir:

- autenticar-se;
- consultar eventos publicados;
- pesquisar eventos, quando a funcionalidade estiver disponível;
- efectuar reservas;
- efectuar o pagamento simulado;
- consultar os seus ingressos;
- consultar os detalhes dos seus ingressos;
- utilizar o mecanismo de partilha disponibilizado pela aplicação.

O Cliente não deve conseguir:

- criar eventos;
- gerir eventos de outros utilizadores;
- validar ingressos na portaria.

---

## 3.3 Portaria

A Portaria representa o utilizador responsável pela validação dos ingressos no acesso ao evento.

Deve conseguir:

- autenticar-se;
- aceder à funcionalidade de validação;
- introduzir manualmente um código de ingresso;
- utilizar a leitura do QR Code, quando disponível;
- validar o ingresso;
- receber o resultado da validação.

A Portaria não deve conseguir:

- criar eventos;
- alterar eventos;
- comprar ingressos;
- alterar dados de reservas;
- gerar ingressos.

---

# 4. Modelo de identidade

Cada utilizador deve possuir uma identidade única no sistema.

A identidade deve permitir associar operações realizadas a um utilizador concreto.

No mínimo, o sistema deve manter:

- identificador único;
- nome;
- endereço de correio electrónico ou outro identificador de autenticação;
- credencial protegida;
- papel;
- estado da conta.

A implementação concreta destes campos pode variar, desde que preserve o comportamento definido nesta especificação.

---

# 5. Papéis

O sistema deve reconhecer os seguintes papéis:

```text
ORGANIZER
CUSTOMER
GATEKEEPER
````

Os nomes utilizados internamente na implementação podem ser diferentes, mas deve existir uma correspondência inequívoca entre o papel persistido e o comportamento definido nesta especificação.

Um utilizador deve possuir um papel claramente identificável.

Para o âmbito deste desafio, não é necessário implementar múltiplos papéis simultaneamente para o mesmo utilizador.

---

# 6. Autenticação

## 6.1 Processo

O utilizador fornece as suas credenciais através do mecanismo de autenticação disponibilizado pela aplicação.

O sistema deve:

1. receber as credenciais;
2. localizar a identidade correspondente;
3. verificar a credencial;
4. verificar se a conta pode autenticar-se;
5. estabelecer o contexto autenticado;
6. disponibilizar as informações necessárias para as operações autorizadas.

Quando qualquer uma destas verificações falhar, a autenticação deve ser rejeitada.

---

# 7. Credenciais inválidas

Quando as credenciais fornecidas não forem válidas, o sistema deve rejeitar a autenticação.

O sistema não deve revelar informação desnecessária que permita determinar se:

* o utilizador existe;
* o endereço de correio electrónico existe;
* a palavra-passe estava correcta;
* a conta possui determinado estado interno.

A resposta deve ser suficientemente clara para o utilizador compreender que a autenticação falhou, sem expor informação sensível.

---

# 8. Utilizador não autenticado

Uma operação protegida só pode ser executada quando existir um contexto de autenticação válido.

Quando um utilizador não autenticado tentar aceder a um recurso protegido, a operação deve ser rejeitada.

Exemplo:

```text
Cliente não autenticado
        │
        ▼
GET /events/{id}/tickets
        │
        ▼
Acesso protegido
        │
        ▼
Autenticação ausente
        │
        ▼
Operação rejeitada
```

A aplicação não deve tratar um utilizador não autenticado como pertencendo automaticamente a qualquer papel.

---

# 9. Autorização baseada em papéis

A autorização deve ser aplicada depois da autenticação.

O fluxo conceptual é:

```text
Request
   │
   ▼
Authentication
   │
   ├── Falha ──► Rejeitar
   │
   ▼
Identidade
   │
   ▼
Role
   │
   ▼
Authorization
   │
   ├── Não autorizado ──► Rejeitar
   │
   ▼
Operação permitida
```

A existência de uma identidade autenticada não significa que essa identidade tenha autorização para executar qualquer operação.

---

# 10. Matriz de autorização

A matriz mínima de permissões é:

| Operação                        | Organizador | Cliente | Portaria |
| ------------------------------- | :---------: | :-----: | :------: |
| Autenticar                      |      ✓      |    ✓    |     ✓    |
| Consultar eventos publicados    |      ✓      |    ✓    |    ✓*    |
| Criar evento                    |      ✓      |    ✗    |     ✗    |
| Gerir evento próprio            |      ✓      |    ✗    |     ✗    |
| Reservar ingresso               |      ✗      |    ✓    |     ✗    |
| Realizar pagamento simulado     |      ✗      |    ✓    |     ✗    |
| Consultar os próprios ingressos |      ✗      |    ✓    |     ✗    |
| Partilhar ingresso              |      ✗      |    ✓    |     ✗    |
| Validar ingresso                |      ✗      |    ✗    |     ✓    |

`*` O acesso da Portaria à consulta de eventos deve ser limitado ao necessário para executar a validação. A interface não precisa de disponibilizar a mesma experiência de consulta de eventos oferecida ao Cliente.

---

# 11. Isolamento dos recursos do Organizador

Um Organizador pode gerir os seus próprios eventos.

Não deve conseguir modificar eventos pertencentes a outro Organizador.

Por exemplo:

```text
Organizador A
     │
     ├── Evento A1 ✓
     └── Evento A2 ✓

Organizador B
     │
     └── Evento B1 ✗
```

A autorização deve verificar não apenas o papel do utilizador, mas também a propriedade do recurso quando essa propriedade for relevante.

---

# 12. Isolamento dos recursos do Cliente

Um Cliente deve conseguir consultar os seus próprios ingressos e reservas.

Não deve conseguir consultar ou modificar os ingressos privados de outro Cliente através de uma simples alteração de identificador.

Por exemplo:

```text
Cliente A
    │
    └── Ticket A ✓

Cliente A
    │
    └── Ticket B ✗
```

A verificação de autorização deve ocorrer no servidor.

Não é suficiente esconder recursos na interface frontend.

---

# 13. Operações da Portaria

A Portaria possui um papel especializado.

A sua principal responsabilidade é validar ingressos.

A interface da Portaria deve expor apenas as operações necessárias para esta actividade.

Uma Portaria autenticada não deve obter automaticamente permissões para:

* gerir eventos;
* efectuar compras;
* consultar dados privados de Clientes;
* alterar reservas.

---

# 14. Protecção no servidor

Todas as decisões de autorização devem ser aplicadas no backend.

O frontend pode esconder funcionalidades que o utilizador não pode executar, mas isso serve apenas para melhorar a experiência de utilização.

Não constitui um mecanismo de segurança.

A regra fundamental é:

> Se uma operação não é permitida pelo papel do utilizador, o backend deve rejeitá-la mesmo que o utilizador consiga construir manualmente o pedido HTTP.

---

# 15. Recursos públicos

Nem todos os recursos necessitam de autenticação.

A consulta de eventos publicados pode ser disponibilizada publicamente, de acordo com a decisão final de produto.

Por exemplo:

```text
GET /events
GET /events/{event_id}
```

podem ser públicos.

Operações que modificam dados ou expõem informação privada devem permanecer protegidas.

---

# 16. Dados privados

Os seguintes dados devem ser considerados privados:

* credenciais;
* informação interna da conta;
* reservas associadas a um Cliente;
* ingressos privados de um Cliente;
* informação interna de pagamento;
* informação necessária apenas para operações administrativas.

A API não deve devolver dados privados simplesmente porque o utilizador conhece o identificador do recurso.

---

# 17. Palavra-passe

As palavras-passe nunca devem ser armazenadas em texto simples.

O sistema deve utilizar uma função de derivação de credenciais apropriada para armazenamento seguro.

O valor armazenado na base de dados deve permitir verificar uma palavra-passe sem armazenar a palavra-passe original.

A escolha concreta do algoritmo pertence à implementação técnica.

---

# 18. Sessão de autenticação

A implementação deve manter uma forma segura de representar o estado de autenticação.

A solução poderá utilizar, por exemplo:

* tokens;
* sessões;
* cookies de sessão.

A escolha deve ser definida pela arquitectura da aplicação.

Independentemente da tecnologia escolhida:

* o contexto autenticado deve ser verificável;
* a identidade deve poder ser determinada pelo backend;
* credenciais ou tokens inválidos devem ser rejeitados;
* informação sensível não deve ser exposta ao cliente sem necessidade.

---

# 19. Expiração

O mecanismo de autenticação deve possuir uma política de validade.

Uma credencial de autenticação expirada não deve ser aceite como válida indefinidamente.

Os detalhes de:

* duração;
* renovação;
* revogação;

serão definidos na especificação técnica de autenticação ou na implementação, desde que não contradigam os requisitos de segurança do sistema.

---

# 20. Conta inválida ou desactivada

Se uma conta deixar de estar autorizada a utilizar o sistema, a autenticação deve ser impedida ou o contexto de autenticação existente deve deixar de permitir operações protegidas, de acordo com o mecanismo escolhido.

O estado da conta deve, portanto, ser considerado durante a autorização quando aplicável.

---

# 21. Tentativa de acesso não autorizado

Quando um utilizador autenticado tentar executar uma operação para a qual não possui autorização, a operação deve ser rejeitada.

Exemplo:

```text
Cliente autenticado
        │
        ▼
POST /events
        │
        ▼
Role = CUSTOMER
        │
        ▼
CUSTOMER não possui permissão
        │
        ▼
Operação rejeitada
```

A resposta deve distinguir, quando tecnicamente apropriado, entre:

* ausência de autenticação;
* autenticação válida mas sem autorização.

A implementação deve evitar revelar detalhes internos desnecessários.

---

# 22. Segurança contra alteração de identificadores

O backend não deve confiar na simples correspondência entre um identificador fornecido pelo cliente e a propriedade do recurso.

Exemplo de tentativa inválida:

```text
Cliente A
     │
     ▼
GET /tickets/ticket-b
```

Mesmo que `ticket-b` exista, o sistema deve verificar se o Cliente A possui autorização para consultar esse ingresso.

---

# 23. Seed de utilizadores

O ambiente de desenvolvimento e avaliação deve disponibilizar os utilizadores exigidos pelo desafio:

```text
1 Organizador
2 Clientes
1 Portaria
```

As credenciais de demonstração devem ser documentadas no README do projecto.

As credenciais utilizadas exclusivamente para desenvolvimento devem ser claramente identificadas como credenciais de teste.

Não devem ser utilizadas credenciais reais.

---

# 24. Requisitos mínimos de segurança

A implementação deve cumprir pelo menos:

* palavras-passe não armazenadas em texto simples;
* autenticação validada no backend;
* autorização validada no backend;
* isolamento entre utilizadores;
* protecção de operações administrativas;
* protecção de dados privados;
* rejeição de credenciais inválidas;
* rejeição de operações não autorizadas;
* validação de entrada fornecida pelo cliente.

---

# 25. Casos de erro

A implementação deve considerar pelo menos os seguintes cenários:

| Cenário                                               | Resultado esperado        |
| ----------------------------------------------------- | ------------------------- |
| Credenciais correctas                                 | Autenticação bem-sucedida |
| Credenciais incorrectas                               | Autenticação rejeitada    |
| Utilizador inexistente                                | Autenticação rejeitada    |
| Utilizador não autenticado acede a recurso protegido  | Acesso rejeitado          |
| Cliente tenta criar evento                            | Acesso rejeitado          |
| Portaria tenta efectuar compra                        | Acesso rejeitado          |
| Cliente tenta consultar ingresso de outro Cliente     | Acesso rejeitado          |
| Organizador tenta alterar evento de outro Organizador | Acesso rejeitado          |
| Credencial expirada                                   | Acesso rejeitado          |
| Conta desactivada                                     | Acesso rejeitado          |

---

# 26. Critérios de aceitação

## AC-01 — Autenticação do Organizador

**Dado** um Organizador com credenciais válidas,

**quando** efectuar a autenticação,

**então** o sistema deve estabelecer um contexto autenticado associado ao papel `ORGANIZER`.

---

## AC-02 — Autenticação do Cliente

**Dado** um Cliente com credenciais válidas,

**quando** efectuar a autenticação,

**então** o sistema deve estabelecer um contexto autenticado associado ao papel `CUSTOMER`.

---

## AC-03 — Autenticação da Portaria

**Dado** um utilizador de Portaria com credenciais válidas,

**quando** efectuar a autenticação,

**então** o sistema deve estabelecer um contexto autenticado associado ao papel `GATEKEEPER`.

---

## AC-04 — Credenciais inválidas

**Dado** um conjunto de credenciais inválidas,

**quando** o utilizador tentar autenticar-se,

**então** o sistema deve rejeitar a autenticação.

---

## AC-05 — Operação não autorizada

**Dado** um Cliente autenticado,

**quando** tentar criar um evento,

**então** o sistema deve rejeitar a operação.

---

## AC-06 — Isolamento de eventos

**Dado** um Organizador A e um evento pertencente ao Organizador B,

**quando** o Organizador A tentar alterar esse evento,

**então** o sistema deve rejeitar a operação.

---

## AC-07 — Isolamento de ingressos

**Dado** um ingresso pertencente ao Cliente A,

**quando** o Cliente B tentar consultar esse ingresso,

**então** o sistema deve rejeitar a operação.

---

## AC-08 — Protecção no backend

**Dado** um utilizador que tente contornar a interface frontend,

**quando** efectuar directamente um pedido HTTP para uma operação não autorizada,

**então** o backend deve rejeitar a operação.

---

# 27. Casos limite

A implementação deve considerar:

### 27.1 Dois utilizadores com o mesmo identificador

O sistema não deve permitir identidades ambíguas.

---

### 27.2 Token ou sessão inválida

Uma credencial estruturalmente inválida deve ser rejeitada.

---

### 27.3 Token ou sessão expirada

Uma credencial expirada não deve permitir acesso a operações protegidas.

---

### 27.4 Utilizador eliminado ou desactivado

O sistema não deve continuar a tratar a conta como operacional apenas porque existia uma sessão anteriormente válida.

---

### 27.5 Alteração do papel

Se o papel de um utilizador for alterado, o comportamento das suas permissões deve seguir a política definida pela implementação de autenticação.

---

### 27.6 Acesso directo através da API

Um utilizador não deve obter permissões adicionais por ignorar a interface gráfica.

---

# 28. Dependências

Esta especificação depende de:

* modelo de utilizadores;
* persistência de utilizadores;
* gestão de eventos;
* gestão de reservas;
* gestão de ingressos;
* validação de ingressos.

As especificações destes domínios devem respeitar as regras de autorização definidas neste documento.

---

# 29. Relação com a API

A implementação da API deverá expor mecanismos equivalentes aos seguintes comportamentos:

```text
Autenticação
    │
    └── estabelecer identidade

Autorização
    │
    ├── verificar identidade
    ├── verificar papel
    └── verificar propriedade do recurso
```

Os endpoints concretos serão definidos na documentação da API.

---

# 30. Relação com testes

A implementação deve possuir testes que validem, no mínimo:

* autenticação bem-sucedida;
* autenticação falhada;
* acesso sem autenticação;
* acesso com papel incorrecto;
* acesso a recurso pertencente a outro utilizador;
* operações permitidas para cada papel;
* operações proibidas para cada papel.

Os testes devem validar o comportamento no backend e não apenas a visibilidade de elementos na interface.

---

# 31. Confirmação

A conformidade com esta especificação deve ser confirmada através de:

1. testes automatizados de autenticação;
2. testes automatizados de autorização;
3. testes de isolamento entre utilizadores;
4. testes dos papéis `ORGANIZER`, `CUSTOMER` e `GATEKEEPER`;
5. revisão da implementação dos endpoints protegidos;
6. execução do fluxo completo utilizando os utilizadores de teste fornecidos pelo projecto.

---

# 32. Questões em aberto

As seguintes decisões não são necessárias para concluir o comportamento funcional mínimo e serão definidas na arquitectura ou implementação:

* tecnologia exacta utilizada para autenticação;
* formato dos tokens ou sessões;
* duração exacta da sessão;
* mecanismo de renovação;
* mecanismo de revogação;
* política de recuperação de palavra-passe.

Estas decisões não devem alterar os comportamentos definidos nesta especificação.

---

# 33. Referências

* Requisitos funcionais do desafio Elite Dev.
* Requisitos não funcionais do desafio Elite Dev.
* Especificações relacionadas com eventos, reservas, pagamentos, ingressos e validação de ingressos.
* ADRs relacionados com autenticação, segurança e arquitectura da aplicação.