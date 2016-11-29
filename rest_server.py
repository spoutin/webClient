from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import ldap

'''
Docker command:
docker.exe run -d -i -t -p 389:389 -e SLAPD_PASSWORD=mysecretpassword -e SLAPD_DOMAIN=ldap.example.org --volume /users/ablack/:/etc/ldap.dist/prepopulate dinkel/openldap
'''


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'version': '3.5.1',
                    'last_build': date.today().isoformat()}
        self.write(response)


class GetGameByIdHandler(tornado.web.RequestHandler):

    def initialize(self, ldap):
        self.ldap = ldap

    def get(self, game_id):
        response = {'id': int(game_id),
                    'name': 'Crazy Game',
                    'release_date': date.today().isoformat(),
                    'cn': self.ldap.search()[1]['attributes']['cn'][0]
                    }
        self.write(response)


ldap = ldap.LdapClient()
ldap.connect()
application = tornado.web.Application([
    (r"/getgamebyid/([0-9]+)", GetGameByIdHandler, dict(ldap=ldap)),
    (r"/version", VersionHandler)
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
