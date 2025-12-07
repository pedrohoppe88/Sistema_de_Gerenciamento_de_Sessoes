describe('Admin Panel', () => {
  beforeEach(() => {
    // Login as admin
    cy.visit('http://127.0.0.1:8000/usuarios/login/');
    cy.get('input[name="email"]').type('admin@example.com');
    cy.get('input[name="senha"]').type('admin123');
    cy.get('button[type="submit"]').click();
  });

  it('should access admin panel', () => {
    cy.visit('/admin_panel/');
    cy.contains('Painel de Administração').should('be.visible');
  });

  it('should display stats cards', () => {
    cy.visit('/admin_panel/');
    cy.get('.stats-card').should('have.length', 4); // Assuming 4 stats cards
  });

  it('should display users table', () => {
    cy.visit('/admin_panel/');
    cy.get('table').first().should('contain', 'Usuários');
  });

  it('should display sessions table', () => {
    cy.visit('/admin_panel/');
    cy.get('table').last().should('contain', 'Sessões');
  });

  it('should display charts', () => {
    cy.visit('/admin_panel/');
    cy.get('canvas').should('have.length', 3); // Assuming 3 charts
  });

  it('should edit a user', () => {
    cy.visit('/admin_panel/');
    cy.get('a[href*="editar_usuario"]').first().click();
    cy.get('input[name="nome"]').clear().type('Updated User');
    cy.get('button[type="submit"]').click();
    cy.contains('Usuário atualizado com sucesso').should('be.visible');
  });

  it('should delete a user', () => {
    cy.visit('/admin_panel/');
    cy.get('button[onclick*="excluirUsuario"]').first().click();
    cy.on('window:confirm', () => true);
    cy.contains('Usuário excluído com sucesso').should('be.visible');
  });
});
