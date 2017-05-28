from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import *
from rest_framework.response import Response
from rest_framework import status
from elearning.serializers import *
from rest_framework.views import APIView
import json
import os
# Create your views here.


def check_login(request,roles):
    session_data = request.session
    if 'role' not in session_data or 'id' not in session_data:
        return False
    role = session_data['role']
    if role not in roles:
        return False
    return True


@api_view(['POST'])
def login(request):
    input_data = request.data
    login_id = input_data['id']
    login_password = input_data['password']
    users = User.objects.filter(id=login_id)
    if users.exists():
        user = users[0]
        if user.password == login_password:
            request.session['role'] = user.role
            request.session['id'] = user.id
            serializer = UserSerializer(instance=user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def logout(request):
    try:
        del request.session['id']
        del request.session['role']
    except KeyError:
        pass
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    input_data = request.data
    if 'id' in input_data and 'password' in input_data and 'role' in input_data and 'name' in input_data:
        if input_data['role'] in ['TEACHER','STUDENT']:
            existing_user = User.objects.filter(id=input_data['id'])
            if existing_user.exists():
                return Response(status=status.HTTP_409_CONFLICT)
            user = User(id=input_data['id'],password=input_data['password'],name=input_data['name'],role=input_data['role'])
            user.save()
            return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def tree(request):

    # roles = ['TEACHER','STUDENT']
    # if not check_login(request,roles):
    #     return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':

        trees = Tree.objects.all()
        if not trees.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
            # return Response(data={},status=status.)
        else:
            tree = trees[0]
            tree_str = tree.tree
            return Response(data=json.loads(tree_str), status=status.HTTP_200_OK)

    elif request.method == 'POST':

        # roles = ['TEACHER']
        # if not check_login(request, roles):
        #     return Response(status=status.HTTP_403_FORBIDDEN)

        input_data = json.dumps(request.data)
        trees = Tree.objects.all()
        if not trees.exists():
            tree = Tree(tree=input_data)
            tree.save()
        else:
            tree = trees[0]
            tree.tree = input_data
            tree.save()
        return Response(status=status.HTTP_200_OK)


class HomeworkAnswerView(APIView):

    def get(self,request,node_id):

        # roles = ['STUDENT']
        # if not check_login(request, roles):
        #     return Response(status=status.HTTP_403_FORBIDDEN)

        node_homework = NodeHomework.objects.get(node_id=node_id)
        if not node_homework:
            return Response(status=status.HTTP_404_NOT_FOUND)
        node_homeworkanswer = HomeworkAnswer.objects.get(node_homework=node_homework,student=request.session['id'])
        if not node_homeworkanswer:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = HomeworkAnswerSerializer(instance=node_homeworkanswer)
        result_data = serializer.data
        result_data.pop('student', None)
        result_data.pop('node_homework', None)
        return Response(result_data, status=status.HTTP_200_OK)

    def post(self,request,node_id):

        input_data = request.data
        input_data['node_id'] = str(node_id)

        # roles = ['STUDENT']
        # if not check_login(request, roles):
        #     return Response(status=status.HTTP_403_FORBIDDEN)

        node_homeworks = NodeHomework.objects.filter(node_id=node_id)
        if not node_homeworks.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        node_homework = node_homeworks[0]
        input_data['node_homework'] = node_homework.id
        input_data['student'] = request.session['id']
        serializer = HomeworkAnswerSerializer(data=input_data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class HomeworkView(APIView):
    def get(self,request,node_id):

        # roles = ['TEACHER', 'STUDENT']
        # if not check_login(request, roles):
        #     return Response(status=status.HTTP_403_FORBIDDEN)

        # node_homeworks = NodeHomework.objects.filter(node_id=node_id)
        # if not node_homeworks.exists():
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        # node_homework = node_homeworks[0]
        node_homework = NodeHomework.objects.get(node_id=node_id)
        if not node_homework:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = NodeHomeworkSerializer(instance=node_homework)
        result_data = serializer.data
        result_data['questions'] = sorted(result_data['questions'], key=lambda k: k['order'])
        return Response(result_data, status=status.HTTP_200_OK)

    def post(self,request,node_id):

        input_data = request.data
        input_data['node_id'] = str(node_id)

        # roles = ['TEACHER']
        # if not check_login(request, roles):
        #     return Response(status=status.HTTP_403_FORBIDDEN)

        node_homeworks = NodeHomework.objects.filter(node_id=node_id)
        if node_homeworks.exists():
            node_homeworks[0].delete()
        order = 0
        for question in input_data['questions']:
            question['order'] = order
            order = order + 1
        serializer = NodeHomeworkSerializer(data=input_data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_materials(request,node_id):

    # roles = ['TEACHER', 'STUDENT']
    # if not check_login(request, roles):
    #     return Response(status=status.HTTP_403_FORBIDDEN)

    node_material = NodeMaterial.objects.get(node_id=node_id)
    if not node_material:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = NodeMaterialSerializer(instance=node_material)
    return Response(serializer.data,status=status.HTTP_200_OK)


class MaterialFileUploadView(APIView):
    parser_classes = (FormParser,MultiPartParser)

    def post(self, request,node_id):

        # roles = ['TEACHER']
        # if not check_login(request, roles):
        #     return Response(status=status.HTTP_403_FORBIDDEN)

        file_name = None
        for key in request.FILES:
            file_name = key
        if not file_name:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        file_obj = request.FILES[file_name]
        node_materials = NodeMaterial.objects.filter(node_id=node_id)
        if not node_materials.exists():
            node_material = NodeMaterial(node_id=node_id)
        else:
            node_material = node_materials[0]
        node_material.save()
        material = Material(material_file=file_obj, node_material=node_material)
        material.save()
        return Response(status=status.HTTP_201_CREATED)


class MaterialFileDownloadView(APIView):

    def get(self,request,material_id,node_id):

        # roles = ['TEACHER', 'STUDENT']
        # if not check_login(request, roles):
        #     return Response(status=status.HTTP_403_FORBIDDEN)

        material = Material.objects.get(id=material_id)
        if material is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        response = HttpResponse(status=status.HTTP_200_OK)
        full_path = os.path.join('', str(material.material_file))
        base = os.path.basename(full_path)
        filename, file_extension = os.path.splitext(base)
        uuid_length = 36
        filename = filename[uuid_length:]
        response['Content-Disposition'] = 'attachment;filename=' + filename + file_extension
        if os.path.exists(full_path):
            response['Content-Length'] = os.path.getsize(full_path)
            content = open(full_path, 'rb').read()
            response.write(content)
            return response
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def statistics_all(self,request):
    input_data = request.data
    node_id = input_data['node_id']
    node_homeworks = NodeHomework.objects.filter(node_id = node_id)
    if node_homeworks is None:
        return Response(status.HTTP_400_BAD_REQUEST)

    node_homework = node_homeworks[0]
    questions = Question.objects.filter(node_homework = node_homework)
    correct_accuracy = 0
    if len(questions) == 0:
        accuracy = 0
    else:
        for question in questions:
            answers_all = Answer.objects.filter(question=question)
            if len(answers_all) == 0:
                correct_accuracy += 0
            else:
                answers_corrert = Answer.objects.filter(question=question, answer=question.correct_answer)
                correct_accuracy += len(answers_corrert) / len(answers_all)
        accuracy = correct_accuracy/len(questions)

    data = {
        'accuracy': accuracy
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def statistics_query(self,request):
    input_data = request.data
    question_id = input_data['question_id']
    questions = Question.objects.filter(id = question_id)
    if questions is None:
        return Response(status = status.HTTP_400_BAD_REQUEST)

    question = questions[0]

    answers_all = Answer.objects.filter(question = question)
    if len(answers_all) == 0:
        accuracy = 0
    else:
        answers_correct = Answer.objects.filter(question = question,answer = question.correct_answer)
        accuracy = len(answers_correct)/len(answers_all)
    data = {
        'accuracy': accuracy
    }
    return Response(data,status = status.HTTP_200_OK)

@api_view(['POST'])
def statistics_student_all(request):
    input_data = request.data
    student_id = input_data['student_id']
    students = User.objects.filter(id = student_id,role = 'STUDENT')
    if students is None:
        return Response(status = status.HTTP_400_BAD_REQUEST)

    student = students[0]
    homework_answers = HomeworkAnswer.objects.filter(student = student)
    correct = 0
    all = 0
    for homework_answer in homework_answers:
        answers = Answer.objects.filter(homework_answer = homework_answer)
        all += len(answers)
        for answer in answers:
            if answer.answer == answer.question.correct_answer:
                correct += 1
    if all == 0:
        accuracy = 0
    else:
        accuracy = correct/all

    data = {
        'accuracy':accuracy
    }
    return Response(data,status = status.HTTP_200_OK)

@api_view(['POST'])
def statistics_student_node_query(request):
    input_data = request.data
    student_id = input_data['student_id']
    node_id = input_data['node_id']

    students = User.objects.filter(id=student_id, role='STUDENT')
    if students is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    nodeHomeworks = NodeHomework.objects.filter(node_id = node_id)
    if nodeHomeworks is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    student = students[0]
    node_homework = nodeHomeworks[0]

    homework_answers = HomeworkAnswer.objects.filter(student=student,node_homework = node_homework)

    if len(homework_answers) == 0:
        accuracy = 0
    else:
        homework_answer = homework_answers[0]
        answers = Answer.objects.filter(homework_answer=homework_answer)
        all = len(answers)
        correct = 0
        for answer in answers:
            if answer.answer == answer.question.correct_answer:
                correct += 1
        if all == 0:
            accuracy = 0
        else:
            accuracy = correct/all

    data = {
        'accuracy':accuracy
    }
    return Response(data,status = status.HTTP_200_OK)

@api_view(['POST'])
def question_check(request):
    input_data = request.data
    student_id = input_data['student_id']
    question_id = input_data['question_id']

    students = User.objects.filter(id=student_id, role='STUDENT')
    if students is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    questions = Question.objects.filter(id=question_id)
    if questions is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    student = students[0]
    question = questions[0]
    answers = Answer.objects.filter(homework_answer__student = student,question = question)
    if answers is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    answer = answers[0]
    if answer.answer == question.correct_answer:
        result = 'right'
    else:
        result = 'wrong'

    data = {
        'result':result
    }
    return Response(data,status = status.HTTP_200_OK)