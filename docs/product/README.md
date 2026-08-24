# Documentação do Produto

## 1. Objectivo

A pasta `docs/product/` contém a documentação relacionada com o produto, com o problema que a plataforma procura resolver e com o comportamento esperado pelos seus utilizadores.

Esta área descreve **o que a plataforma deve fazer e porquê**.

Não descreve, como regra geral, **como a plataforma deve ser implementada**.

A separação entre produto e implementação é importante porque uma mesma necessidade de negócio pode ser implementada de várias formas tecnicamente diferentes.

---

# 2. Separação entre produto e tecnologia

A documentação do produto deve concentrar-se em:

- problema;
- objectivos;
- utilizadores;
- necessidades;
- requisitos funcionais;
- regras de negócio;
- fluxos;
- critérios de aceitação;
- limitações;
- prioridades.

A documentação técnica deve concentrar-se em:

- arquitectura;
- componentes;
- tecnologias;
- persistência;
- APIs;
- infraestrutura;
- segurança;
- deployment;
- decisões técnicas.

A relação pode ser representada da seguinte forma:

```text
Produto
   │
   ├── Problema
   ├── Utilizadores
   ├── Objectivos
   ├── Requisitos
   ├── Regras de negócio
   └── Critérios de aceitação
             │
             ▼
       Especificações
             │
             ▼
        Arquitectura
             │
             ▼
       Implementação
````

Uma decisão tecnológica não deve alterar silenciosamente um requisito funcional.

Se uma limitação técnica obrigar a alterar o comportamento esperado do produto, essa alteração deve ser explicitamente discutida e documentada.

---

# 3. Produto

A plataforma é uma aplicação de gestão e venda de ingressos para eventos.

O sistema permite que:

* organizadores criem e publiquem eventos;
* clientes descubram eventos disponíveis;
* clientes reservem ingressos;
* clientes realizem um pagamento simulado;
* clientes recebam ingressos digitais;
* ingressos sejam representados através de QR Code;
* ingressos sejam partilhados através de um link;
* utilizadores de portaria validem ingressos no acesso ao evento.

O sistema deve suportar o fluxo completo desde a publicação de um evento até à validação do ingresso na entrada.

---

# 4. Problema

O produto procura demonstrar uma solução integrada para gestão de eventos e venda de ingressos.

O desafio não consiste apenas em apresentar páginas individuais.

É necessário demonstrar que as diferentes partes da plataforma funcionam como um único sistema:

```text
Evento
   │
   ▼
Descoberta
   │
   ▼
Reserva
   │
   ▼
Pagamento
   │
   ▼
Ingresso
   │
   ▼
QR Code
   │
   ▼
Portaria
   │
   ▼
