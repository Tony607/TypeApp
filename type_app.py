import pyautogui
import time
import os
import wx
import wx.adv
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
                time.sleep(2)
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
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Type APP", pos=wx.DefaultPosition, size=wx.Size(614, 573),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        main_v_sizer = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"History", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        main_v_sizer.Add(self.m_staticText1, 0, wx.ALL, 5)

        self.text_ctrl_history = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(600, 300),
                                             wx.TE_MULTILINE)
        self.text_ctrl_history.SetToolTip(u"Sent history")

        main_v_sizer.Add(self.text_ctrl_history, 0, wx.ALL, 5)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"Input", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        main_v_sizer.Add(self.m_staticText2, 0, wx.ALL, 5)

        cmd_h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.text_ctrl_cmd = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(400, 150),
                                         wx.TE_MULTILINE)
        self.text_ctrl_cmd.SetToolTip(u"Type here and click Sent button")

        cmd_h_sizer.Add(self.text_ctrl_cmd, 0, wx.ALL, 5)

        cmd_ctl_v_sizer = wx.BoxSizer(wx.VERTICAL)

        cmd_ctl_opt_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.checkbox_enter = wx.CheckBox(self, wx.ID_ANY, u"Enter", wx.DefaultPosition, wx.DefaultSize, 0)
        self.checkbox_enter.SetValue(True)
        self.checkbox_enter.SetToolTip(u"Append Enter key for each Sent")

        cmd_ctl_opt_sizer.Add(self.checkbox_enter, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.checkbox_switch_win = wx.CheckBox(self, wx.ID_ANY, u"Auto Switch", wx.DefaultPosition, wx.DefaultSize, 0)
        self.checkbox_switch_win.SetToolTip(u"Auto switch to window before typing")

        cmd_ctl_opt_sizer.Add(self.checkbox_switch_win, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        cmd_ctl_v_sizer.Add(cmd_ctl_opt_sizer, 1, wx.ALL | wx.EXPAND, 5)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"Window Feature File", wx.DefaultPosition, wx.DefaultSize,
                                           0)
        self.m_staticText3.Wrap(-1)
        cmd_ctl_v_sizer.Add(self.m_staticText3, 0, wx.ALL, 5)

        self.file_picker_img = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*",
                                                 wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        self.file_picker_img.SetToolTip(u"Select a image file")

        cmd_ctl_v_sizer.Add(self.file_picker_img, 0, wx.ALL, 5)

        self.button_sent = wx.Button(self, wx.ID_ANY, u"Sent", wx.DefaultPosition, wx.DefaultSize, 0)
        cmd_ctl_v_sizer.Add(self.button_sent, 0, wx.ALL, 5)

        cmd_h_sizer.Add(cmd_ctl_v_sizer, 1, wx.EXPAND, 5)

        main_v_sizer.Add(cmd_h_sizer, 1, wx.EXPAND, 5)

        self.SetSizer(main_v_sizer)
        self.Layout()
        self.main_menubar = wx.MenuBar(0)
        self.menu_file = wx.Menu()
        self.menu_choose_feature = wx.MenuItem(self.menu_file, wx.ID_ANY, u"Choose Feature File", wx.EmptyString,
                                               wx.ITEM_NORMAL)
        self.menu_file.Append(self.menu_choose_feature)

        self.menu_load_file = wx.MenuItem(self.menu_file, wx.ID_ANY, u"Load Input from File", wx.EmptyString,
                                          wx.ITEM_NORMAL)
        self.menu_file.Append(self.menu_load_file)

        self.main_menubar.Append(self.menu_file, u"File")

        self.menu_help = wx.Menu()
        self.menu_get_about = wx.MenuItem(self.menu_help, wx.ID_ANY, u"About", wx.EmptyString, wx.ITEM_NORMAL)
        self.menu_help.Append(self.menu_get_about)

        self.main_menubar.Append(self.menu_help, u"Help")

        self.SetMenuBar(self.main_menubar)

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

    def sent_enable(self, enable):
        self.button_sent.Enable(enable)


class Model:
    def __init__(self):
        pass


class Controller:
    def __init__(self, app):
        self.model = Model()
        self.main_view = MainView(None)
        self.main_view.button_sent.Bind(wx.EVT_BUTTON, self.type_command)
        self.main_view.Bind(wx.EVT_MENU, self.choose_feature_img, id=self.main_view.menu_choose_feature.GetId())
        self.main_view.Bind(wx.EVT_MENU, self.load_input_file, id=self.main_view.menu_load_file.GetId())
        self.main_view.Bind(wx.EVT_MENU, self.show_about, id=self.main_view.menu_get_about.GetId())
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

    def choose_feature_img(self, event):
        event.Skip()
        img_file_dialog = wx.FileDialog(None, "Feature image", "", "",
                                           "Image File (*.jpeg,*.jpg,*.png)|*.jpeg;*.jpg;*.png",
                                            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if img_file_dialog.ShowModal() == wx.ID_CANCEL:
            return  # the user changed idea...
        img = img_file_dialog.GetPath()
        self.main_view.file_picker_img.SetPath(img)

    def load_input_file(self, event):
        event.Skip()
        input_file_dialog = wx.FileDialog(None, "Input Text File", "", "",
                                           "Text File (*.*)|*.*",
                                            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if input_file_dialog.ShowModal() == wx.ID_CANCEL:
            return  # the user changed idea...
        file = input_file_dialog.GetPath()
        with open(file, "r") as f:
            try:
                text = f.read()
                self.main_view.text_ctrl_cmd.SetValue(text)
            except:
                msg = wx.MessageDialog(None, message="Not a text file.",
                                       caption="Error", style=wx.ICON_INFORMATION)
                msg.ShowModal()
                msg.Destroy()

    def show_about(self, event):
        event.Skip()
        about_info = wx.adv.AboutDialogInfo()
        about_info.SetName("Type App")
        about_info.SetVersion("V1.0")
        about_info.SetDescription("An automatically typing GUI.\n ")
        about_info.SetWebSite("https://github.com/Tony607/TypeApp", "GitHub")
        about_info.SetDevelopers(["Chengwei"])
        wx.adv.AboutBox(about_info)

    def type_command(self, evt):
        self.main_view.sent_enable(False)
        enter = self.main_view.get_enter()
        cmd = self.main_view.get_cmd()
        img_path = self.main_view.get_img_path()
        print(cmd)
        if enter:
            cmd = cmd + "\n"
        worker = TypingThread(self.main_view, TypePara(cmd, img_path))
        worker.start()

    def on_type_over(self, evt):
        evt_value = evt.get_value()
        if evt_value:
            print("Done Typing \"{}\"".format(evt_value))
        else:
            pyautogui.alert('Please move the window \"feature\" to current screen and try again.')
        self.main_view.sent_enable(True)


if __name__ == "__main__":
    app = wx.App(False)
    controller = Controller(app)
    app.MainLoop()
