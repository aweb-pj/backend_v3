from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import copy
import json
# Create your tests here.


class MyTests(APITestCase):

    def setUp(self):
        pass

    def Register(self):
        url = '/register'
        # test teacher register
        data = {
            'id':'1234567',
            'password':'1234567',
            'role':'TEACHER',
            'name':'FirstTeacher'
        }
        response = self.client.post(url,data=data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        # test duplicate id
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        # test student register
        data = {
            'id': '12345678',
            'password': '12345678',
            'role': 'STUDENT',
            'name': 'FirstStudent'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def LoginAsTeacher(self):
        url = '/login'
        # test successful login
        data = {
            'id': '1234567',
            'password': '1234567'
        }
        response = self.client.post(url,data=data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        result_correct_data = {
            'id':'1234567',
            'role':'TEACHER',
            'name':'FirstTeacher'
        }
        self.assertEqual(response.data,result_correct_data)
        # test login failure
        data['id'] = '000'
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def LoginAsStudent(self):
        url = '/login'
        # test successful login
        data = {
            'id': '12345678',
            'password': '12345678'
        }
        response = self.client.post(url,data=data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        result_correct_data = {
            'id':'12345678',
            'role':'STUDENT',
            'name':'FirstStudent'
        }
        self.assertEqual(response.data,result_correct_data)
        # test login failure
        data['id'] = '000'
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def Logout(self):
        url = '/logout'
        response = self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_register_login_logout(self):
        self.Register()
        self.LoginAsStudent()
        self.LoginAsTeacher()
        self.Logout()

    def test_get_set_tree(self):
        self.Register()
        url = '/tree'

        # test get without login
        # response = self.client.get(url)
        # self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

        # test get without a tree
        self.LoginAsStudent()
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)
        self.Logout()

        # test set tree
        self.LoginAsTeacher()
        data = {
            # anything will do
            "msg":"klsjdfl",
            "aaa":"lsjgklasjg",
            "dkl":"lkadjflksdj"
        }
        response = self.client.post(url,data=data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        # test get tree
        response = self.client.get(url)
        self.assertEqual(response.data,data)
        self.Logout()

    def test_homework(self):

        self.Register()
        url = '/node/1/homework'
        homework = {
            "published":False,
            "questions":[
                {
                    "type":"TEXT",
                    "question":"who is jiangzhuoli?",
                    "A": None,
                    "B": None,
                    "C": None,
                    "D": None,
                    "correct_answer": None
                },
                {
                    "type":"CHOICE",
                    "question":"what is zhuolijiang like?",
                    "A":"tall",
                    "B":"rich",
                    "C":"handsome",
                    "D":"king of pudong district",
                    "correct_answer":"ABCD"
                },
                {
                    "type": "TEXT",
                    "question": "who is god tao?",
                    "A": None,
                    "B": None,
                    "C": None,
                    "D": None,
                    "correct_answer": None
                },
                {
                    "type": "CHOICE",
                    "question": "what is god tao like?",
                    "A": "tall",
                    "B": "rich",
                    "C": "handsome",
                    "D": "king of jiangsu province",
                    "correct_answer": "ABCD"
                },
            ]
        }

        # test set homework
        self.LoginAsTeacher()
        response = self.client.post(url,data=homework)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test get homework
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        result_homework = json.loads(json.dumps(homework))
        # response homework data has order and id
        order = 0
        for question in result_homework['questions']:
            question['order'] = order
            order += 1
        for question in response.data['questions']:
            question.pop('id', None)
        result_homework['node_id'] = 1
        self.assertEqual(response.data,result_homework)

    def CreateHomework(self,node_id):
        self.LoginAsTeacher()
        homework = {
            "node_id":node_id,
            "published": False,
            "questions": [
                {
                    "type": "TEXT",
                    "question": "who is jiangzhuoli?",
                    "A": None,
                    "B": None,
                    "C": None,
                    "D": None,
                    "correct_answer": None
                },
                {
                    "type": "CHOICE",
                    "question": "what is zhuolijiang like?",
                    "A": "tall",
                    "B": "rich",
                    "C": "handsome",
                    "D": "king of pudong district",
                    "correct_answer": "ABCD"
                },
                {
                    "type": "TEXT",
                    "question": "who is god tao?",
                    "A": None,
                    "B": None,
                    "C": None,
                    "D": None,
                    "correct_answer": None
                },
                {
                    "type": "CHOICE",
                    "question": "what is god tao like?",
                    "A": "tall",
                    "B": "rich",
                    "C": "handsome",
                    "D": "king of jiangsu province",
                    "correct_answer": "ABCD"
                },
            ]
        }
        url = '/node/{}/homework'.format(node_id)
        response = self.client.post(url,data=homework)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.Logout()

    def test_homework_answer(self):
        self.Register()
        url = '/node/1/homeworkanswer'
        homework_answer = {
            "answers": [
                {
                    "answer": "aaaaaaaaaaaaa",
                    "question": 1
                },
                {
                    "answer": "ccccccccccccccc",
                    "question": 2
                }
            ]
        }
        expected_result = {
            "answers": [
                {
                    "answer": "aaaaaaaaaaaaa",
                    "question": 1
                },
                {
                    "answer": "ccccccccccccccc",
                    "question": 2
                }
            ]
        }
        # create a homework for testing
        self.CreateHomework(1)
        # test set homework answer
        self.LoginAsStudent()
        response = self.client.post(url, homework_answer)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        # test get homework answer
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,expected_result)

    def test_material(self):
        pass

    def CreateAnswer(self):
        self.LoginAsStudent()
        url = '/node/1/homeworkanswer'
        student = {
            'id': '12345678',
            'password': '12345678',
            'role': 'STUDENT',
            'name': 'FirstStudent'
        }
        homework_answer = {
            "student":student,
            "answers": [
                {
                    "answer": "ABCD",
                    "question": 1
                },
                {
                    "answer": "ABCD",
                    "question": 2
                },
                {
                    "answer": "ABCD",
                    "question": 3
                },
                {
                    "answer": "ABCD",
                    "question": 4
                }
            ]
        }
        self.client.post(url, homework_answer)
        self.Logout()

    def init(self):
        self.Register()
        self.CreateHomework(1)
        self.CreateAnswer()
        self.LoginAsStudent()

    def test_statistics_check_qusetion(self):
        self.init()
        url = '/question/check'
        post_data = {
            "student_id":12345678,
            "question_id":2
        }
        expected_result = {
            "result":'right'
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_result)
        post_data = {
            "student_id": 12345678,
            "question_id": 1
        }
        expected_result = {
            "result": 'wrong'
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_result)

    def test_statistics_all(self):
        self.init()
        url = '/statistics/all'
        post_data = {
            "node_id":1
        }
        expected_result = {
            'accuracy': 0.5
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_result)

    def test_statistics_query(self):
        self.init()

