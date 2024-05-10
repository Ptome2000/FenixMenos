from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, viewsets
from Vitae.models import Curso, Aluno, Genero


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['codigo', 'designacao', 'creditos', 'descricao']


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserAlunoSerializer(serializers.ModelSerializer):
    curso = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all())
    foto = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ('foto', 'curso')

    def create(self, validated_data):
        curso = validated_data.pop('curso')
        foto = validated_data.pop('foto', None)
        user = User.objects.create_user(**validated_data)
        Aluno.objects.create(user=user, curso=curso, foto=foto)
        return user
