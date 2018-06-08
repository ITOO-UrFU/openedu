from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import django_filters
import graphene

from .models import PersonalData as PersonalDataModel
from .models import Program as ProgramModel


class Program(DjangoObjectType):
    class Meta:
        model = ProgramModel


class PersonalData(DjangoObjectType):
    class Meta:
        model = PersonalDataModel

    fio = graphene.Field(graphene.String)
    grades = graphene.Field(graphene.String)

    def resolve_fio(instance, info, **kwargs):
        return instance.fio()

    def resolve_grades(instance, info, **kwargs):
        return instance.get_grades()


class Query(graphene.ObjectType):
    pdata = graphene.List(PersonalData, active=graphene.Boolean(), start=graphene.Int())

    programs = graphene.List(Program, id=graphene.Int(), course_id=graphene.String(), active=graphene.Boolean())

    unique_programs = graphene.List(graphene.String)

    def resolve_programs(self, info, **kwargs):
        id = kwargs.get('id')
        active = kwargs.get('active')
        course_id = kwargs.get('course_id')

        if id is not None:
            return ProgramModel.objects.filter(pk=id)
        if course_id is not None:
            return ProgramModel.objects.filter(course_id=course_id)
        if active is not None:
            return ProgramModel.objects.filter(active=active)
        return ProgramModel.objects.all()

    def resolve_unique_programs(self, info, **kwargs):

        return ProgramModel.objects.order_by().distinct().values_list('course_id', flat=True)

    def resolve_pdata(self, info, **kwargs):
        active = kwargs.get('active')
        start = kwargs.get('start')

        if active is not None:
            return PersonalDataModel.objects.filter(program__active=active)
        elif start is not None:
            return PersonalDataModel.objects.filter(program__start=start)
        else:
            return PersonalDataModel.objects.all()  # filter(in_quote=False, paid=False)


schema = graphene.Schema(query=Query)
