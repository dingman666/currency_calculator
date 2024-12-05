# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import sys
import inspect

class Wox(object):
    """
    Wox Python Plugin Base Class
    """
    def __init__(self):
        rpc_request = json.loads(sys.argv[1])
        # proxy setup
        self.proxy = rpc_request.get("proxy",{})
        request_method_name = rpc_request.get("method")
        request_parameters = rpc_request.get("parameters")
        methods = inspect.getmembers(self, predicate=inspect.ismethod)

        if request_method_name is not None and request_parameters is not None:
            method = dict(methods)[request_method_name]
            if method is not None:
                method(*request_parameters)

    def query(self,query):
        """
        sub class need to override this method
        """
        return []

    def debug(self,msg):
        """
        alert msg
        """
        print("DEBUG:{}".format(msg))
        sys.stdout.flush()

    def show_msg(self,title,sub_title,ico_path=""):
        """
        show messagebox
        """
        print("ShowMsg:{}|{}|{}".format(title,sub_title,ico_path))
        sys.stdout.flush()

    def change_query(self,query,requery = False):
        """
        change query
        """
        print("ChangeQuery:{}|{}".format(query,requery))
        sys.stdout.flush()

    def shell_run(self,cmd):
        """
        run shell commands
        """
        print("ShellRun:{}".format(cmd))
        sys.stdout.flush()

    def close_app(self):
        """
        close wox
        """
        print("CloseApp")
        sys.stdout.flush()

    def hide_app(self):
        """
        hide wox
        """
        print("HideApp")
        sys.stdout.flush()

    def send_keyboard(self,key,modifier=""):
        """
        send keystrokes
        """
        print("SendKeyboard:{}|{}".format(key,modifier))
        sys.stdout.flush()

    def open_setting(self):
        """
        open setting pancel
        """
        print("OpenSettingDialog")
        sys.stdout.flush()

    def start_loadingbar(self):
        """
        start loading animation in wox
        """
        print("API:StartLoadingBar")
        sys.stdout.flush()

    def stop_loadingbar(self):
        """
        stop loading animation in wox
        """
        print("API:StopLoadingBar")
        sys.stdout.flush()

    def reload_plugins(self):
        """
        reload all wox plugins
        """
        print("API:ReloadPlugins")
        sys.stdout.flush()