# -*- coding: utf-8 -*-
import time
import random

class Dialogs(object):
    def __init__(self):
        self.initTime = time.time()
        self.earlyThreshold = 300 # 5 first minutes
        self.midThreshold = 700 #10 mins
        self.lateThreshold = 900 # 15 mins

    def load_dialogs(self):
        print("look in the database to load available dialogs")
        #self.WelcomeSentence = "Hola, \\pau=500\\ mi nombre es Jansel, y hoy voy a ayudarte en tu rehabilitación"
        #self.ByeSentence = "Ha sido un placer ayudarte en la sesión, espero verte pronto"

        #First introduction
        self.WelcomeSentence = "Hola, \\pau=400\\ mi nombre es Nano. \\pau=500\\ Te estaré acompañando en las terapias. \\pau=500\\ Estoy aqui para cuidar tus signos y ayudarte a mejorar en tu rehabilitación."
        #Announce sentence
        self.sentenceAnnounce = "Hoy, vamos a iniciar con una velocidad de XX millas por hora con una inclinación de YY"
        self.sentenceChange = "To complete"
        self.sentenceStart = "To complete"

        #Sentences used for feedbacks
        self.sentencesEarlyMotivation = ["\\bound=S\\ Animo! Apenas estamos empezando","Vamos a empezar bien hoy","Empieza caminando despacio"]
        self.earlyMotivationProvided = []
        self.sentencesMidMotivation = ["\\bound=S\\ Vamos! Puedes hacerlo","Anímate","Estás haciéndolo bien","Estoy seguro que puedes hacerlo","Continúa esforzándote!","Que bien lo \\emph=200\\ estás haciendo","Sigue \\bound=S\\ así!","Estás progresando!","Hoy lo estás haciendo mejor","No olvides respirar!","Sé que puedes hacerlo!","Excelente trabajo","Has mejorado"]
        self.midMotivationProvided = []
        self.sentencesLateMotivation = ["Falta poco","Ya casi terminamos","Solo faltan algunos minutos","Puedes hacerlo","Que bien lo has hecho","¡Ánimo!","Lo estás haciendo muy bien","Te veo mejor "]
        self.lateMotivationProvided = []
        #sentnece for cooldown
        self.cooldownSentence = "Has terminado, ahora puedes seguir con el enfriamiento"
        #Sentences for alert
        self.sentenceAlertHR = "Tu frecuencia cardiaca es muy alta, voy a llamar al doctor"
        self.sentenceAlertBP = "Tu presión cardiaca es muy alta, voy a llamar al doctor"

        self.sentencePain = "^start(animations/Stand/Gestures/Hey_1) \\bound=S\\ \\emph=200\\ Doctora, el paciente tiene dolor. \\pau=500\\ puede venir por favor ^wait(animations/Stand/Gestures/Hey_1)"
        self.sentenceDizziness = "^start(animations/Stand/Gestures/Hey_1) \\bound=S\\ \\emph=200\\ Doctora, el paciente está mareado. \\pau=500\\ puede venir por favor ^wait(animations/Stand/Gestures/Hey_1)"
        self.sentenceFatigue = "^start(animations/Stand/Gestures/Hey_1) \\bound=S\\ \\emph=200\\ Doctora, el paciente se siente demasiado cansado. \\pau=500\\ puede venir por favor ^wait(animations/Stand/Gestures/Hey_1)"

        #Sentences for Borg Scale
        self.sentenceBorgInitial = ["¿Según esta escala, qué tan cansado te sientes?","¿Mira la pantalla, que cansancio tienes?","¿Puedes completar la escala de cansancio?","¿Según esta escala, qué tan cansado estás?","¿Cómo te sientes? Responde según la escala","¿Cuál es tu nivel de cansancio?","¿Según esta escala, como te sientes?","¿Estás cansado?","¿Según esta escala, que cansancio tienes?","¿Según esta escala, cómo te sientes?"]
        self.borgInitialProvided = []
        self.sentenceBorgSecond = "Dijiste que estás muy cansado pero tu frecuencia cardiaca se encuentra baja, ¿estás seguro que estás muy cansado?"
        self.sentenceBorgResponseLow = ["Gracias!!"]
        self.borgResponseLowProvided = []

        #Sentences for warning and call for help
        self.sentenceCallHelp = "Listo, voy a llamar el doctor"
        self.sentenceCallNurse = "^start(animations/Stand/Gestures/Hey_1) \\bound=S\\ \\emph=200\\ Doctora, puede venir por favor ^wait(animations/Stand/Gestures/Hey_1)"
        self.sentenceFine = "Me alegra que todo esté bien."

        #Sentences for additional requests and thanks
        self.sentenceRequestLookForward = ["Mira al frente","Pon la vista al frente","Recuerda mirar al frente","No mires a tus pies","Levanta la cabeza","Continua mirando al frente"]
        self.requestLookForwardProvided = []
        self.sentenceLookedForward = ["Bien hecho","Muy bien","Continua así","Bien"]
        self.lookedForwardProvided = []
        self.sentenceRequestCloser = ["Acércate adelante","Camina un poco hacia adelante","Cuidado! Te encuentras muy atrás","Acércate a la caminadora"]
        self.requestCloserProvided = []
        self.sentenceWarning = "Parece que estas empezando a estar cansado, todo está bien?"
        self.sentenceCameCloser = ["Bien hecho","Muy bien","Bien"]
        self.cameCloserProvided = []
        self.sentenceThanksDoctor = "Gracias doctora"

        #Sentences for asking bps
        self.askForBpsBegin = "Antes de comenzar,\\pau=200\\ ingresa tu presión sanguínea, por favor"
        self.askForBpsEnd = "Para finalizar, \\pau=200\\ ingresa tu presión sanguínea, por favor"
        #Sentences for feedback and motivation
        self.askForFeedback = "¿Según esta escala, Qué tan motivado te sientes para regresar de nuevo?.\\pau=800\\ Cómo te sentiste hoy? \\pau=200\\ Espero que bien!!."

        #Sentences for conclusions
        self.sentencesGoodSession = ["Excelente trabajo hoy, me alegra haberte acompañado","Bien hecho, espero haberte ayudado hoy","Mereces un aplauso, buen trabajo"]
        self.goodSessionProvided = []
        self.sentencesBadSession = "La sesión de hoy fue un poco intesa, estoy seguro que estará mejor la próxima vez."
        self.sentenceRateSession = ["Cómo te pareció la sesión hoy?","Cómo te sentiste hoy?","Que tal te pareció la sesión?","Como te fue hoy?"]
        self.rateSessionProvided = []
        #additional indications
        self.CloseInstructionSentence = "Para finalizar, \\pau=50\\ pulsa el botón rojo, en la esquina superior derecha, \\pau=200\\ por favor"
        #say bye sentences
        self.ByeSentence = 'Eso ha sido todo por hoy!! \\pau=20\\ No olvides ingresar la presión arterial y responder las preguntas al final! '


    #returns a random motivation sentences depending on the therapy time
    def get_motivation_sentence(self):
        timeElapsed = self.get_therapy_time()

        if timeElapsed < self.earlyThreshold:
            i = random.randint(0, len(self.sentencesEarlyMotivation) - 1)
            return self.sentencesEarlyMotivation[i]
        elif timeElapsed < self.midThreshold:
            i = random.randint(0, len(self.sentencesMidMotivation) - 1)
            return self.sentencesMidMotivation[i]
        else:
            i = random.randint(0, len(self.sentencesLateMotivation) - 1)
            return self.sentencesLateMotivation[i]

    #returns a random borg sentence
    def get_borg_sentence(self):
        #timeElapsed = self.get_therapy_time()
        i = random.randint(0, len(self.sentenceBorgInitial) - 1)
        return self.sentenceBorgInitial[i]

    #
    def get_borg_receive(self):
        i = random.randint(0, len(self.sentenceBorgResponseLow) - 1)
        return self.sentenceBorgResponseLow[i]

    #
    def ask_borg_again(self):
        return self.sentenceBorgSecond
    #return the amount of seconds transcurred during the session
    def get_therapy_time(self):
        currentTime = time.time()
        timeElapsed =  currentTime - self.initTime
        return timeElapsed

if __name__ == '__main__':
    s = Dialogs()
    s.load_dialogs()

    time.sleep(1)
    print s.get_motivation_sentence()
    print s.get_borg_sentence()
    time.sleep(5)
    print s.get_motivation_sentence()
    print s.get_borg_sentence()
    time.sleep(5)
    print s.get_motivation_sentence()
    print s.get_borg_sentence()
