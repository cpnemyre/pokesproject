from system.core.model import Model
import re


EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
PASSWORD_REGEX = re.compile(r'^([^0-9]*|[^A-Z]*)$')
class WelcomeModel(Model):
    def __init__(self):
        super(WelcomeModel, self).__init__()


    def login(self, data):
        errors = []
        if len(data['email']) == 0 or not EMAIL_REGEX.match(data['email']):
            errors.append("Email is not valid")
        if len(data['password']) < 6:
            errors.append("Password must be more than 6 characters")
        if errors:
            return{"status" : False, "errors" : errors}
        else:
            query = "SELECT * FROM users WHERE email = :email"
            values = {'email' : data['email']}
            users = self.db.query_db(query,values)
            return {"status" : True, "user" : users[0]}

    def register(self,data):
        errors = []
        if len(data['name']) == 0:
            errors.append("Name is required")
        if len(data['alias']) == 0:
            errors.append("Alias is required")
        if len(data['email']) == 0:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(data['email']):
            errors.append("Email must be valid")
        if len(data['password']) < 6:
            errors.append("Password must be 6 characters or more")
        if data['password'] != data['confirm_password']:
            errors.append("Passwords must match")
        if errors:
            return {"status" : False, "errors" : errors}
        else:
            query = "INSERT INTO users (name, alias, email, password, dob, created_at, updated_at) VALUES (:name, :alias, :email, :pw_hash, :dob, NOW(), NOW())"
            data = {'name' : data['name'], 'alias' : data['alias'], 'email' : data['email'], 'pw_hash' : self.bcrypt.generate_password_hash(data['password']), 'dob' : data['dob']}
            self.db.query_db(query,data)
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            return {"status" : True, "user" : users[0]}

    def poke_button(self, id):

        query = "INSERT INTO pokes (numof_pokes, users_id, pokes_id) VALUES (1, :users_id, :pokes_id) ON DUPLICATE KEY UPDATE numof_pokes = numof_pokes + 1"
        data = {'id' : id}

        return self.db.query_db(query, data)


    def show_pokes(self, users_id):

        query = "SELECT users.name, pokes.id as poke_id, users.id as user_id FROM users LEFT JOIN pokes ON pokes.pokes_id = users.id WHERE pokes.users_id = :users_id ORDER BY poke_id DESC"
        data = {"users_id" : users_id}
        return self.db.query_db(query,data)

    def show_friendstopoke(self, users_id):
            query = "SELECT users.name , pokes.id as poke_id, users.alias, users.email, users.id FROM users LEFT JOIN pokes ON pokes.pokes_id = users.id WHERE (pokes.users_id NOT IN (SELECT pokes.users_id FROM pokes WHERE pokes.id = 1) OR pokes.users_id is NULL) ORDER BY users.id"
            values = {"users_id" : users_id}
            return self.db.query_db(query,values)

    def total_pokes(self, id):
        query = "SELECT COUNT(DISTINCT pokes_id) AS totalofpokes, name FROM pokes LEFT JOIN users ON users.id = pokes.users_id WHERE users.id = :id"
        values = {"id" : id}
        return self.db.query_db(query,values)
