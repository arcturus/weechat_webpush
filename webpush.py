# -*- coding: utf-8 -*-
# Author: Francisco Jordano <francisco@jordano.es>
# Homepage:
# Derived from notifo:
#   Author: ochameau <poirot.alex AT gmail DOT com>
#   Homepage: https://github.com/ochameau/weechat-notifo
# And from: notify
#   Author: lavaramano <lavaramano AT gmail DOT com>
#   Improved by: BaSh - <bash.lnx AT gmail DOT com>
#   Ported to Weechat 0.3.0 by: Sharn - <sharntehnub AT gmail DOT com)
# And from: notifo_notify
#   Author: SAEKI Yoshiyasu <laclef_yoshiyasu@yahoo.co.jp>
#   Homepage: http://bitbucket.org/laclefyoshi/weechat/
# This plugin send push notifications to your iPhone or Android smartphone
# by using Notifo.com mobile application/services
# Requires Weechat 1.0.0
# Released under GNU GPL v2
#
# 2017-03-27, Francisco Jordano <francisco@jordano.es>
#     version 0.1: send web push notifications. It will use vapi and or gcm, which data
#                  will need to be provided via configuration object.

import weechat, string, urllib, urllib2, json

weechat.register("webpush", "francisco.jordano", "0.1", "GPL", "webpush: Send webpush notifications about your private messages and highlights.", "", "")

configuration = {
    "endpoint": "",
    "key": "",
    "authSecret": "",
    "webpushProxy": "",
    "vapidPublicKey": "",
    "vapidPrivateKey": "",
    "vapidSubject": ""
}

for option, default_value in configuration.items():
    if weechat.config_get_plugin(option) == "":
        weechat.prnt("", weechat.prefix("error") + "webpush: Please set option: %s" % option)
        weechat.prnt("", "webpush: /set plugins.var.python.webpush.%s STRING" % option)

# Hook privmsg/hilights
weechat.hook_print("", "irc_privmsg", "", 1, "notify_show", "")

# Functions
def notify_show(data, bufferp, uber_empty, tagsn, isdisplayed,
        ishilight, prefix, message):

    if (bufferp == weechat.current_buffer()):
        pass

    elif weechat.buffer_get_string(bufferp, "localvar_type") == "private":
        show_notification(prefix, message)

    elif int(ishilight):
        buffer = (weechat.buffer_get_string(bufferp, "short_name") or
                weechat.buffer_get_string(bufferp, "name"))
        show_notification(buffer, prefix + ": " + message)

    return weechat.WEECHAT_RC_OK

def show_notification(chan, message):
    weechat.prnt("", "Showing notification")
    payload_dic = {
        "endpoint": weechat.config_get_plugin("endpoint"),
        "key": weechat.config_get_plugin("key"),
        "authSecret": weechat.config_get_plugin("authSecret"),
	"payload": {
		"channel": chan,
		"msg": message
	},
	"vapidDetails": {
		"publicKey": weechat.config_get_plugin("vapidPublicKey"),
		"privateKey": weechat.config_get_plugin("vapidPrivateKey"),
		"subject": weechat.config_get_plugin("vapidSubject")
	}
    }
    url = weechat.config_get_plugin("webpushProxy")
    weechat.prnt("", url)
    weechat.prnt("", json.dumps(payload_dic))
    #payload = urllib.urlencode(payload_dic)
    python2_bin = weechat.info_get("python2_bin", "") or "python"
    weechat.prnt("", python2_bin)
    payload = json.dumps(payload_dic).replace('"', '\\"')
    #weechat.hook_process(
    #        python2_bin + " -c \"import urllib2\n"
    #        "req = urllib2.Request('" + url + "', '" + payload + "', {'Content-Type': 'application/json'})\n"
    #        "res = urllib2.urlopen(req)\n\"",
    #        30 * 1000, "", "")
    cmd = """{} -c "import urllib2
req = urllib2.Request('{}', '{}', {{'Content-Type': 'application/json'}})
res = urllib2.urlopen(req)
""".format(python2_bin, url, payload)
    weechat.prnt("", cmd)
    weechat.hook_process(cmd, 30 * 1000, "", "")

# vim: autoindent expandtab smarttab shiftwidth=4
