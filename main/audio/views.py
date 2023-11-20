from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .serializers import AudioFileSerializer
from rest_framework.response import Response
from rest_framework import status
from pydub import AudioSegment
from django.core.files import File
from .models import AudioFile, Text
import speech_recognition as sr
import os


class AudioFileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        serializer = AudioFileSerializer(data=request.data)

        if serializer.is_valid():
            uploaded_file = serializer.validated_data['audio']

            audio = AudioSegment.from_file(uploaded_file)
            wav_file = audio.export(format="wav")

            wav_file_name = os.path.splitext(uploaded_file.name)[0] + ".wav"
            wav_file_django = File(wav_file, name=wav_file_name)

            audio_model = AudioFile(audio=wav_file_django)
            audio_model.save()

            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_model.audio.path) as source:
                audio_data = recognizer.record(source)
                try:
                    recognized_text = recognizer.recognize_google(audio_data, language="ru-RU")
                except sr.UnknownValueError:
                    recognized_text = "Не могу разобрать вопрос!"
                except sr.RequestError as e:
                    recognized_text = f"Could not request results: {e}"

            response_data = {
                "recognized_text": recognized_text,
                "uploaded_file_url": audio_model.audio.url,
            }

            return Response(response_data, status=201)

        return Response(serializer.errors, status=400)


class TextUploadView(APIView):
    def post(self, request):
        text = request.data.get('text', '')
        text_instance = Text(content=text)
        text_instance.save()

        return Response({'Text': {text}}, status=status.HTTP_201_CREATED)