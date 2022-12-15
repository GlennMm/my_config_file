import os
import socket
import json
import subprocess
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.command import lazy
from qtile_extras import widget as ex_widget

mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser("~")


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


keys = [
    # Most of our keybindings are in sxhkd file - except these
    # SUPER + FUNCTION KEYS
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    # SUPER + SHIFT KEYS
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    # QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),
    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    # RESIZE UP, DOWN, LEFT, RIGHT
    Key(
        [mod, "control"],
        "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [mod, "control"],
        "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [mod, "control"],
        "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [mod, "control"],
        "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [mod, "control"],
        "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [mod, "control"],
        "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [mod, "control"],
        "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    Key(
        [mod, "control"],
        "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    # FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),
    # FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),
    # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),
    # TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
]


def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)


def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)


keys.extend(
    [
        # MOVE WINDOW TO NEXT SCREEN
        Key(
            [mod, "shift"],
            "Right",
            lazy.function(window_to_next_screen, switch_screen=True),
        ),
        Key(
            [mod, "shift"],
            "Left",
            lazy.function(window_to_previous_screen, switch_screen=True),
        ),
    ]
)

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6"]

# FOR AZERTY KEYBOARDS
# group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]

# group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0",]
group_labels = ["", "", "", "", "", ""]
# group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = [
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
]
# group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        )
    )

for i in groups:
    keys.extend(
        [
            # CHANGE WORKSPACES
            Key([mod], i.name, lazy.group[i.name].toscreen()),
            Key([mod], "Tab", lazy.screen.next_group()),
            Key([mod, "shift"], "Tab", lazy.screen.prev_group()),
            Key(["mod1"], "Tab", lazy.screen.next_group()),
            Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
            # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
            # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                lazy.group[i.name].toscreen(),
            ),
        ]
    )

# COLORS FOR THE BAR
# Pywal Colors
alpha = {
    "100%": "FF",
    "99%": "FC",
    "98%": "FA",
    "97%": "F7",
    "96%": "F5",
    "95%": "F2",
    "94%": "F0",
    "93%": "ED",
    "92%": "EB",
    "91%": "E8",
    "90%": "E6",
    "89%": "E3",
    "88%": "E0",
    "87%": "DE",
    "86%": "DB",
    "85%": "D9",
    "84%": "D6",
    "83%": "D4",
    "82%": "D1",
    "81%": "CF",
    "80%": "CC",
    "79%": "C9",
    "78%": "C7",
    "77%": "C4",
    "76%": "C2",
    "75%": "BF",
    "74%": "BD",
    "73%": "BA",
    "72%": "B8",
    "71%": "B5",
    "70%": "B3",
    "69%": "B0",
    "68%": "AD",
    "67%": "AB",
    "66%": "A8",
    "65%": "A6",
    "64%": "A3",
    "63%": "A1",
    "62%": "9E",
    "61%": "9C",
    "60%": "99",
    "59%": "96",
    "58%": "94",
    "57%": "91",
    "56%": "8F",
    "55%": "8C",
    "54%": "8A",
    "53%": "87",
    "52%": "85",
    "51%": "82",
    "50%": "80",
    "49%": "7D",
    "48%": "7A",
    "47%": "78",
    "46%": "75",
    "45%": "73",
    "44%": "70",
    "43%": "6E",
    "42%": "6B",
    "41%": "69",
    "40%": "66",
    "39%": "63",
    "38%": "61",
    "37%": "5E",
    "36%": "5C",
    "35%": "59",
    "34%": "57",
    "33%": "54",
    "32%": "52",
    "31%": "4F",
    "30%": "4D",
    "29%": "4A",
    "28%": "47",
    "27%": "45",
    "26%": "42",
    "25%": "40",
    "24%": "3D",
    "23%": "3B",
    "22%": "38",
    "21%": "36",
    "20%": "33",
    "19%": "30",
    "18%": "2E",
    "17%": "2B",
    "16%": "29",
    "15%": "26",
    "14%": "24",
    "13%": "21",
    "12%": "1F",
    "11%": "1C",
    "10%": "1A",
    "9%": "17",
    "8%": "14",
    "7%": "12",
    "6%": "0F",
    "5%": "0D",
    "4%": "0A",
    "3%": "08",
    "2%": "05",
    "1%": "03",
    "0%": "00",
}


colordict = json.load(open(os.path.expanduser("~/.cache/wal/colors.json")))
ColorZ = colordict["colors"]["color0"]
ColorA = colordict["colors"]["color1"]
ColorB = colordict["colors"]["color2"]
ColorC = colordict["colors"]["color3"]
ColorD = colordict["colors"]["color4"]
ColorE = colordict["colors"]["color5"]
ColorF = colordict["colors"]["color6"]
ColorG = colordict["colors"]["color7"]
ColorH = colordict["colors"]["color8"]
ColorI = colordict["colors"]["color9"]
ColorK = colordict["colors"]["color10"]
ColorL = colordict["colors"]["color11"]
ColorM = colordict["colors"]["color12"]
ColorN = colordict["colors"]["color13"]
ColorO = colordict["colors"]["color14"]
ColorP = colordict["colors"]["color15"]
BgColor = colordict["special"]["background"]
FgColor = colordict["special"]["foreground"]


def init_layout_theme():
    return {
        "margin": 2,
        "border_width": 2,
        "border_focus": "#5e81ac",
        "border_normal": "#4c566a",
    }


