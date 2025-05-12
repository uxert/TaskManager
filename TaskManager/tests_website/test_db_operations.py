from datetime import datetime
from unittest import TestCase
import os

from pydantic import ValidationError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import close_all_sessions
from ..website import db, create_app, TEST_DATABASE_PATH
from ..website.db_operations import try_getting_user_tasks, try_add_new_task, try_getting_specific_task, \
    try_removing_specific_task, try_editing_specific_task
from ..website.models.requests import AddTaskRequestModel, EditTaskRequestModel


class TestDbOperations(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app(test=True)
        # Have to create a context manually - because the Flask app does not get any HTTP requests
        # during testing, so the context is not created automatically by Flask.
        cls.app_context = cls.app.app_context()
        cls.app_context.push()


    @classmethod
    def tearDownClass(cls):
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

        self.request_ctx = self.app.test_request_context()
        self.request_ctx.push()

    def tearDown(self):
        self.request_ctx.pop()

    def test_add_new_task(self):
        task_data = AddTaskRequestModel(
            title="Test task",
            importance = 5,
            deadline = datetime.now(),
            est_time_days = 3,
            description = "Hello, it's a test. Also, hello world!"
        )
        test_user_id = 42
        result = try_add_new_task(task_data, test_user_id)
        self.assertTrue(result.success)
        assigned_id = int(result.message)

        result = try_getting_specific_task(test_user_id, assigned_id)
        self.assertTrue(result.success)
        retrieved_task = result.task
        for attribute in ["title", "importance", "deadline", "est_time_days", "description"]:
            self.assertEqual(getattr(task_data, attribute), retrieved_task[attribute])

    def test_add_new_task_invalid(self):
        # someone passes something else than just AddTaskRequest
        task_data = {
            'title' : "Test task",
            'importance' : 5,
            'deadline' : datetime.now(),
            'est_time_days' : 3,
            'description' : "Hello, it's a test. Also, hello world!"
        }
        test_user_id = 42
        result = try_add_new_task(task_data, test_user_id)
        self.assertFalse(result.success)
        self.assertIsInstance(result.exception, TypeError)

    def test_AddTaskRequestModel_wrong_type(self):

        # someone tries to construct bad AddTaskRequest
        with self.assertRaises(ValidationError):
            task_data = AddTaskRequestModel(
                title="Test task",
                importance = "Yes, very important!",
                deadline = "tomorrow morning",
                est_time_days = 12,
                description = "Hello, it's a test. Also, hello world!"
            )

        # someone tries to modify good AddTaskRequest in a bad way
        task_data = AddTaskRequestModel(
            title="Test task",
            importance=10,
            deadline=datetime.now(),
            est_time_days=12,
            description="Hello, it's a test. Also, hello world!"
        )
        try:
            task_data.importance = 12
        except ValidationError:
            self.fail("There should not be any validation errors")

        with self.assertRaises(ValidationError):
            task_data.deadline = "tomorrow morning"

    def test_try_getting_specific_task_empty_db(self):
        res = try_getting_specific_task(42, 115)
        self.assertFalse(res.success)
        self.assertIsInstance(res.exception, NoResultFound)

    def test_try_getting_specific_task_wrong_arg_type(self):
        res1 = try_getting_specific_task(42, "Cat")
        res2 = try_getting_specific_task("Cat", 42)
        res3 = try_getting_specific_task("Cat", "Cat")
        self.assertFalse(res1.success)
        self.assertFalse(res2.success)
        self.assertFalse(res3.success)
        self.assertIsInstance(res1.exception, TypeError)
        self.assertIsInstance(res2.exception, TypeError)
        self.assertIsInstance(res3.exception, TypeError)


    def test_try_getting_user_tasks(self):
        task_data = AddTaskRequestModel(
            title="Test task",
            importance=10,
            deadline=datetime.now(),
            est_time_days=12,
            description="Hello, it's a test. Also, hello world!"
        )
        added_tasks = []
        test_user_id = 42
        res1 = try_add_new_task(task_data, test_user_id)
        self.assertTrue(res1.success)
        get_task_1_res = try_getting_specific_task(test_user_id, int(res1.message))
        self.assertTrue(get_task_1_res.success)
        added_tasks.append(get_task_1_res.task)

        task_data.title = "Second test task"
        task_data.importance = 999
        res2 = try_add_new_task(task_data, test_user_id)
        self.assertTrue(res2.success)
        get_task_2_res = try_getting_specific_task(test_user_id, int(res2.message))
        self.assertTrue(get_task_2_res.success)
        added_tasks.append(get_task_2_res.task)

        res_all_tasks = try_getting_user_tasks(test_user_id)
        self.assertTrue(res_all_tasks.success)

        #check that the lists contain the same tasks
        self.assertTrue(all(added_task in res_all_tasks.tasks for added_task in added_tasks))
        self.assertTrue((len(res_all_tasks.tasks) == len(added_tasks)))

    def test_try_getting_user_tasks_wrong_arg(self):
        res = try_getting_user_tasks("cat")
        self.assertFalse(res.success)
        self.assertIsInstance(res.exception, TypeError)

    def test_try_removing_specific_task(self):
        task_data = AddTaskRequestModel(
            title="Test task",
            importance=10,
            deadline=datetime.now(),
            est_time_days=12,
            description="Hello, it's a test. Also, hello world!"
        )
        test_user_id = 42
        res1 = try_add_new_task(task_data, test_user_id)
        self.assertTrue(res1.success)
        id_1 = int(res1.message)

        task_data.title = "Second test task"
        task_data.importance = 999
        res2 = try_add_new_task(task_data, test_user_id)
        self.assertTrue(res2.success)
        id_2 = int(res2.message)

        find_1_res = try_getting_specific_task(test_user_id, id_1)
        find_2_res = try_getting_specific_task(test_user_id, id_2)
        self.assertTrue(find_1_res.success)
        self.assertTrue(find_2_res.success)

        try_removing_specific_task(test_user_id, id_1)

        find_1_res = try_getting_specific_task(test_user_id, id_1)
        find_2_res = try_getting_specific_task(test_user_id, id_2)
        self.assertFalse(find_1_res.success)
        self.assertTrue(find_2_res.success)

        try_removing_specific_task(test_user_id, id_2)

        find_1_res = try_getting_specific_task(test_user_id, id_1)
        find_2_res = try_getting_specific_task(test_user_id, id_2)
        self.assertFalse(find_1_res.success)
        self.assertFalse(find_2_res.success)

    def test_try_remove_specific_task_wrong_arg(self):
        task_data = AddTaskRequestModel(
            title="Test task",
            importance=10,
            deadline=datetime.now(),
            est_time_days=12,
            description="Hello, it's a test. Also, hello world!"
        )
        test_user_id = 42
        res1 = try_add_new_task(task_data, test_user_id)
        self.assertTrue(res1.success)
        id_1 = int(res1.message)

        res_del_1 = try_removing_specific_task("test_user_id", id_1)
        res_del_2 = try_removing_specific_task(test_user_id, "id_1")
        res_del_3 = try_removing_specific_task("test_user_id", "id_1")

        self.assertIsInstance(res_del_1.exception, TypeError)
        self.assertIsInstance(res_del_2.exception, TypeError)
        self.assertIsInstance(res_del_3.exception, TypeError)

        res_del_4 = try_removing_specific_task(test_user_id, id_1)
        self.assertTrue(res_del_4.success)

    def test_try_editing_specific_task(self):
        task_data = AddTaskRequestModel(
            title="Test task",
            importance=10,
            deadline=datetime.now(),
            est_time_days=12,
            description="Hello, it's a test. Also, hello world!"
        )
        test_user_id = 42
        res1 = try_add_new_task(task_data, test_user_id)
        self.assertTrue(res1.success)
        id_1 = int(res1.message)

        edit_request = EditTaskRequestModel(
            task_id=id_1,
            title="Edited",
            importance=1,
            deadline=task_data.deadline, # do not change the deadline and est_days
            est_time_days=task_data.est_time_days,
            description="This was edited"
        )
        res_edit = try_editing_specific_task(test_user_id, edit_request)
        self.assertTrue(res_edit.success)

        res_after_edit = try_getting_specific_task(test_user_id, id_1)
        new_task = res_after_edit.task
        self.assertTrue(res_after_edit.success)
        self.assertTrue(new_task['title'] == "Edited")
        self.assertTrue(new_task['importance'] == 1)
        self.assertTrue(new_task['description'] == "This was edited")
        self.assertTrue(new_task['deadline'] == task_data.deadline)
        self.assertTrue(new_task['est_time_days'] == task_data.est_time_days)

    def test_try_editing_nonexistent_task(self):
        id_1 = 1
        edit_request = EditTaskRequestModel(
            task_id=id_1,
            title="Edited",
            importance=1,
            deadline=datetime.now(), # do not change the deadline and est_days
            est_time_days=15,
            description="This was edited"
        )
        test_user_id = 42
        res1 = try_editing_specific_task(test_user_id, edit_request)
        self.assertFalse(res1.success)
        self.assertIsInstance(res1.exception, NoResultFound)