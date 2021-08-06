





class ChatSocketHandler(tornado.websocket.WebSocketHandler):




    @classmethod
    def push_playlist(cls, playlist):
        print "push_playlist===>"
        if not playlist:
            return
        
        binded = playlist.get("bind",{})

        stores_ids = []
        for k,v in binded.iteritems():
            stores_ids.extend(v)

        stores_ids = list(set(stores_ids))
        stores = [ObjectId(x) for x in stores_ids]
        print "ddd",stores
        terminals = list(database.database.getDB().tb_terminal_profile.find({"_id": {"$in": stores}}))

        del playlist["bind"]
        xjson = json.dumps(playlist)
        print xjson

        msg = {"msgid": 3, "playlist": xjson}
        print "============================================="
        for t in terminals:
            for k,v in cls.devlist.iteritems():
                print "===>",v.get("userid"),t.get("userid")
                if v.get("userid") == t.get("userid"):
                    print k,cls.usersockets[k], msg
                    print cls.usersockets[k].write_message(msg)
                    print "++++++++++++++++++++++++++++"

    def on_message(self, message):
        print "on_message====>"
        logging.info("got message %r", message)
        print "message=",message
        parsed = tornado.escape.json_decode(message)
        if parsed["msgid"] == 1:
            print 'adduser start ...'
            dev = {
                "msgid": parsed.get("msgid"),
                "userid": parsed.get("userid"),
                "devid": parsed.get("devid"),
            }

            ChatSocketHandler.usersockets[parsed["devid"]] = self
            ChatSocketHandler.update_dev(dev)
            return

        if parsed["msgid"] == 2:
            print "close"
            return

        if parsed["msgid"] == 4:
            print 'playlist push result ...'
            msg = {
                "msgid": parsed.get("msgid"),
                "userid": parsed.get("userid"),
                "devid": parsed.get("devid"),
                "result": parsed.get("result"),
            }
