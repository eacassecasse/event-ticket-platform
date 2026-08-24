# Especificação de Descoberta de Eventos

**Estado:** `approved`  
**Versão:** `1.0`  
**Última actualização:** `2026-08-22`

---

# 1. Objectivo

Esta especificação define o comportamento responsável pela descoberta de conteúdos que podem ser utilizados como base para a criação de eventos na Plataforma de Eventos e Ingressos.

A plataforma deverá integrar-se com uma API externa de catálogo, permitindo ao Organizador seleccionar um conteúdo existente e utilizá-lo como referência para a criação de um evento.

O catálogo externo poderá ser proveniente de:

- Ticketmaster Discovery API;
- TMDb.

A implementação poderá utilizar uma destas fontes ou ambas.

A descoberta de conteúdos externos deve ser tratada como uma funcionalidade distinta da gestão dos eventos próprios da plataforma.

---

# 2. Âmbito

Esta especificação cobre:

- integração com uma API externa de catálogo;
- pesquisa de conteúdos;
- consulta de detalhes de um conteúdo externo;
- normalização dos dados recebidos;
- apresentação dos resultados ao utilizador;
- utilização de um conteúdo externo durante a criação de um evento;
- tratamento de erros da API externa;
- indisponibilidade temporária do serviço externo;
- separação entre catálogo externo e eventos internos da plataforma.

Esta especificação não cobre:

- criação de eventos;
- publicação de eventos;
- reservas;
- pagamentos;
- emissão de ingressos;
- validação de ingressos.

Essas responsabilidades são definidas pelas respectivas especificações.

---

# 3. Conceitos fundamentais

Existem dois conceitos que não devem ser confundidos.

## 3.1 Conteúdo externo

É uma obra, espectáculo, filme ou outro conteúdo disponibilizado por uma API externa.

Exemplo:

```text
Conteúdo externo
    │
    ├── ID externo
    ├── Título
    ├── Descrição
    ├── Imagem
    ├── Data original
    └── Fonte
````

Este conteúdo não pertence à base de dados de eventos da plataforma.

---

## 3.2 Evento da plataforma

É uma ocorrência concreta criada pelo Organizador.

Exemplo:

```text
Evento
    │
    ├── Conteúdo seleccionado
    ├── Data
    ├── Hora
    ├── Local
    ├── Capacidade
    ├── Preço
    └── Estado
```

O mesmo conteúdo externo poderá servir de base para vários eventos.

Por exemplo:

```text
Filme: "Exemplo"

Evento 1
19/09/2026 — 18:00 — Cinema A

Evento 2
20/09/2026 — 21:00 — Cinema B
```

Não devem ser tratados como o mesmo evento.

---

# 4. Fonte externa

A aplicação poderá utilizar:

```text
Ticketmaster Discovery API
```

ou:

```text
TMDb
```

A arquitectura deverá evitar espalhar dependências específicas destas APIs pelo restante sistema.

A integração deverá ser encapsulada através de uma camada própria.

---

# 5. Abstracção do catálogo

O domínio da aplicação deve trabalhar com um modelo normalizado.

Conceptualmente:

```text
API externa
     │
     ▼
Adapter / Integration
     │
     ▼
Modelo normalizado
     │
     ▼
Application Service
     │
     ├── API
     └── Frontend
