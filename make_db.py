from condition_monitor.models import *
import random
import datetime
import time

class DBGenerator():
    def __init__(self):
        self.db = DBConnection()
        self.rooms = []
        self.users = []

    def cleanDB(self):
        self.db._engine.drop_all()
        self.db._engine.create_all()

    def genDB(self):
        self.genUserRoles()
        self.genUsers()
        self.genRooms()
        self.genAccesses()
        self.genMeasurements()

    def genUserRoles(self):
        self.db.session.add(UserRole(id=1, name=UserRole.BASIC))
        self.db.session.add(UserRole(id=2, name=UserRole.ADMIN))
        self.db.flush()


    def genUsers(self):
        usernames = ["Bartek", "Ola", "Karolina", "Kasia", "Natalia", "Krzysztof", "Jan"]
        admin = User(username="Kacper", email="Kacper@gmail.com", password_hash="$2b$12$S7zEm.HCaGlrMyy5uJDpF.Zp45TOyGOKZQm6Je/6dLdCSV5R5il3e", role_id = 2)
        self.db.addUser(admin)
        self.users.append(admin)
        for user in usernames:
            user = User(username=user, email=user+"@gmail.com", password_hash="$2b$12$S7zEm.HCaGlrMyy5uJDpF.Zp45TOyGOKZQm6Je/6dLdCSV5R5il3e", role_id = 1)
            self.users.append(user)
            self.db.addUser(user)
        self.db.flush()

    def genRooms(self):
        room_letters = ["A","B"]
        floors = 6
        for letter in room_letters:
            for floor in range(floors):
                for d in [1,2,3,4,5,7]:
                    for j in [1,2,3,4]:
                        room = Room(name=letter+str(floor+1)+str(d)+str(j))
                        self.rooms.append(room)
                        self.db.addRoom(room)
        self.db.flush()

    def genAccesses(self):
        for user in self.users:
            selected_ids = [-1]
            for i in range(random.randint(10, 40)):
                randomid = -1
                while randomid in selected_ids:
                    randomid = self.rooms[random.randint(0, len(self.rooms)-1)].id
                selected_ids.append(randomid)
                self.db.session.add(Access(userid=user.id, roomid = randomid))
        self.db.flush()

    def genMeasurements(self):
        time_now = datetime.datetime.now()
        time_start = time_now - datetime.timedelta(days=3)
        time_curr = time_start
        for room in self.rooms:
            time_curr = time_start
            while time_curr < time_now:
                self.db.session.add(Measurement(roomid = room.id, temperature = int(random.gauss(15,10)), humidity = int(random.gauss(50,15)), timestamp = time_curr))
                time_curr += datetime.timedelta(minutes=80)
        self.db.flush()

if __name__ == "__main__":
    generator = DBGenerator()
    generator.cleanDB()
    generator.genDB()