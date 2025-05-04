from unittest import TestCase
import os
from sqlalchemy.orm import close_all_sessions
from sqlalchemy.exc import IntegrityError, ResourceClosedError
from website import db, create_app, TEST_DATABASE_PATH
from website.auth import register_user


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


