class Client():
    def __init__(self, playerNumber):
        self.readyMessage = ''
        self.readyCode = ''
        self.playerNumber = playerNumber
        self.choice = ''
        self.connection = ''
        self.Board=None
        self.latestTargetPlayer = None
        self.isDeadMessage = None
        self.isDead = False