Validação
```

O valor principal da solução está na consistência deste fluxo.

---

# 5. Utilizadores

A plataforma possui três papéis funcionais principais.

## 5.1. Organizador

O Organizador é responsável pela criação e gestão dos eventos.

As suas responsabilidades incluem:

* criar eventos;
* definir informação do evento;
* definir data;
* definir local;
* definir capacidade;
* definir preço;
* publicar eventos;
* gerir eventos que lhe pertencem.

O Organizador não deve possuir automaticamente permissões destinadas ao Cliente ou à Portaria.

---

## 5.2. Cliente

O Cliente é o utilizador que procura e compra ingressos.

As suas responsabilidades incluem:

* consultar eventos publicados;
* pesquisar eventos;
* consultar informação relevante;
* seleccionar ingressos;
* efectuar uma reserva;
* realizar o pagamento simulado;
* consultar os seus ingressos;
* visualizar o QR Code;
* partilhar um ingresso através de um link.

---

## 5.3. Portaria

O utilizador de Portaria é responsável pela validação dos ingressos no momento de entrada no evento.

As suas responsabilidades incluem:

* introduzir ou ler o código do ingresso;
* identificar o evento;
* validar o ingresso;
* receber uma indicação clara sobre o resultado;
* impedir a utilização repetida do mesmo ingresso.

A Portaria não deve possuir permissões para alterar dados administrativos do evento.

---

# 6. Objectivos do produto

Os principais objectivos são:

1. Demonstrar um fluxo completo de compra e utilização de ingressos.
2. Demonstrar separação clara entre os diferentes papéis.
3. Garantir que as regras críticas são aplicadas no backend.
4. Demonstrar integração com uma fonte externa de eventos.
5. Demonstrar uma experiência de utilização coerente.
6. Disponibilizar dados de demonstração suficientes para avaliação.
7. Disponibilizar documentação clara para execução e avaliação.
8. Demonstrar decisões técnicas conscientes em vez de implementação indiscriminada de funcionalidades.

---

# 7. Âmbito funcional

O produto deve incluir, no mínimo:

## Descoberta de eventos

O Cliente deve conseguir consultar eventos publicados.

A informação apresentada deve permitir compreender, pelo menos:

* nome;
* data;
* local;
* preço;
* disponibilidade, quando aplicável.

---

## Criação de eventos

O Organizador deve conseguir criar um evento utilizando informação proveniente de uma API externa de eventos.

As fontes permitidas pelo desafio incluem:

* Ticketmaster Discovery API;
* TMDb.

A solução pode utilizar uma das fontes ou ambas.

---

## Gestão de eventos

O Organizador deve conseguir gerir os eventos que criou.

A implementação exacta das operações de gestão deve ser definida na especificação funcional.

---

## Reserva

O Cliente deve conseguir reservar ingressos para um evento.

A solução pode implementar:

* mapa de lugares; ou
* quantidade de ingressos.

Também pode implementar ambos.

A implementação escolhida deve ser explicitamente documentada.

---

## Pagamento

O pagamento deve ser simulado.

O sistema deve representar pelo menos dois resultados:

```text
Pagamento aprovado
Pagamento recusado
```

O sistema não deve comunicar que uma compra foi concluída quando o pagamento tiver sido recusado.

---

## Ingresso

Após uma compra concluída, o Cliente deve conseguir consultar o ingresso.

O ingresso deve possuir um código representado através de QR Code.

O código não deve poder ser simplesmente manipulado pelo utilizador para produzir um ingresso aceite pelo sistema.

---

## Partilha

O Cliente deve conseguir obter um link que permita partilhar o ingresso.

O comportamento exacto de um ingresso partilhado deve ser definido nas especificações funcionais.

A existência do link não deve permitir ao utilizador alterar a validade ou os dados protegidos do ingresso.

---

## Validação

A Portaria deve conseguir validar um ingresso.

A validação deve suportar:

* leitura do QR Code através da câmara;
* introdução manual do código.

O sistema deve fornecer um resultado claramente identificável.

Os estados mínimos exigidos pelo desafio são:

```text
válido
inválido
já utilizado
evento errado
```

---

# 8. Regras de negócio críticas

As seguintes regras são consideradas fundamentais para a integridade do produto.

## 8.1. Não vender o mesmo lugar duas vezes

Quando for utilizada uma estratégia baseada em lugares, o sistema deve impedir que dois clientes adquiram o mesmo lugar.

Esta regra deve ser garantida pelo backend e pela persistência dos dados.

O frontend não é uma camada suficiente para garantir esta regra.

---

## 8.2. Não ultrapassar a capacidade

Quando a solução utilizar ingressos por quantidade, a quantidade vendida não pode ultrapassar a capacidade definida para o evento.

A disponibilidade deve ser calculada com base no estado persistido no backend.

---

## 8.3. Apenas pagamentos aprovados geram compra concluída

Um pagamento recusado não deve resultar num ingresso válido.

---

## 8.4. Um ingresso não pode ser utilizado duas vezes

Depois de um ingresso ter sido validado com sucesso, uma nova tentativa de utilização deve produzir o estado:

```text
já utilizado
```

---

## 8.5. O ingresso deve pertencer ao evento correcto

Um ingresso válido para um evento não deve ser aceite na entrada de outro evento.

---

## 8.6. O utilizador deve possuir o papel adequado

A operação disponível deve depender do papel autenticado.

Exemplo:

```text
Organizador → gestão de eventos
Cliente     → reserva e compra
Portaria    → validação
```

---

# 9. Fluxo principal

O fluxo principal do produto é:

```text
┌─────────────────────┐
│ Organizador         │
│ cria evento         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Evento publicado    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Cliente descobre    │
│ evento              │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Cliente selecciona  │
│ ingresso            │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Reserva             │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Pagamento simulado  │
└───────┬────────┬────┘
        │        │
     aprovado  recusado
        │        │
        ▼        ▼
    Ingresso   Compra
    criado     recusada
        │
        ▼
