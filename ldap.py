from ldap3 import Server, Connection, ALL, SIMPLE, ALL_ATTRIBUTES


class LdapClient(object):

    def __init__(self):
        self.host = "ldap://localhost:389"
        self.binddn = "cn=admin,dc=ldap,dc=example,dc=org"
        self.password = "mysecretpassword"
        self.searchFilter = "(objectClass=organizationalRole)"
        self.server = Server(self.host, port=389, get_info=ALL)
        self.connection = None

    def connect(self):
        self.connection = Connection(self.server, authentication=SIMPLE, user=self.binddn, password=self.password, check_names=True, lazy=False, raise_exceptions=True)
        self.connection.open()
        self.connection.bind()

    def disconnect(self):
        self.connection.unbind()

    def search(self):
            self.connection.search(search_base='dc=ldap,dc=example,dc=org', search_filter=self.searchFilter, attributes=ALL_ATTRIBUTES)
            return self.connection.response