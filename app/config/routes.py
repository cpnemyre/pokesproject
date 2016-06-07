from system.core.router import routes


routes['default_controller'] = 'Welcome'
routes['POST']['/login'] = 'Welcome#login'
routes['POST']['/register'] = 'Welcome#register'
routes['GET']['/pokesdash'] = 'Welcome#show_userpage'
routes['/pokebutton/<id>'] = 'Welcome#poke_button'
routes['/logout'] = 'Welcome#logout'
