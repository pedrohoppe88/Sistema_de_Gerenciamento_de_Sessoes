describe('User Management', () => {
  beforeEach(() => {
    // Login as admin
    cy.login('admin@example.com', 'admin123');
  });

  it('should list all users', () => {
    cy.visit('/all_users/');
    cy.get('table').should('contain', 'Usuários');
  });

  it('should edit a user', () => {
    cy.visit('/editar_usuario/1/'); // Assuming user ID 1
    cy.get('input[name="nome"]').clear().type('Updated Name');
    cy.get('input[name="email"]').clear().type('updated@example.com');
    cy.get('select[name="graduacao"]').select('tenente');
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
