from django.db import models
import uuid
import os


def get_file_path(instance, filename):
    base = os.path.basename(filename)
    filename,ext = os.path.splitext(base)
    # ext = filename.split('.')[-1]
    filename = "%s.%s" % (str(uuid.uuid4())+filename, ext)
    return os.path.join('materials', filename)


class User(models.Model):
    id = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    USER_ROLES = (
        ('STUDENT','Student'),
        ('TEACHER','Teacher'),
    )
    role = models.CharField(max_length=7,choices=USER_ROLES)

    def __str__(self):
        return self.name


class NodeHomework(models.Model):
    id = models.AutoField(primary_key=True)
    node_id = models.IntegerField()
    published = models.BooleanField(default=False)

    def __str__(self):
        return 'node:'+str(self.node_id)+'pk:'+str(self.id)


class NodeMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    node_id = models.IntegerField()

    def __str__(self):
        return 'node:'+str(self.node_id)+'pk:'+str(self.id)


class Material(models.Model):
    id = models.AutoField(primary_key=True)
    node_material = models.ForeignKey('NodeMaterial',on_delete=models.CASCADE,related_name='materials')
    # material_name = models.CharField(max_length=100)
    material_file = models.FileField(upload_to=get_file_path)

    def __str__(self):
        return 'selfpk:'+str(self.id)


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    node_homework = models.ForeignKey('NodeHomework',on_delete=models.CASCADE,related_name='questions')
    QUESTION_TYPES = (
        ('TEXT', 'TextQuestion'),
        ('CHOICE', 'ChoiceQuestion'),
    )
    type = models.CharField(max_length=6, choices=QUESTION_TYPES)
    question = models.CharField(max_length=100)
    order = models.IntegerField()
    # for a choice question
    A = models.CharField(max_length=100,null=True,blank=True)
    B = models.CharField(max_length=100, null=True,blank=True)
    C = models.CharField(max_length=100, null=True,blank=True)
    D = models.CharField(max_length=100, null=True,blank=True)
    correct_answer = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.question


class HomeworkAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey('User',on_delete=models.CASCADE)
    node_homework = models.ForeignKey('NodeHomework',on_delete=models.CASCADE)

    def __str__(self):
        return 'pk:'+str(self.id)


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey('Question',on_delete=models.CASCADE)
    homework_answer = models.ForeignKey('HomeworkAnswer',on_delete=models.CASCADE,related_name='answers')
    answer = models.TextField()

    def __str__(self):
        return self.answer


class Tree(models.Model):
    id = models.AutoField(primary_key=True)
    tree = models.TextField()







