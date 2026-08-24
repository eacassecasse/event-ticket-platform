module.exports = {
  rules: {
    type: {
      enum: [
        "feat",
        "fix",
        "docs",
        "style",
        "refactor",
        "perf",
        "test",
        "build",
        "ci",
        "chore",
        "revert"
      ]
    },
    subject: {
      required: true
    }
  },

  prompt: {
    messages: {
      type: "Seleccione o tipo de alteração que está a realizar:",
      scope: "Indique o âmbito da alteração (opcional):",
      subject: "Descreva a alteração de forma curta e clara:",
      body: "Descreva os detalhes adicionais (opcional):",
      breaking: "Existem alterações incompatíveis com versões anteriores?",
      breakingBody:
        "Descreva as alterações incompatíveis e o impacto esperado:"
    },

    types: {
      feat: "Nova funcionalidade",
      fix: "Correcção de um erro",
      docs: "Alteração de documentação",
      style: "Formatação ou estilo sem alteração de comportamento",
      refactor: "Reestruturação sem alteração funcional",
      perf: "Melhoria de desempenho",
      test: "Alteração ou criação de testes",
      build: "Alteração do sistema de build/dependências",
      ci: "Alteração da integração ou entrega contínua",
      chore: "Manutenção técnica",
      revert: "Reversão de uma alteração anterior"
    }
  }
};