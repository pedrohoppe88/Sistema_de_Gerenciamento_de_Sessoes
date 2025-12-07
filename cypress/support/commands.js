// Custom commands for Cypress tests

Cypress.Commands.add('login', (email, password) => {
  cy.visit('/usuarios/login/');
  cy.get('input[name="email"]').type(email);
  cy.get('input[name="senha"]').type(password);
  cy.get('button[type="submit"]').click();
});

Cypress.Commands.add('register', (nome, email, graduacao, senha) => {
  cy.visit('/usuarios/cadastrar/');
  cy.get('input[name="nome"]').type(nome);
  cy.get('input[name="email"]').type(email);
  cy.get('select[name="graduacao"]').select(graduacao);
  cy.get('input[name="senha"]').type(senha);
  cy.get('input[name="confirmar_senha"]').type(senha);
  cy.get('button[type="submit"]').click();
});

Cypress.Commands.add('createSession', (nome, senha) => {
  cy.visit('/usuarios/criar_sessao/');
  cy.get('input[name="nome"]').type(nome);
  cy.get('input[name="senha"]').type(senha);
  cy.get('button[type="submit"]').click();
});

Cypress.Commands.add('enterSession', (sessionId, sessionPassword) => {
  cy.visit(`/listar_sessoes/`);
  cy.get(`a[href="/entrar_sessao/${sessionId}/"]`).click();
  cy.get('input[name="senha"]').type(sessionPassword);
  cy.get('button[type="submit"]').click();
});
