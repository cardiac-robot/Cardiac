import gui.EndQuestionWin as EndQuestionWin


class EndQuestionPlugin(object):
    def __init__(self, ProjectHandler, DataHandler):
        self.PH = ProjectHandler
        self.DB = DataHandler
        self.View = EndQuestionWin.EndQuestionWin(ProjectHandler = self.PH)
        self.set_signals()

    def set_signals(self):
        self.View.onData.connect(self.get_data)

    def get_data(self):
        #load event
        self.DB.General.SM.load_event(t = "Questions", c= "None", v = self.View.data)


    def LaunchView(self):
        self.View.show()
        print  "launch EndQuestionWin"

    def shutdown(self):
        self.View.close()
