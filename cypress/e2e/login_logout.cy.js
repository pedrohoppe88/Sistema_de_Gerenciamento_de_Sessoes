describe('Login and Logout', () => {
  it('should login successfully', () => {
    cy.visit('/usuarios/login/');
    cy.get('input[name="email"]').type('admin@gmail.com');
    cy.get('input[name="senha"]').type('root');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/usuarios/sucesso/');
    cy.contains('Bem-vindo').should('be.visible');
  });

  it('should show error for invalid credentials', () => {
    cy.visit('/usuarios/login/');
    cy.get('input[name="email"]').type('invalid@example.com');
    cy.get('input[name="senha"]').type('wrongpassword');
    cy.get('button[type="submit"]').click();
    cy.contains('Usuário não encontrado').should('be.visible');
  });

  it('executar cadastro errado com email já existente', () => {
    cy.visit('http://127.0.0.1:8000/usuarios/cadastrar/')
    cy.get('input[name="email"]').type('admin@gmail.com');
    cy.get('input[name="senha"]').type('root');
    cy.get('input[name="nome"]').type('saga');
    cy.get('#id_graduacao').select(['Cabo']);
    cy.get('input[name="confirmar_senha"]').type('root')
    cy.get('input[name="pin"]').type('1234');
    cy.get('input[name="pin_confirm"]').type('1234')
    cy.get('button[type="submit"]').click();
    cy.contains('Usuario with this Email already exists.').should('be.visible');

  })


  it('executar novo cadastro correto', () => {

  const email = `user_${Date.now()}@teste.com`
  const nome = `nome_${Math.floor(Math.random() * 1000)}`
  const pin = Math.floor(1000 + Math.random() * 9000).toString()

  const graduacoes = ['Soldado', 'Cabo', '3_sargento']
  const graduacaoAleatoria = graduacoes[Math.floor(Math.random() * graduacoes.length)]

  cy.visit('http://127.0.0.1:8000/usuarios/cadastrar/')
  
  cy.get('input[name="email"]').type(email)
  cy.get('input[name="senha"]').type('root')
  cy.get('input[name="nome"]').type(nome)
  
  cy.get('#id_graduacao').select(graduacaoAleatoria)

  cy.get('input[name="confirmar_senha"]').type('root')
  cy.get('input[name="pin"]').type(pin)
  cy.get('input[name="pin_confirm"]').type(pin)
  
  cy.get('button[type="submit"]').click()

})


 it('should logout successfully', () => {

    cy.visit('/usuarios/login/');
    cy.get('input[name="email"]').type('admin@gmail.com');
    cy.get('input[name="senha"]').type('root');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/usuarios/sucesso/');
    cy.contains('Bem-vindo').should('be.visible');

    cy.visit('http://127.0.0.1:8000/');
    cy.contains('Sair').click() // clica no botão de fazer o Logout
  });


})





 