describe('User Registration', () => {
  it('should register a new user successfully', () => {
    cy.visit('/cadastrar/');
    cy.get('input[name="nome"]').type('Test User');
    cy.get('input[name="email"]').type('test@example.com');
    cy.get('select[name="graduacao"]').select('soldado');
    cy.get('input[name="senha"]').type('password123');
    cy.get('input[name="confirmar_senha"]').type('password123');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/login/');
    cy.contains('Usuário cadastrado com sucesso').should('be.visible');
  });

  it('should show error for duplicate email', () => {
    cy.visit('/cadastrar/');
    cy.get('input[name="nome"]').type('Test User 2');
    cy.get('input[name="email"]').type('test@example.com'); // Same email
    cy.get('select[name="graduacao"]').select('cabo');
    cy.get('input[name="senha"]').type('password123');
    cy.get('input[name="confirmar_senha"]').type('password123');
    cy.get('button[type="submit"]').click();
    cy.contains('Email já cadastrado').should('be.visible');
  });
});