```

O restante sistema não deve depender directamente da estrutura de resposta da Ticketmaster ou da TMDb.

---

# 6. Modelo normalizado

Um resultado de catálogo deve possuir informação suficiente para permitir ao Organizador identificar o conteúdo.

O modelo mínimo deve suportar:

```text
external_id
source
title
description
image_url
```

Poderão ser incluídos outros atributos disponibilizados pela fonte externa quando estes forem úteis para a experiência de utilização.

A aplicação não deve assumir que todas as fontes fornecem exactamente os mesmos campos.

---

# 7. Identificação da fonte

Cada conteúdo externo deve manter a identificação da fonte.

Exemplo:

```text
source = TMDB
external_id = 123456
```

ou:

```text
source = TICKETMASTER
external_id = abc123
```

A combinação:

```text
source + external_id
```

deve ser considerada a identidade do conteúdo externo.

Isto evita colisões entre identificadores provenientes de fontes diferentes.

---

# 8. Pesquisa

A aplicação deve permitir que o utilizador pesquise conteúdos disponíveis na fonte externa.

Exemplo:

```text
Pesquisa:
"Batman"
```

Resultado conceptual:

```text
Batman
Batman Begins
The Batman
Batman Returns
```

Cada resultado deve fornecer informação suficiente para que o Organizador consiga identificar correctamente o conteúdo.

---

# 9. Pesquisa vazia

Uma pesquisa vazia não deve provocar uma chamada externa desnecessária.

A aplicação poderá:

* rejeitar a pesquisa;
* solicitar um termo;
* apresentar conteúdos populares, caso essa funcionalidade seja suportada.

Para o MVP, recomenda-se exigir um termo de pesquisa.

---

# 10. Limitação dos resultados

A aplicação deve limitar a quantidade de resultados apresentados.

Não é necessário transferir todo o catálogo externo.

Exemplo:

```text
GET /catalog/search?q=batman&page=1
```

A implementação poderá utilizar paginação quando suportada pela API externa.

---

# 11. Tempo de resposta

A API externa pode possuir latência superior à da aplicação.

A aplicação deve evitar bloquear indefinidamente uma operação de pesquisa.

Devem existir limites de tempo para chamadas externas.

Quando a API externa não responder dentro do período aceitável, a operação deve ser tratada como falhada.

---

# 12. Indisponibilidade da API externa

A indisponibilidade do catálogo externo não deve provocar uma falha geral da aplicação.

Por exemplo:

```text
Ticketmaster / TMDb
        │
        X
   indisponível
        │
        ▼
Pesquisa falha
        │
        ▼
Aplicação continua operacional
```

O utilizador deve receber uma mensagem compreensível indicando que não foi possível obter os resultados.

Não devem ser apresentados erros internos ou detalhes técnicos desnecessários.

---

# 13. Erros da API externa

A integração deve tratar pelo menos:

* timeout;
* erro de autenticação da API;
* limite de pedidos atingido;
* resposta inválida;
* erro HTTP;
* serviço indisponível;
* falha de rede.

A aplicação deve converter estes erros para uma representação apropriada ao domínio da plataforma.

O frontend não deve depender dos códigos de erro específicos da API externa.

---

# 14. Credenciais da API externa

As credenciais utilizadas para aceder à API externa não podem ser armazenadas no código-fonte.

Devem ser fornecidas através da configuração do ambiente.

Exemplo conceptual:

```text
TICKETMASTER_API_KEY
```

ou:

```text
TMDB_API_KEY
```

Os nomes definitivos serão definidos na implementação.

As credenciais não devem ser incluídas no repositório Git.

---

# 15. Limites da API externa

A implementação deve considerar que as APIs externas podem impor limites de utilização.

A aplicação não deve:

* efectuar chamadas desnecessárias;
* repetir imediatamente chamadas que falharam;
* efectuar chamadas duplicadas para a mesma operação sem necessidade.

A implementação poderá utilizar mecanismos de cache caso isso seja necessário.

Para o MVP, uma estratégia de cache simples ou ausência de cache é aceitável, desde que a aplicação não efectue chamadas excessivas.

---

# 16. Criação de eventos a partir do catálogo

O fluxo principal esperado é:

```text
Organizador
    │
    ▼
Pesquisar catálogo
    │
    ▼
Seleccionar conteúdo
    │
    ▼
Preencher dados do evento
    │
    ├── Data
    ├── Hora
    ├── Local
    ├── Capacidade
    └── Preço
    │
    ▼
Criar evento
```

A selecção do conteúdo externo não deve criar automaticamente um evento publicado.

O Organizador deve completar os dados necessários do evento.

---

# 17. Persistência do conteúdo externo

A aplicação poderá armazenar uma referência ao conteúdo externo quando um Organizador criar um evento.

Por exemplo:

```text
Event
├── external_source
├── external_id
├── title
├── description
├── image_url
├── date
├── time
├── venue
├── capacity
└── price
```

A decisão sobre armazenar uma cópia dos dados externos deve privilegiar a estabilidade do evento.

Depois de criado, o evento não deve depender da disponibilidade da API externa para ser apresentado ao Cliente.

---

# 18. Independência dos eventos publicados

Uma vez criado e publicado um evento, a consulta desse evento não deve depender obrigatoriamente da API externa.

Exemplo:

```text
API externa
    │
    │ utilizada durante criação
    ▼
Evento interno
    │
    ▼
Base de dados
    │
    ▼
