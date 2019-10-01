import pymongo

from passlib.hash import pbkdf2_sha512
from db.database import database as mongodb


class Authentication:
    def login(self, username, password):
        return False

    def logout(self, username):
        return

    def register(self, username, password, acls):
        return False

    def get_acls(self, username):
        return []

    def has_acl(self, username, acl):
        return False


class MongoAuthentication(Authentication):
    def __init__(self, database, collection, field):
        # self._conn = pymongo.Connection(**kwargs)
        self._conn = mongodb.conn
        self._coll = self._conn[database][collection]
        self._field = field

    def login(self, user, password):
        record = self._coll.find_one({self._field: user})
        print "found=>",record
        if not record:
            print "user not exist"
            return False
        password_hash = record.get('passwd')
        rs = pbkdf2_sha512.verify(password, password_hash)
        return rs

    def logout(self, username):
        return

    def register(self, user):
        print "register=", user,self._field
        if not user.get(self._field, None) or not user.get('passwd', None):
            return -1

        print user.get(self._field)
        cond = {self._field: user.get(self._field)}
        print cond
        record = self._coll.find_one(cond)
        print record
        if record:
            return 1

        password_hash = pbkdf2_sha512.encrypt(user.get('passwd', None))
        user['passwd'] =password_hash

        self._coll.insert(user)
        return 0

    def changepwd(self, mobile, newpwd):
        record = self._coll.find_one({self._field: mobile})
        if record is None:
            return False
        password_hash = pbkdf2_sha512.encrypt(newpwd)
        if record['passwd'] == password_hash:
            return False
        self._coll.update({self._field: mobile}, {'$set': {'passwd': password_hash}})
        return True

    def changephone(self, mobile, new_phone):
        record = self._coll.find_one({"mobile": mobile})
        if record is None:
            return False
        self._coll.update({'mobile': mobile}, {'$set': {'mobile': new_phone}})
        return True

    def changepaypwd(self, mobile, newpwd):
        record = self._coll.find_one({"mobile": mobile})
        password_hash = pbkdf2_sha512.encrypt(newpwd)
        if record is None:
            return False
        self._coll.update({'mobile': mobile}, {'$set': {'pay_pwd': password_hash}})
        return True

    def get_acls(self, username):
        record = self._coll.find_one({"username": username})
        if record is None:
            return []
        return record['acl']

    def has_acl(self, username, acl):
        acls = self.get_acls(username)
        return acl in acls
