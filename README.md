WeeChat WebPush Script
======================

This is a plugin for the famous and extensible [WeeChat](https://weechat.org/) chat client.

This plugin will send information of private messages via WebPush to a client previously configured. This will allow any web client, like [Glowing Bear](https://www.glowing-bear.org/), receive notifications even if web app is not running in a tab.


# Configuration
When loading the script via
```
/python load webpush.py
```

You will see on the screen a series of variables that you will need to configure, those variables will come from your browser. Different web clients will have different ways of providing you this credentials once they request the user permissions to perform push notifications.

# Dependencies
In order to perform the crypto operations, this plugin is using the [WebPushProxy](https://github.com/arcturus/webpushproxy) service, right now a public (and private) instance, but you can deploy your own WebPushProxy to be free of any 3rd party machine that you don't control.