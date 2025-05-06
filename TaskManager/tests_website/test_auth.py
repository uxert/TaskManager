from unittest import TestCase
import os
from sqlalchemy.orm import close_all_sessions
from sqlalchemy.exc import IntegrityError, ResourceClosedError, NoResultFound
from website import db, create_app, TEST_DATABASE_PATH
from website.auth import register_user, is_email_available, is_username_available, perform_login


class TestAuth(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(test=True)
        # Have to create a context manually - because for now the Flask app does not get any HTTP requests
        # during testing, so the context is not created automatically by Flask.
        cls.app_context = cls.app.app_context()
        cls.app_context.push()


    @classmethod
    def tearDownClass(cls):
        # db.session.close_all() # deprecated in newer sqLite!
        close_all_sessions()
        db.drop_all()
        if os.path.exists(TEST_DATABASE_PATH):
            os.remove(TEST_DATABASE_PATH)
            print(f"Removed test database from {TEST_DATABASE_PATH}")
        cls.app_context.pop()

    def setUp(self):
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

    def tearDown(self):
        pass

    def test_register_user_valid(self):
        res1 = register_user("random@randomness.ran", "random_of_course", "123123123")
        res2 = register_user("Kowalski@Analiza.pl", "kowalski", "OhMyOhMy")
        self.assertTrue(res1.success)
        self.assertTrue(res2.success)

    def test_register_user_repeating_(self):
        res1 = register_user("random@randomness.ran", "random_of_course", "123123123")
        res2 = register_user("random@randomness.ran", "random_of_course", "123123123")

        self.assertTrue(res1.success)
        self.assertFalse(res2.success)
        self.assertIsInstance(res2.exception, IntegrityError)

    def test_is_username_available(self):
        some_name = "Jack"
        res1 = is_username_available(some_name)
        register_user(email="some@email.com", username=some_name, password="Ladidadida")
        res2 = is_username_available(some_name)
        res3 = is_username_available(some_name + "!")

        self.assertTrue(res1)
        self.assertFalse(res2)
        self.assertTrue(res3)

    def test_is_email_available(self):
        some_email = ("jack@email.com")
        res1 = is_email_available(some_email)
        register_user(email=some_email, username="Jack", password="Ladidadida")
        res2 = is_email_available(some_email)
        res3 = is_email_available(some_email + "!")

        self.assertTrue(res1)
        self.assertFalse(res2)
        self.assertTrue(res3)

    def test_perform_login(self):
        res1 = perform_login("random@randomness.ran", "Ladidadida")
        self.assertFalse(res1.success)
        self.assertIsInstance(res1.exception, NoResultFound)

        register_user("random@randomness.ran", "random_of_course", "Ladidadida")
        res2 = perform_login("random_of_course", "Ladidadida")
        self.assertTrue(res2.success)

