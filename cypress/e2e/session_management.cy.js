describe('Session Management', () => {
  beforeEach(() => {
    // Login as admin user
    cy.visit('/login/');
    cy.get('input[name="email"]').type('admin@example.com');
    cy.get('input[name="senha"]').type('admin123');
    cy.get('button[type="submit"]').click();
  });

  it('should create a new session', () => {
    cy.visit('/criar_sessao/');
    cy.get('input[name="nome"]').type('Test Session');
    cy.get('input[name="senha"]').type('session123');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/listar_sessoes/');
    cy.contains('Sessão criada com sucesso').should('be.visible');
  });

  it('should list sessions', () => {
    cy.visit('/listar_sessoes/');
    cy.get('.card').should('have.length.greaterThan', 0);
  });

  it('should enter a session', () => {
    cy.visit('/listar_sessoes/');
    cy.get('.btn-primary').first().click(); // Assuming first session
    cy.get('input[name="senha"]').type('session123');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/itens/');
  });

  it('should edit a session', () => {
    cy.visit('/admin_panel/');
    cy.get('a[href*="editar_sessao"]').first().click();
    cy.get('input[name="nome"]').clear().type('Updated Session');
    cy.get('input[name="senha"]').clear().type('newpassword');
    cy.get('button[type="submit"]').click();
    cy.contains('Sessão atualizada com sucesso').should('be.visible');
  });

  it('should delete a session', () => {
    cy.visit('/admin_panel/');
    cy.get('a[href*="excluir_sessao"]').first().click();
    cy.get('button[type="submit"]').click();
    cy.contains('Sessão excluída com sucesso').should('be.visible');
  });
});
