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
        self.WelcomeSentenceMemory = "Hola XX, \\pau=400\\ mi nombre es Nano. \\pau=500\\ Te estaré acompañando en las terapias. \\pau=500\\ Estoy aqui para cuidar tus signos y ayudarte a mejorar en tu rehabilitación."
        #Announce sentence
        self.sentenceAnnounce = "Hoy, vamos a iniciar con una velocidad de XX millas por hora con una inclinación de YY"
        self.sentenceChange = "To complete"
        self.sentenceStart = "To complete"

        #Sentences used for feedbacks
        self.sentencesEarlyMotivation = ["\\bound=S\\ Animo! Apenas estamos empezando","Vamos a empezar bien hoy","Empieza caminando despacio"]
        self.sentencesEarlyMotivationMemory = ["\\bound=S\\ Animo, \\pau=200\\ XX! Apenas estamos empezando","Vamos a empezar bien hoy, \\pau=200\\ XX","Empieza caminando despacio, \\pau=200\\ XX"]
        self.earlyMotivationProvided = []
        
        self.sentencesMidMotivation = ["\\bound=S\\ Vamos! Puedes hacerlo","Anímate","Estás haciéndolo bien","Estoy seguro que puedes hacerlo","Continúa esforzándote!","Que bien lo \\emph=200\\ estás haciendo","Sigue \\bound=S\\ así!","Estás progresando!","Hoy lo estás haciendo mejor","No olvides respirar!","Sé que puedes hacerlo!","Excelente trabajo","Has mejorado"]
        self.sentencesMidMotivationMemory = ["\\bound=S\\ Vamos, \\pau=200\\ XX! Puedes hacerlo","Anímate, \\pau=200\\ XX","Estás haciéndolo bien, \\pau=200\\ XX","Estoy seguro que puedes hacerlo, \\pau=200\\ XX","Continúa esforzándote, \\pau=200\\ XX!","Que bien lo \\emph=200\\ estás haciendo, \\pau=200\\ XX","Sigue \\bound=S\\ así, \\pau=200\\ XX!","Estás progresando, \\pau=200\\ XX!","Hoy lo estás haciendo mejor, \\pau=200\\ XX","No olvides respirar, \\pau=200\\ XX!","Sé que puedes hacerlo, \\pau=200\\ XX!","Excelente trabajo, \\pau=200\\ XX","Has mejorado, \\pau=200\\ XX"]
        self.midMotivationProvided = []
        
        self.sentencesLateMotivation = ["Falta poco","Ya casi terminamos","Solo faltan algunos minutos","Puedes hacerlo","Que bien lo has hecho","¡Ánimo!","Lo estás haciendo muy bien","Te veo mejor "]
        self.sentencesLateMotivationMemory = ["Falta poco, \\pau=200\\ XX","Ya casi terminamos, \\pau=200\\ XX","Solo faltan algunos minutos, \\pau=200\\ XX","Puedes hacerlo, \\pau=200\\ XX","Que bien lo has hecho, \\pau=200\\ XX","¡Ánimo, \\pau=200\\ XX!","Lo estás haciendo muy bien, \\pau=200\\ XX","Te veo mejor, \\pau=200\\ XX"]
        self.lateMotivationProvided = []
        #sentnece for cooldown
        self.cooldownSentence = "Has terminado, ahora puedes seguir con el enfriamiento"

        #Sentences for alert
        self.sentenceAlertHR = "Tu frecuencia cardiaca es muy alta, voy a llamar al doctor"
        self.sentenceAlertHRMemory = "Tu frecuencia cardiaca es muy alta, \\pau=100\\ XX. Voy a llamar al doctor"
        self.sentenceAlertBP = "Tu presión cardiaca es muy alta, voy a llamar al doctor"

        self.sentencePain = "^start(animations/Stand/Gestures/Hey_1) \\bound=S\\ \\emph=200\\ Doctora, el paciente tiene dolor. \\pau=500\\ puede venir por favor ^wait(animations/Stand/Gestures/Hey_1)"
        self.sentenceDizziness = "^start(animations/Stand/Gestures/Hey_1) \\bound=S\\ \\emph=200\\ Doctora, el paciente está mareado. \\pau=500\\ puede venir por favor ^wait(animations/Stand/Gestures/Hey_1)"
        self.sentenceFatigue = "^start(animations/Stand/Gestures/Hey_1) \\bound=S\\ \\emph=200\\ Doctora, el paciente se siente demasiado cansado. \\pau=500\\ puede venir por favor ^wait(animations/Stand/Gestures/Hey_1)"

        #Sentences for Borg Scale
        self.sentenceBorgInitial = ["¿Según esta escala, qué tan cansado te sientes?","¿Mira la pantalla, que cansancio tienes?","¿Puedes completar la escala de cansancio?","¿Según esta escala, qué tan cansado estás?","¿Cómo te sientes? Responde según la escala","¿Cuál es tu nivel de cansancio?","¿Según esta escala, como te sientes?","¿Estás cansado?","¿Según esta escala, que cansancio tienes?","¿Según esta escala, cómo te sientes?"]
        self.sentenceBorgInitialMemory = ["¿XX, \\pau=400\\ Según esta escala, qué tan cansado te sientes?","¿XX, \\pau=400\\ Mira la pantalla, que cansancio tienes?","¿XX, \\pau=400\\ puedes completar la escala de cansancio?","¿Según esta escala, qué tan cansado estás, \\pau=200\\ XX ?","¿Cómo te sientes, \\pau=400\\ XX? Responde según la escala","¿XX, \\pau=400\\ cuál es tu nivel de cansancio?","¿XX, \\pau=400\\ según esta escala, como te sientes?","¿XX, \\pau=400\\ estás cansado?","¿XX, \\pau=400\\ según esta escala, que cansancio tienes?","¿XX, \\pau=400\\ según esta escala, cómo te sientes?"]
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
        self.sentenceRequestLookForwardMemory = ["XX, \\pau=200\\ Mira al frente","Pon la vista al frente, \\pau=200\\ XX "," \\pau=200\\Recuerda mirar al frente, \\pau=200\\ XX","No mires a tus pies, \\pau=200\\ XX","Levanta la cabeza, \\pau=200\\ XX","Continua mirando al frente, \\pau=200\\ XX"]
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

        # Behavior to heart rate alert with the doctor

        self.clinicalSatffBehavior = ['call_staff-2840e1/behavior_1', 'call_staff2-0ac685/behavior_1','call_staff3-d6db9c/behavior_1']

        print "load dialogs finished"

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

    def get_motivation_memory_sentence(self):
        timeElapsed = self.get_therapy_time()

        if timeElapsed < self.earlyThreshold:
            i = random.randint(0, len(self.sentencesEarlyMotivationMemory) - 1)
            return self.sentencesEarlyMotivationMemory[i]
        elif timeElapsed < self.midThreshold:
            i = random.randint(0, len(self.sentencesMidMotivationMemory) - 1)
            return self.sentencesMidMotivationMemory[i]
        else:
            i = random.randint(0, len(self.sentencesLateMotivationMemory) - 1)
            return self.sentencesLateMotivationMemory[i]


    #returns a random Call Staff sentence

    def get_CallStaff_sentence(self):

        i = random.randint(0, len(self.clinicalSatffBehavior) - 1)
        return self.clinicalSatffBehavior[i]

    #returns a random borg sentence
    def get_borg_sentence(self):
        #timeElapsed = self.get_therapy_time()
        i = random.randint(0, len(self.sentenceBorgInitial) - 1)
        return self.sentenceBorgInitial[i]
    def get_borg_memory_sentence(self):
        i = random.randint(0, len(self.sentenceBorgInitialMemory) - 1)
        return self.sentenceBorgInitialMemory[i]

    def get_posture_correction_sentence(self):
        i = random.randint(0, len(self.sentenceRequestLookForward) - 1)
        return self.sentenceRequestLookForward[i]

    def get_posture_correction_memory_sentence(self):
        i = random.randint(0, len(self.sentenceRequestLookForwardMemory) - 1)
        return self.sentenceRequestLookForwardMemory[i]
    #
    def get_borg_receive(self):
        i = random.randint(0, len(self.sentenceBorgResponseLow) - 1)
        return self.sentenceBorgResponseLow[i]

    def sentence_fine(self):

        return self.sentenceFine

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
