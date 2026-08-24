# Política de Segurança

## Objectivo

Este documento define como devem ser comunicadas vulnerabilidades de segurança identificadas neste projecto.

A segurança é tratada como uma responsabilidade transversal da aplicação, abrangendo código, dependências, configuração, autenticação, autorização, persistência de dados e infraestrutura.

## Comunicação de vulnerabilidades

Não devem ser abertas issues públicas para comunicar vulnerabilidades que possam permitir:

- acesso não autorizado;
- exposição de dados;
- bypass de autenticação ou autorização;
- manipulação indevida de reservas ou bilhetes;
- utilização fraudulenta de bilhetes;
- exposição de credenciais;
- comprometimento da infraestrutura.

Sempre que o projecto possuir um canal privado de reporte configurado no GitHub, esse canal deve ser utilizado.

Durante o desenvolvimento deste projecto, caso não exista ainda um mecanismo privado configurado, as vulnerabilidades devem ser comunicadas directamente ao responsável pelo repositório antes de serem divulgadas publicamente.

## Informação recomendada

Uma comunicação de vulnerabilidade deve incluir, sempre que possível:

- descrição do problema;
- componente afectado;
- passos para reproduzir;
- impacto esperado;
- evidência técnica;
- eventual solução ou mitigação conhecida.

Não devem ser incluídos dados pessoais ou credenciais reais.

## Segredos

É proibido versionar:

- passwords;
- API keys;
- tokens;
- chaves privadas;
- credenciais da base de dados;
- secrets utilizados pelos serviços externos.

Os valores devem ser fornecidos através de variáveis de ambiente ou mecanismos equivalentes de gestão de segredos.

## Dependências

As dependências utilizadas pelo projecto devem ser mantidas sob controlo e verificadas através das ferramentas de segurança configuradas no CI.

Uma vulnerabilidade conhecida numa dependência deve ser avaliada considerando:

1. severidade;
2. componente afectado;
3. possibilidade de exploração;
4. exposição da aplicação;
5. disponibilidade de correcção;
6. impacto de actualizar ou substituir a dependência.

## Responsabilidade

A existência de ferramentas automatizadas de segurança não substitui a análise técnica realizada pelos developers.

Ferramentas de análise devem ser utilizadas como mecanismos de detecção e prevenção, não como garantia absoluta de ausência de vulnerabilidades.