Cliente consulta evento
```

Isto significa que a indisponibilidade posterior da API externa não deve impedir a consulta dos eventos já publicados.

---

# 19. Alteração do conteúdo externo

Se os dados de um conteúdo externo forem posteriormente alterados na fonte original, isso não deve alterar silenciosamente um evento já criado.

Por exemplo:

```text
API externa:
Título = "Filme A"

Evento criado:
Título = "Filme A"
```

Se a API externa passar a devolver:

```text
Título = "Filme A — Edição Especial"
```

o evento existente não deve ser automaticamente alterado sem uma operação explícita da aplicação.

---

# 20. Imagens externas

Quando forem utilizadas imagens provenientes da API externa, a aplicação deve tratar a URL como uma referência externa.

A disponibilidade da imagem não deve ser considerada essencial para a integridade do evento.

Se uma imagem deixar de estar disponível, os restantes dados do evento devem continuar funcionais.

---

# 21. Conteúdo não encontrado

Quando o identificador externo solicitado deixar de existir:

```text
GET /catalog/{source}/{external_id}
```

a aplicação deve comunicar que o conteúdo não foi encontrado.

Não deve criar um evento com dados incompletos simplesmente porque a referência externa deixou de existir.

---

# 22. Dados incompletos

A aplicação não deve assumir que a fonte externa fornece todos os dados necessários para a criação de um evento.

Por exemplo, a API pode fornecer:

```text
Título
Descrição
Imagem
```

mas não:

```text
Preço
Capacidade
Local
```

Esses dados pertencem ao evento da plataforma e devem ser definidos pelo Organizador.

---

# 23. Separação entre catálogo e evento

O seguinte princípio deve ser mantido:

> O catálogo externo fornece informação sobre o conteúdo; a plataforma define a ocorrência concreta desse conteúdo.

Exemplo:

```text
TMDb
  │
  └── "Dune: Part Two"
          │
          ▼
      Organizador
          │
          ├── 25/09/2026
          ├── 20:00
          ├── Cinema X
          ├── 120 lugares
          └── 850 MT
          │
          ▼
     Evento da plataforma
```

---

# 24. Segurança

As respostas da API externa devem ser tratadas como dados externos não confiáveis.

A aplicação deve:

* validar os dados recebidos;
* evitar assumir formatos não verificados;
* sanitizar conteúdos apresentados quando necessário;
* não executar conteúdo recebido da API;
* não permitir que dados externos contornem as regras de validação da aplicação.

---

# 25. Autorização

A pesquisa no catálogo pode ser disponibilizada apenas a utilizadores autenticados, caso seja utilizada exclusivamente durante a criação de eventos.

A criação do evento deve respeitar as regras definidas na especificação de Autenticação e Autorização.

Um Cliente não deve conseguir utilizar directamente a API de catálogo para criar eventos.

---

# 26. API interna

A aplicação deverá expor uma interface própria para a camada frontend.

Exemplo conceptual:

```text
GET /catalog/search
GET /catalog/{source}/{external_id}
```

Os endpoints concretos poderão variar.

O frontend não deve chamar directamente a Ticketmaster ou a TMDb quando isso permitiria expor:

* API keys;
* regras internas;
* detalhes de integração;
* dependências específicas da fonte.

---

# 27. Estratégia de integração

A integração deverá seguir uma separação semelhante a:

```text
app/
├── integrations/
│   └── catalog/
│       ├── ticketmaster/
│       ├── tmdb/
│       └── models.py
│
└── services/
    └── catalog/