┌─────────────────────┐
│ QR Code             │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Entrada do evento   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Portaria lê código  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Backend valida      │
└──────────┬──────────┘
           │
      ┌────┴────┐
      ▼         ▼
    válido    inválido
      │
      ▼
 ingresso
 consumido
```

---

# 10. Estado do ingresso

O ingresso deve possuir um estado que permita determinar se ainda pode ser utilizado.

Um modelo conceptual é:

```text
ISSUED
   │
   ▼
VALID
   │
   ▼
USED
```

Uma tentativa de validação pode também resultar em:

```text
INVALID
WRONG_EVENT
ALREADY_USED
```

Os estados definitivos devem ser definidos na especificação do domínio.

---

# 11. Estado da reserva

A reserva deve possuir estados suficientemente claros para representar o seu ciclo de vida.

Um exemplo conceptual:

```text
PENDING
   │
   ├── PAYMENT_APPROVED ──► CONFIRMED
   │
   └── PAYMENT_DECLINED ──► FAILED
```

O modelo definitivo deve ser estabelecido antes da implementação da lógica de negócio correspondente.

---

# 12. Integração com catálogo externo

O organizador deve poder utilizar informação proveniente de uma fonte externa para montar um evento.

A fonte externa não deve ser considerada a fonte de verdade para o evento criado dentro da plataforma.

A relação conceptual é:

```text
External Catalog
       │
       ▼
Selection
       │
       ▼
Platform Event
       │
       ▼
Published Event
```

Depois de criado, o evento pertence ao domínio da plataforma.

Uma indisponibilidade temporária do fornecedor externo não deve invalidar automaticamente eventos já publicados.

---

# 13. Requisitos de experiência

A interface deve ser:

* clara;
* consistente;
* funcional;
* responsiva;
* compreensível sem instruções externas desnecessárias.

A interface não deve ser construída apenas para demonstrar que determinados componentes existem.

Cada ecrã deve possuir uma finalidade clara.

---

# 14. Requisitos específicos da portaria

A interface de Portaria deve privilegiar rapidez e clareza.

O utilizador deve conseguir determinar rapidamente:

```text
O ingresso é válido?
```

A resposta deve ser visualmente clara e não depender exclusivamente de texto pequeno ou informação secundária.

A interface deve disponibilizar:

```text
Leitura por câmara
        +
Introdução manual
```

A alternativa manual é obrigatória para situações em que a leitura automática não seja possível.

---

# 15. Dados de demonstração

O projecto deve disponibilizar dados de teste para facilitar a avaliação.

Devem existir pelo menos:

```text
1 Organizador
2 Clientes
1 utilizador de Portaria
1 evento publicado
Ingressos disponíveis
```

Os dados devem permitir percorrer o fluxo principal sem configuração manual extensa.

---

# 16. Critérios de aceitação do fluxo principal

O fluxo principal será considerado funcional quando for possível:

1. autenticar como Organizador;
2. criar ou configurar um evento;
3. publicar o evento;
4. consultar o evento como Cliente;
5. seleccionar ingressos;
6. efectuar uma reserva;
7. simular pagamento aprovado;
8. receber um ingresso;
9. visualizar o QR Code;
10. abrir o fluxo de Portaria;
11. ler ou introduzir o código;
12. validar o ingresso;
13. obter uma indicação de sucesso;
14. tentar validar novamente;
15. obter a indicação de que o ingresso já foi utilizado.

Também deve ser possível demonstrar o fluxo de pagamento recusado.

---

# 17. Fora do âmbito

O desafio explicitamente não exige:

* emissão de nota fiscal;
* revenda entre utilizadores;
* aplicação móvel nativa;
* recuperação de password;
* envio do ingresso por email.

Estas funcionalidades não devem receber prioridade durante a implementação inicial.

Podem ser adicionadas apenas se o fluxo principal estiver concluído e estável.

---

# 18. Funcionalidades opcionais

O desafio identifica como opcionais:

* pesquisa e filtros;
* painel do Organizador;
* cancelamento com devolução ao stock;
* mapa de lugares em tempo real;
* Docker Compose;
* testes;
* publicação da aplicação.

A prioridade deve ser:

```text
Fluxo principal
      ↓
