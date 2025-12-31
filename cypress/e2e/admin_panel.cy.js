describe('Admin Panel', () => {
  beforeEach(() => {
    // Login as admin
    cy.visit('http://127.0.0.1:8000/usuarios/login/');
    cy.get('input[name="email"]').type('admin@gmail.com');
    cy.get('input[name="senha"]').type('root');
    cy.get('button[type="submit"]').click();
  });

  it('should access admin panel', () => {
    cy.visit('http://127.0.0.1:8000/usuarios/admin_panel/');
    cy.contains('Dashboard Administrativo').should('be.visible');
  });

  it('deve exibir cartões de estatísticas', () => {
    cy.visit('http://127.0.0.1:8000/usuarios/admin_panel/');
    cy.get('.stats-card').should('have.length', 4); // Assuming 4 stats cards
  });

  
  it('deve exibir a tabela de Sessões', () => {
    cy.visit('http://127.0.0.1:8000/usuarios/admin_panel/');
    cy.get(':nth-child(3) > .card-header > .mb-0').contains('Sessões').should('be.visible')
    
  });

  it('deve exibir a tabela de usuários', () => {
    cy.visit('http://127.0.0.1:8000/usuarios/admin_panel/');
    cy.get(':nth-child(4) > .card-header > .mb-0').contains('Usuários').should('be.visible')
  });

  it('Deverá exibir os três gráficos.', () => {
    cy.visit('http://127.0.0.1:8000/usuarios/admin_panel/');
    cy.get('canvas').should('have.length', 3); // Assuming 3 charts
  });

  it('Deverá editar um user', () => {
    cy.visit('http://127.0.0.1:8000/usuarios/admin_panel/');
    cy.get('a[href*="editar_usuario"]').first().click();
    cy.get('input[name="nome"]').clear().type('Updated User');
    cy.get('button[type="submit"]').click();

  });

  it('Deverá exlcuir um user', () => {
    cy.visit('http://127.0.0.1:8000/usuarios/admin_panel/');
    cy.get('button[onclick*="excluirUsuario"]').first().click();
    cy.on('window:confirm', () => true);
  });

  it('Deverá editar uma Sessão', () => {
    cy.visit('http://127.0.0.1:8000/usuarios/admin_panel/');
    cy.get('a[href*="excluir_sessao"]').first().click();
    cy.on('window:confirm', () => true);
    cy.get('button[type="submit"]').click();
  });


});
