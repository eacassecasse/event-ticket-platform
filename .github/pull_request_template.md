## Descrição

Descreva de forma clara o que foi alterado e qual problema ou necessidade está a ser resolvido.

## Tipo de alteração

- [ ] Nova funcionalidade
- [ ] Correcção de erro
- [ ] Refactorização
- [ ] Testes
- [ ] Documentação
- [ ] Infraestrutura
- [ ] CI/CD
- [ ] Segurança
- [ ] Outra

## Alterações principais

Liste as alterações mais relevantes introduzidas nesta Pull Request.

- 
- 
- 

## Relação com Issue ou requisito

Indique a Issue, especificação ou requisito relacionado, quando aplicável.

Exemplo:

```text
Closes #123
````

## Validação

Indique os comandos, testes ou procedimentos utilizados para verificar a alteração.

```bash
# Exemplos
pnpm lint
pnpm test
```

Para alterações específicas, descreva também a validação manual realizada.

## Testes

* [ ] Foram adicionados novos testes.
* [ ] Foram actualizados testes existentes.
* [ ] Os testes existentes foram executados.
* [ ] Não foram necessários novos testes.
* [ ] Foi realizada validação manual quando aplicável.

## Documentação

* [ ] A documentação foi actualizada.
* [ ] A alteração não requer actualização da documentação.
* [ ] A documentação será actualizada numa alteração relacionada.

## Base de dados

* [ ] Não existem alterações à base de dados.
* [ ] Foram criadas/actualizadas migrações.
* [ ] Foram actualizados os dados de teste/seeding.
* [ ] As alterações foram validadas localmente.

## Segurança

* [ ] Não foram introduzidos segredos, credenciais ou API keys.
* [ ] Foram consideradas as implicações de autenticação.
* [ ] Foram consideradas as implicações de autorização.
* [ ] Foram consideradas as implicações de validação de dados.
* [ ] Não foram expostos dados sensíveis.
* [ ] Não aplicável.

## Compatibilidade

* [ ] A alteração mantém compatibilidade com o comportamento existente.
* [ ] A alteração introduz uma mudança de comportamento documentada.
* [ ] A alteração requer actualização de outros componentes.
* [ ] Não aplicável.

## Checklist do autor

* [ ] A branch foi criada a partir da branch correcta.
* [ ] A Pull Request possui um âmbito claramente definido.
* [ ] O código segue os padrões definidos no projecto.
* [ ] O lint passa sem erros.
* [ ] Os testes aplicáveis passam.
* [ ] Não existem ficheiros ou alterações desnecessárias.
* [ ] Não existem segredos ou credenciais no código.
* [ ] A documentação necessária foi actualizada.
* [ ] As mensagens de commit seguem Conventional Commits.
* [ ] As limitações conhecidas estão documentadas.
* [ ] A alteração foi revista pelo próprio autor antes da submissão.

## Limitações conhecidas

Descreva limitações, dívida técnica, funcionalidades não implementadas ou comportamentos conhecidos que possam ser relevantes para a revisão.

Se não existirem:

```text
Nenhuma limitação conhecida.
```

## Notas para revisão

Indique áreas específicas que mereçam atenção durante a revisão.

Por exemplo:

* decisões arquitecturais;
* regras de negócio;
* concorrência;
* segurança;
* tratamento de erros;
* alterações de base de dados;
* integração com serviços externos.

```text
Nenhuma nota adicional.
```

````

### Recommended final location

Your repository should now have:

```text
.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   └── feature_request.md
└── pull_request_template.md
````

This version is intentionally more detailed than a generic GitHub template because the challenge explicitly evaluates **how you think, document decisions, validate the implementation, and communicate technical trade-offs**, not merely whether the application runs.