Estabilidade
      ↓
Qualidade
      ↓
Documentação
      ↓
Funcionalidades opcionais
```

Uma funcionalidade opcional não deve comprometer a conclusão do fluxo obrigatório.

---

# 19. Critérios de prioridade

Quando existir conflito entre funcionalidades, deve ser utilizada a seguinte ordem:

### Prioridade 1 — Fluxo obrigatório

A aplicação deve permitir completar o percurso principal de ponta a ponta.

### Prioridade 2 — Integridade

As regras de negócio críticas devem funcionar correctamente.

### Prioridade 3 — Segurança

Autenticação, autorização e protecção dos ingressos devem ser tratadas antes de funcionalidades cosméticas.

### Prioridade 4 — Experiência

A interface deve ser clara e consistente.

### Prioridade 5 — Qualidade técnica

Testes, tratamento de erros, documentação e organização devem ser melhorados progressivamente.

### Prioridade 6 — Extras

Funcionalidades opcionais podem ser adicionadas depois das anteriores.

---

# 20. Relação com especificações

A documentação em `docs/product/` define necessidades e comportamento esperado.

A pasta `specs/` deverá transformar essas necessidades em especificações suficientemente precisas para orientar a implementação.

A relação será:

```text
docs/product/
       │
       ▼
    specs/
       │
       ▼
 architecture
       │
       ▼
 implementation
```

Uma especificação não deve inventar requisitos que contradigam a documentação do produto.

Quando uma decisão de produto mudar, as especificações afectadas devem ser revistas.

---

# 21. Relação com ADRs

Os ADRs documentam decisões arquitecturais e técnicas.

Eles não substituem os requisitos do produto.

Por exemplo:

```text
Produto:
"O Cliente deve conseguir reservar um ingresso."

ADR:
"Foi escolhida PostgreSQL para garantir persistência transaccional."

Especificação:
"A reserva deve impedir a aquisição concorrente do mesmo recurso."

Implementação:
"Transacção + constraint + lógica de serviço."
```

Cada documento possui uma responsabilidade diferente.

---

# 22. Alterações aos requisitos

Alterações aos requisitos devem ser explicitamente registadas.

Uma alteração relevante pode afectar:

```text
Produto
   │
   ├── Especificações
   │
   ├── ADRs
   │
   ├── API
   │
   ├── Frontend
   │
   ├── Backend
   │
   └── Testes
```

Não se deve alterar apenas a implementação quando a alteração modifica o comportamento esperado do produto.

---

# 23. Critérios de qualidade da documentação

Uma pessoa que não tenha participado no desenvolvimento deve conseguir compreender:

* qual é o problema;
* quem utiliza o produto;
* o que cada papel pode fazer;
* qual é o fluxo principal;
* quais são as regras críticas;
* o que é obrigatório;
* o que é opcional;
* o que está fora do âmbito.

A documentação deve utilizar linguagem técnica quando necessário, mas não deve exigir conhecimento prévio da implementação.

---

# 24. Regra de actualização

A documentação do produto deve ser actualizada quando ocorrer uma alteração relevante em:

* requisitos;
* comportamento;
* regras de negócio;
* utilizadores;
* âmbito;
* prioridades;
* critérios de aceitação.

Alterações puramente internas à implementação não precisam de alterar esta documentação quando o comportamento observável do produto permanece igual.

---

# 25. Princípio final

A plataforma deve ser construída a partir das necessidades que pretende satisfazer e não a partir das ferramentas que estão disponíveis.

A tecnologia deve servir o produto.

Quando existir uma decisão entre:

```text
"É tecnicamente interessante implementar isto?"
```

e:

```text
"É necessário para cumprir o objectivo do produto?"
```

a segunda pergunta deve determinar a prioridade.

O objectivo deste documento é garantir que a equipa consegue distinguir claramente essas duas situações.
