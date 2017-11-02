import pyautogui
import time
import os
import wx
import threading
import json

CONFIG_FILE = ".//res//config.json"
DEFAULT_CONFIGS = {"enter": True, "switch": False, "img": ""}
myEVT_TYPE = wx.NewEventType()
EVT_TYPE = wx.PyEventBinder(myEVT_TYPE, 1)


class TypePara:
    def __init__(self, text, img):
        if text is not None:
            self.cmd = str(text)
        else:
            self.cmd = None
        if img is not None:
            self.img = str(img)
        else:
            self.img = None


class TypingEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid, value=None):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._value = value

    def get_value(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._value


class TypingThread(threading.Thread):
    def __init__(self, parent, value):
        """
                @param parent: The gui object that should recieve the value
                @param value: value to 'calculate' to
                """
        threading.Thread.__init__(self)
        self._parent = parent
        self._value = value

    def run(self):
        """Overrides Thread.run. Don't call this directly its called internally
        when you call Thread.start().
        """
        time.sleep(0.5)  # our simulated calculation time
        if isinstance(self._value, TypePara):
            cmd = self._value.cmd
            img = self._value.img
            done_typing = False
            if img is not None and os.path.exists(img):
                last_coordinate = pyautogui.position()
                coordinate = pyautogui.locateCenterOnScreen(img)
                if coordinate is not None:
                    x, y = coordinate
                    pyautogui.click(x=x, y=y, clicks=1, button='left')
                    pyautogui.typewrite(cmd, interval=0.01)
                    done_typing = True
                    pyautogui.moveTo(last_coordinate[0], last_coordinate[1], duration=.1)
            else:
                pyautogui.typewrite(cmd, interval=0.01)
                done_typing = True
            if done_typing:
                evt_value = cmd
            else:
                evt_value = None
            evt = TypingEvent(myEVT_TYPE, -1, evt_value)
            wx.PostEvent(self._parent, evt)


class MainView(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Type App", pos=wx.DefaultPosition,
                          size=wx.Size(614, 507), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        main_v_sizer = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"History", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        main_v_sizer.Add(self.m_staticText1, 0, wx.ALL, 5)

        self.text_ctrl_history = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(550, 300),
                                             wx.TE_MULTILINE)
        main_v_sizer.Add(self.text_ctrl_history, 0, wx.ALL, 5)

        cmd_h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.text_ctrl_cmd = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(400, 150),
                                         wx.TE_MULTILINE)
        cmd_h_sizer.Add(self.text_ctrl_cmd, 0, wx.ALL, 5)

        cmd_ctl_v_sizer = wx.BoxSizer(wx.VERTICAL)

        cmd_ctl_opt_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.checkbox_enter = wx.CheckBox(self, wx.ID_ANY, u"Enter", wx.DefaultPosition, wx.DefaultSize, 0)
        self.checkbox_enter.SetValue(True)
        cmd_ctl_opt_sizer.Add(self.checkbox_enter, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.checkbox_switch_win = wx.CheckBox(self, wx.ID_ANY, u"Auto Switch", wx.DefaultPosition, wx.DefaultSize, 0)
        cmd_ctl_opt_sizer.Add(self.checkbox_switch_win, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        cmd_ctl_v_sizer.Add(cmd_ctl_opt_sizer, 1, wx.ALL | wx.EXPAND, 5)

        self.file_picker_img = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*",
                                                 wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        cmd_ctl_v_sizer.Add(self.file_picker_img, 0, wx.ALL, 5)

        self.button_sent = wx.Button(self, wx.ID_ANY, u"Sent", wx.DefaultPosition, wx.DefaultSize, 0)
        cmd_ctl_v_sizer.Add(self.button_sent, 0, wx.ALL, 5)

        cmd_h_sizer.Add(cmd_ctl_v_sizer, 1, wx.EXPAND, 5)

        main_v_sizer.Add(cmd_h_sizer, 1, wx.EXPAND, 5)

        self.SetSizer(main_v_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

    def get_switch(self):
        return self.checkbox_switch_win.GetValue()

    def get_cmd(self):
        return self.text_ctrl_cmd.GetValue()

    def get_enter(self):
        return self.checkbox_enter.GetValue()

    def get_img_path(self):
        if self.checkbox_switch_win.GetValue():
            return self.file_picker_img.GetPath()
        else:
            return None

    def append_history(self, text):
        new_text = str(text)
        if not new_text.startswith("\n"):
            new_text = "\n" + new_text
        self.text_ctrl_history.AppendText(new_text)

    def load_settings(self, enter, switch, img=""):
        self.checkbox_switch_win.SetValue(switch)
        self.checkbox_enter.SetValue(enter)
        if img is None:
            img = ""
        if os.path.exists(img) or img == "":
            self.file_picker_img.SetPath(img)
        else:
            raise FileExistsError('Path: \"{}\" not exist.'.format(img))


class Model:
    def __init__(self):
        pass


class Controller:
    def __init__(self, app):
        self.model = Model()
        self.main_view = MainView(None)
        self.main_view.button_sent.Bind(wx.EVT_BUTTON, self.type_command)
        self.main_view.Bind(wx.EVT_CLOSE, self.on_close)
        self.main_view.Bind(EVT_TYPE, self.on_type_over)
        self.load_config()
        self.main_view.Show()

    def on_close(self, event):
        event.Skip()
        self.save_config()

    def save_config(self):
        configs = dict()
        configs["enter"] = self.main_view.get_enter()
        configs["switch"] = self.main_view.get_switch()
        configs["img"] = self.main_view.get_img_path()
        with open(CONFIG_FILE, 'w') as json_file:
            json.dump(configs, json_file, indent=4)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as json_file:
                configs = json.load(json_file)
                self.main_view.load_settings(configs["enter"], configs["switch"], configs["img"])
        else:
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            with open(CONFIG_FILE, 'w') as json_file:
                json.dump(DEFAULT_CONFIGS, json_file, indent=4)
            self.main_view.load_settings(DEFAULT_CONFIGS["enter"], DEFAULT_CONFIGS["switch"], DEFAULT_CONFIGS["img"])

    def type_command(self,evt):
        enter = self.main_view.get_enter()
        cmd = self.main_view.get_cmd()
        img_path = self.main_view.get_img_path()
        print(cmd)
        if enter:
            cmd = cmd + "\n"
        self.main_view.append_history(cmd)
        worker = TypingThread(self.main_view, TypePara(cmd, img_path))
        worker.start()

    def on_type_over(self, evt):
        evt_value = evt.get_value()
        if evt_value:
            print("Done Typing \"{}\"".format(evt_value))
        else:
            pyautogui.alert('Please move the window \"feature\" to current screen and try again.')


if __name__ == "__main__":
    app = wx.App(False)
    controller = Controller(app)
    app.MainLoop()
