class EmailMessage :
    """Cette class représente ce qu'est un email"""

    def __init__(self,to,body,subject=None,cc=[],attachments=[]):
        self.to = to
        self.body = body 
        self.subject = subject 
        self.cc = cc
        self.attachments = attachments

        def __str__(self) :
            return "To :" + self.to + "| Subject :" + self.subject  
        
        def __repr__(self) :
            return f"EmailMessage({self.to},{self.body},{self.subject},{self.cc},{self.attachments})"
        

class TextEmail(EmailMessage) :
    def __init__(self, to, body, subject=None, cc=[], attachments=[]):
        super().__init__(to, body, subject, cc, attachments) 

    def build_body(self) :
        return self.body