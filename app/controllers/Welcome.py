from system.core.controller import *

class Welcome(Controller):
    def __init__(self, action):
        super(Welcome, self).__init__(action)

        self.load_model('WelcomeModel')
        self.db = self._app.db


    def index(self):

        return self.load_view('index.html')

    def login(self):
        login_info = self.models['WelcomeModel'].login(request.form)
        if login_info['status'] == True:
            session['id'] = login_info['user']['id']
            session['name'] = login_info['user']['name']
            return redirect('/pokesdash')
        else:
            for message in login_info['errors']:
                flash(message)
            return redirect('/')

    def register(self):
        user_info = self.models['WelcomeModel'].register(request.form)
        if user_info['status'] == True:
            session['id'] = user_info['user']['id']
            session['name'] = user_info['user']['name']
            return redirect('/pokesdash')
        else:
            for message in user_info['errors']:
                flash(message)
            return redirect('/')

    def logout(self):
        session.clear()
        return redirect('/')

    def show_userpage(self):
        poke_me = self.models['WelcomeModel'].show_pokes(session['id'])
        poke_friends = self.models['WelcomeModel'].show_friendstopoke(session['id'])
        totalofpokes = self.models['WelcomeModel'].total_pokes(session['id'])

        return self.load_view('pokesdash.html', poke_me = poke_me, poke_friends = poke_friends, totalofpokes = totalofpokes)

    def showpokes(self):

        return self.load_view('pokesdash.html', poke_me = poke_me , poke_friends = poke_friends, totalofpokes = totalofpokes)

    def poke_button(self, id):
        poke_person = self.models['WelcomeModel'].poke_button(id)
        return redirect ('/pokesdash')
