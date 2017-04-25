'''
* It Worked Yesterday...
* 3/20/17
* unit_test.py
* Handles all the unit tests.
'''
import unittest
import canvas

usertoken = None
class RetrieveFromCanvasTest(unittest.TestCase):

    # Test to see if able to retrieve token from file
    def test_a_obtain_token(self):
        self.token = None
        try:
            token_file = open('usertoken.txt', 'r')
            self.token = token_file.read()
            token_file.close()
        except:
            pass
        self.assertIsNotNone(self.token)

    # Test to see if able to retrieve at least one class from canvas
    def test_b_has_courses(self):
        global user_token
        user_token = None
        self.courses = []
        try:
            token_file = open('usertoken.txt', 'r')
            user_token = token_file.read()
            token_file.close()
        except:
            pass
        try:
            self.courses = canvas.get_favorite_courses(user_token)
        except:
            pass
        self.assertIsNotNone(user_token)
        self.assertGreater(len(self.courses), 0)

    # Test to see if able to pull at least one assignment from canvas
    def test_c_has_assignments(self):
        global user_token
        user_token = None
        self.courses = []
        try:
            token_file = open('usertoken.txt', 'r')
            user_token = token_file.read()
            token_file.close()
        except:
            pass
        try:
            self.courses = canvas.get_favorite_courses(user_token)
        except:
            pass
        self.assignments = []
        try:
            for course in self.courses:
                self.course_assignments = canvas.get_assignments(str(course['id']),user_token)
                # print(self.course_assignments)
                for assignment in self.course_assignments:
                    self.assignments.append(assignment)
        except:
            pass
        self.assertIsNotNone(user_token)
        self.assertIsNotNone(self.courses)
        self.assertGreater(len(self.assignments), 0)

class WebsiteDependencyTest(unittest.TestCase):
    # Simple test to see if you have imported Django correctly
    def test_if_django_imported(self):
        self.imported = None
        try:
            import django
            self.imported = True
        except:
            self.imported = False
        self.assertTrue(self.imported)
    # Simple test to see if you have imported psycopg2 correctly
    def test_if_psycopg2_imported(self):
        self.imported = None
        try:
            import psycopg2
            self.imported = True
        except:
            self.imported = False
        self.assertTrue(self.imported)
    def test_if_virtualenv_imported(self):
        self.imported = None
        try:
            import virtualenv
            self.imported = True
        except:
            self.imported = False
        self.assertTrue(self.imported)
    def test_if_bs4_imported(self):
        self.imported = None
        try:
            import bs4
            self.imported = True
        except:
            self.imported = False
        self.assertTrue(self.imported)


alltests = unittest.TestSuite()
alltests.addTest(unittest.makeSuite(RetrieveFromCanvasTest))
alltests.addTest(unittest.makeSuite(WebsiteDependencyTest))
results = unittest.TextTestRunner(verbosity=2).run(alltests)
