describe('CRM selected-release regression', () => {
  let fixture
  before(() => {
    const password = Cypress.env('adminPassword')
    expect(password, 'isolated site admin password').to.be.a('string').and.not.be.empty
    cy.loginUpgrade('Administrator', password)
    cy.callUpgrade('crm.tests.dinext_upgrade.prepare').then((response) => {
      fixture = response.body.message
      cy.loginUpgrade(fixture.user, fixture.password)
    })
  })

  after(() => {
    cy.leaveUpgradeApp()
    cy.loginUpgrade('Administrator', Cypress.env('adminPassword'))
    cy.callUpgrade('crm.tests.dinext_upgrade.cleanup')
  })

  it('loads the upgraded application with its synthetic fixture', () => {
    cy.visit('/crm/leads/' + encodeURIComponent(fixture.lead))
    cy.get('#app').should('be.visible')
    cy.location('pathname').should('include', '/crm')
    cy.contains(fixture.title).should('be.visible')
    cy.contains('button', 'Verify form script').should('be.visible').click()
    cy.contains('Form script verified').should('be.visible')
  })
})
