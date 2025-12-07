describe('Report Generation', () => {
  beforeEach(() => {
    // Login and enter a session
    cy.login('user@example.com', 'password123');
    cy.enterSession(1, 'session123'); // Assuming session ID 1
  });

  it('should generate PDF report', () => {
    cy.visit('/usuarios/1/itens/relatorio/pdf/'); // Assuming session ID 1
    cy.url().should('include', '.pdf'); // Check if PDF is generated
  });

  it('should display HTML report', () => {
    cy.visit('/usuarios/1/itens/relatorio/'); // Assuming session ID 1
    cy.contains('Relatório de Cautelas').should('be.visible');
  });
});