```

A organização concreta dos ficheiros poderá variar conforme a arquitectura final.

A regra importante é que a lógica de negócio não fique dependente directamente da implementação de uma API externa específica.

---

# 28. Troca de fornecedor

A arquitectura deve permitir substituir:

```text
TMDb
```

por:

```text
Ticketmaster
```

sem reescrever a lógica de criação de eventos.

Da mesma forma, a aplicação poderá futuramente suportar ambas as fontes.

---

# 29. Critérios de aceitação

## AC-01 — Pesquisa

**Dado** um utilizador autorizado,

**quando** pesquisar um conteúdo existente,

**então** a aplicação deve apresentar resultados provenientes da fonte configurada.

---

## AC-02 — Resultado normalizado

**Dado** um resultado proveniente da API externa,

**quando** for apresentado ao utilizador,

**então** os dados devem seguir o modelo normalizado da aplicação.

---

## AC-03 — Selecção

**Dado** um resultado válido,

**quando** o Organizador o seleccionar,

**então** o conteúdo deve poder ser utilizado como base para a criação de um evento.

---

## AC-04 — Dados próprios do evento

**Dado** um conteúdo seleccionado,

**quando** o Organizador criar um evento,

**então** deve conseguir definir pelo menos:

* data;
* hora;
* local;
* capacidade;
* preço.

---

## AC-05 — Independência

**Dado** um evento já criado,

**quando** a API externa ficar indisponível,

**então** o evento deve continuar disponível através da aplicação.

---

## AC-06 — API indisponível

**Dado** que a API externa está indisponível,

**quando** o utilizador efectuar uma pesquisa,

**então** a aplicação deve apresentar um erro controlado.

---

## AC-07 — Conteúdo inexistente

**Dado** um identificador externo inexistente,

**quando** a aplicação tentar consultar o conteúdo,

**então** deve informar que o conteúdo não foi encontrado.

---

## AC-08 — Credenciais protegidas

**Dado** que a aplicação necessita de uma chave da API externa,

**quando** o projecto for executado,

**então** a chave deve ser fornecida através da configuração do ambiente e não através do código-fonte.

---

# 30. Casos limite

A implementação deve considerar:

### 30.1 Pesquisa sem resultados

A aplicação deve apresentar uma resposta clara indicando que não foram encontrados conteúdos correspondentes.

---

### 30.2 Pesquisa com caracteres inválidos

O termo deve ser validado antes de ser enviado à API externa.

---

### 30.3 Timeout

A aplicação deve terminar a operação após o limite definido, em vez de permanecer indefinidamente à espera.

---

### 30.4 Resposta externa inválida

Uma resposta que não cumpra o formato esperado deve ser rejeitada pelo adaptador.

---

### 30.5 Limite de pedidos

A aplicação deve tratar de forma controlada uma resposta indicando que o limite da API foi atingido.

---

### 30.6 Conteúdo sem imagem

A ausência de imagem não deve impedir a utilização do conteúdo.

---

### 30.7 Conteúdo sem descrição

A ausência de descrição não deve impedir a criação do evento, desde que os dados obrigatórios para o evento estejam disponíveis ou possam ser definidos pelo Organizador.

---

### 30.8 API externa indisponível durante consulta de evento

Um evento já persistido deve continuar disponível.

---

# 31. Testes

A implementação deve possuir testes para:

* pesquisa com resultados;
* pesquisa sem resultados;
* conteúdo inexistente;
* resposta externa inválida;
* timeout;
* erro HTTP;
* normalização dos resultados;
* utilização de diferentes fontes;
* criação de evento a partir de conteúdo externo;
* independência do evento depois da sua criação.

Os testes de integração com a API externa devem evitar depender exclusivamente do serviço real.

Sempre que apropriado, devem ser utilizadas respostas simuladas.

---

# 32. Observabilidade

As falhas de integração devem ser registadas de forma suficiente para diagnóstico.

Os registos devem permitir identificar:

* fonte utilizada;
* operação realizada;
* resultado da operação;
* duração;
* tipo de erro.

Não devem ser registadas:

* API keys;
* credenciais;
* tokens;
* dados sensíveis desnecessários.

---

# 33. Confirmação

A conformidade com esta especificação deve ser confirmada através de:

1. testes automatizados da integração;
2. testes do modelo normalizado;
3. testes de tratamento de erros;
4. teste de criação de evento a partir de conteúdo externo;
5. teste de independência dos eventos relativamente à API externa;
6. revisão da configuração das credenciais;
7. execução do fluxo completo através da interface.

---

# 34. Questões em aberto

As seguintes decisões serão determinadas durante a implementação:

* utilização da Ticketmaster, TMDb ou ambas;
* estratégia exacta de cache;
* limites de timeout;
* política de retry;
* número máximo de resultados;
* política de paginação;
* campos opcionais adicionais;
* fornecedor principal caso sejam utilizadas duas fontes.

Estas decisões não devem alterar os princípios fundamentais definidos nesta especificação.

---

# 35. Referências

* Requisitos funcionais do desafio Elite Dev.
* Ticketmaster Discovery API.
* TMDb API.
* Especificação de Autenticação e Autorização.
* Especificação de Gestão de Eventos.