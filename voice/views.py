#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.conf import settings
import speech_recognition as sr
import time
import librosa
import soundfile as sf
from gtts import gTTS
import os
# Deprecated library
#from bardapi import Bard

def callback_s2t_google_srv(nombre):
	r = sr.Recognizer()
	audioFile = sr.AudioFile("media/"+nombre+".wav")
	with audioFile as source:
		audio = r.record(source)  # read the entire audio file
	google = "None"
	try:
		google = r.recognize_google(audio, language="es")
		google = google.lower()
		print("Google Entendio:"+google)
		#answer = chatbot.ask(google)['content'].replace("*","").replace("_","").replace("-","")
		answer = google
		print("Bard Respondio:"+answer)
		if "Google Bard encountered an error" in answer:
			return ""
		gThing = gTTS(answer,lang="es",slow=False)
		gThing.save("media/"+nombre+".mp3")
		if os.path.isfile("media/"+nombre+".wav"):
			os.remove("media/"+nombre+".wav")
		return answer.lower()
	except sr.UnknownValueError:
		print("No entendio nada google")
	except sr.RequestError as e:
		print("Otro error raro")
	return ""

PSID = "eQhKDXPHzws3V4nsXWQy515gsSCkqeAdhC_gwj2aNDbO2l1X4-ac7kq0ajAAmpPgwALcTQ."
PSIDTS = "sidts-CjEBPVxjSixUzWuGzMj9MWHbNY2rvIaME1bAxIyC5IlKJNzO9Z1PEahXo8-6Dd0SmCoAEAA"
#DEPRECATED LIBRARY
#chatbot = Bard(PSID,PSIDTS)
chatbot = None
#CONTEXTO
#answer = chatbot.ask("Eres un sistema de busqueda de servicios en la web, para siguientes peticiones respondeme con los datos de proveedores de dichos servicios, si no puedes encontrar dichos datos, inventalos. Necesitamos numeros de telefono, nombre del proveedor, ubicacion del proveedor, precios y calificacion. No mandes imagenes porfavor. Muchas gracias! Por favor manten tus respuestas cortas.")
# Create your views here.
def home(request):
    return render(request,"voice/index.html")

@csrf_exempt
def sendAudio(request):
	print(request)
	nombre = request.GET['nombre']
	partes = nombre.split("-")
	if int(partes[1])>0:
		if os.path.isfile("media/"+partes[0]+"-"+str(int(partes[1])-1)+".mp3"):
			os.remove("media/"+partes[0]+"-"+str(int(partes[1])-1)+".mp3")
	audio_file = request.FILES['audio']
	with open("media/"+nombre+".wav", 'wb') as destination:
		for chunk in audio_file.chunks():
			destination.write(chunk)
	x, _ = librosa.load("media/"+nombre+".wav",sr=16000)
	sf.write("media/"+nombre+".wav",x,16000)
	respuesta = callback_s2t_google_srv(nombre)
	if respuesta is None:
		return HttpResponse("No entendi, repitelo porfavor", status=204)
	return HttpResponse(respuesta.replace("*",""))