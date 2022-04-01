from base import Base
from Criminalithe.app.modeles.utilisateurs import User



class TestUser(Base):
    """ Unit tests for Users """
    def test_creation(self):
        with self.app.app_context():
            statut, utilisateur = User.creer("Tea", "tea.pot@chartes.psl.eu", "Teapot", "UneTheiereEstCachee")
            query = User.query.filter(User.user_email == "tea.pot@chartes.psl.eu").first()
        self.assertEqual(query.user_nom, "Teapot")
        self.assertEqual(query.user_login, "Tea")
        self.assertNotEqual(query.user_password, "UneTheiereEstCachee")
        self.assertTrue(statut)

    def test_login_et_creation(self):
        with self.app.app_context():
            statut, cree = User.creer("Tea", "tea.pot@chartes.psl.eu", "Teapot", "UneTheiereEstCachee")
            connecte = User.identification("Tea", "UneTheiereEstCachee")

        self.assertEqual(cree, connecte)
        self.assertTrue(statut)