"""A GUI for the library"""

import wx

from artipy.stats import MainStat
from artipy.types import STAT_NAMES, VALID_MAINSTATS, ArtifactSlot, StatType

INVERTED_STAT_NAMES: dict[str, StatType] = {v: k for k, v in STAT_NAMES.items()}


class ArtipyFrame(wx.Frame):  # type: ignore
    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super(ArtipyFrame, self).__init__(*args, **kwargs)

        pnl = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.slot_comboBox = wx.ComboBox(
            pnl, choices=list(ArtifactSlot), style=wx.CB_READONLY
        )
        self.stat_comboBox = wx.ComboBox(
            pnl,
            choices=[STAT_NAMES[s] for s in VALID_MAINSTATS[ArtifactSlot.FLOWER]],
            style=wx.CB_READONLY,
        )

        self.level_entry = wx.TextCtrl(pnl, style=wx.TE_PROCESS_ENTER)
        self.level_entry.SetHint("0~20")
        self.stat_textBox = wx.TextCtrl(pnl, style=wx.TE_READONLY)

        self.level_entry.Bind(wx.EVT_TEXT_ENTER, self.on_level_change)
        self.slot_comboBox.Bind(wx.EVT_COMBOBOX, self.on_slot_change)
        self.stat_comboBox.Bind(wx.EVT_COMBOBOX, self.on_stat_change)

        sizer.Add(self.level_entry, 0, wx.ALL, 5)
        sizer.Add(self.slot_comboBox, 0, wx.ALL, 5)
        sizer.Add(self.stat_comboBox, 0, wx.ALL, 5)
        sizer.Add(self.stat_textBox, 0, wx.ALL, 5)

        self.level_entry.SetValue("0")
        self.slot_comboBox.SetSelection(0)
        self.stat_comboBox.SetSelection(0)

        self.mainstat = MainStat(INVERTED_STAT_NAMES[self.stat_comboBox.GetValue()])
        self.mainstat.set_value_by_level(int(self.level_entry.GetValue()))

        self.stat_textBox.SetValue(str(self.mainstat))

        pnl.SetSizer(sizer)

        self.SetSize((300, 300))
        self.Show(True)

    def on_slot_change(self, event: wx.PyEvent) -> None:  # type: ignore
        slot = self.slot_comboBox.GetValue()
        self.stat_comboBox.SetItems([
            STAT_NAMES[s] for s in VALID_MAINSTATS[ArtifactSlot(slot)]
        ])
        self.stat_comboBox.SetSelection(0)

        self.stat_textBox.SetValue(str(self.mainstat))

    def on_stat_change(self, event: wx.PyEvent) -> None:  # type: ignore
        self.stat_textBox.SetValue(str(self.mainstat))

    def on_level_change(self, event: wx.PyEvent) -> None:  # type: ignore
        value = self.level_entry.GetValue()

        try:
            number = int(value)
        except ValueError:
            self.level_entry.SetValue("0")
            self.mainstat.set_value_by_level(0)
            return

        if number < 0:
            self.level_entry.SetValue("0")
        elif number > 20:
            self.level_entry.SetValue("20")
        self.mainstat.set_value_by_level(int(self.level_entry.GetValue()))
        self.stat_textBox.SetValue(str(self.mainstat))


if __name__ == "__main__":
    app = wx.App()
    ArtipyFrame(None, title="artipy")
    app.MainLoop()
