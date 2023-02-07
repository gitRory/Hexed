
#? work with closer to 0 being most important so can do burndown handling

class Trigger():
    """do a thing when a thing happens"""
    def __init__(self):
        self.M= self.Message()
    
    class Message():
        "context for triggers"
        def __init__(self):
            self.actions={
                0:'stop',
                1:'start',
                2:'default',
                3:'confirmed',
                4:'vaild',
                5:'reject',
                6:'repeat',
                7:"??",#*foobarr blah blah blah
                }
            
        def send_M(self,message,sender):
            for key, val in self.actions:
                if val == message:
                    return key
            return 2#default
    
        def receive_M(self,message):
            pass
        
    def 