layout_theme = init_layout_theme()
layouts = [
    layout.MonadTall(
        margin=2, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"
    ),
    layout.MonadWide(
        margin=2, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"
    ),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme),
]


def init_colors():
    return [
        [ColorZ, ColorZ],  # color 0
        [BgColor, BgColor],  # color 1
        [FgColor, FgColor],  # color 2
        [ColorC, ColorC],  # color 3
        [ColorD, ColorD],  # color 4
        [ColorE, ColorE],  # color 5
        [ColorF, ColorF],  # color 6
        [ColorG, ColorG],  # color 7
        [ColorH, ColorH],  # color 8
        [ColorI, ColorI],  # color 9
        [ColorK, ColorK],  # color 10
        [ColorL, ColorL],  # color 11
        [ColorM, ColorM],  # color 12
        [ColorN, ColorN],  # color 13
        [ColorO, ColorO],  # color 14
        [ColorP, ColorP],  # color 15
    ]


colors = init_colors()
fonts = {
    "FaSolid": "Font Awesome 6 Free Solid",
    "FaBrand": "Font Awesome 6 Free Brand",
    "FaUn": "Font Awesome 6 Free ",
    "Fa": "FontAwesome",
    "text": "SF Pro Text",
    "text-bold": "SF Pro Rounded Bold",
}


# WIDGETS FOR THE BAR
def init_widgets_defaults():
    return dict(font=fonts["text"], fontsize=10, padding=2, background=colors[1])


widget_defaults = init_widgets_defaults()


def init_widgets_list():
    widgets_list = [
        widget.GroupBox(
            font=fonts["FaSolid"],
            fontsize=14,
            margin_y=3,
            margin_x=0,
            padding_y=6,
            padding_x=5,
            borderwidth=0,
            disable_drag=True,
            active=colors[5],
            inactive=colors[11],
            rounded=False,
            highlight_method="text",
            this_current_screen_border=colors[3],
            foreground=colors[9],
            background=colors[1],
        ),
        #widget.currentlayout
        widget.CurrentLayoutIcon(
            font=fonts["FaSolid"],
            padding=2,
            scale=0.7,
            foreground=colors[9],
            background=colors[1],
        ),
        ex_widget.GlobalMenu(
            foreground=colors[6], background=colors[1], icon_size="autofit", padding=6
        ),
        widget.Spacer(background=colors[1]),
        widget.Bluetooth(font=fonts["text"], foreground=colors[5], background=colors[1]),
        ex_widget.StatusNotifier(
            font=fonts["text"],
            foreground=colors[9],
            fontsize=9,
            background=colors[1],
        ),
        ex_widget.WiFiIcon(
            active_color=colors[5],
            foreground=colors[9],
            fontsize=7,
            background=colors[1],
        ),
        ex_widget.UPowerWidget(
            spacing=10,
            fontsize=9,
            foreground=colors[9],
            background=colors[1],
        ),
        widget.TextBox(
            font=fonts["FaSolid"],
            text="  ",
            foreground=colors[9],
            background=colors[1],
            padding=0,
            fontsize=16,
        ),
        widget.Clock(
            foreground=colors[9],
            background=colors[1],
            fontsize=12,
            format="%Y-%m-%d %H:%M",
        ),
    ]
    return widgets_list


widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2


widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [
        Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=21, opacity=0.6)),
        Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=21, opacity=0.6)),
    ]


screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Click(
        [mod],
        "Button3",
        lazy.spawn("rofi -show drun -theme .cache/wal/colors-rofi-light.rasi"),
    ),
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ################## tf
#########################################################
# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#     #####################################################################################
#     ### Use xprop fo find  the value of WM_CLASS(STRING) -> First field is sufficient ###
#     #####################################################################################
#     d[group_names[0]] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
#               "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
#     d[group_names[1]] = [ "Atom", "Subl", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
#                "atom", "subl", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
#     d[group_names[2]] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
#               "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
#     d[group_names[3]] = ["Gimp", "gimp" ]
#     d[group_names[4]] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld" ]
#     d[group_names[5]] = ["Vlc","vlc", "Mpv", "mpv" ]
#     d[group_names[6]] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
#               "virtualbox manager", "virtualbox machine", "vmplayer", ]
#     d[group_names[7]] = ["Thunar", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt",
#               "thunar", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
#     d[group_names[8]] = ["Evolution", "Geary", "Mail", "Thunderbird",
#               "evolution", "geary", "mail", "thunderbird" ]
#     d[group_names[9]] = ["Spotify", "Pragha", "Clementine", "Deadbeef", "Audacious",
#               "spotify", "pragha", "clementine", "deadbeef", "audacious" ]
#     ######################################################################################
#
# wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen(toggle=False)

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME


main = None


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/scripts/autostart.sh"])


@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(["xsetroot", "-cursor_name", "left_ptr"])


@hook.subscribe.client_new
def set_floating(window):
    if (
        window.window.get_wm_transient_for()
        or window.window.get_wm_type() in floating_types
    ):
        window.floating = True


floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="Arcolinux-welcome-app.py"),
        Match(wm_class="Archlinux-tweak-tool.py"),
        Match(wm_class="Arcolinux-calamares-tool.py"),
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(wm_class="Arandr"),
        Match(wm_class="feh"),
        Match(wm_class="Galculator"),
        Match(wm_class="archlinux-logout"),
        Match(wm_class="xdman"),
    ],
    fullscreen_border_width=0,
    border_width=0,
)
auto_fullscreen = True

focus_on_window_activation = "focus"  # or smart

wmname = "LG3D"
