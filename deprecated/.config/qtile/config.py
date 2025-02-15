# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, qtile
from libqtile.config import Click, Drag, Group, Key, Match, hook, Screen
from libqtile.lazy import lazy
# from libqtile.dgroups import simple_key_binder
import os
import subprocess

mod = "mod4"
terminal = "alacritty"

# █▄▀ █▀▀ █▄█ █▄▄ █ █▄░█ █▀▄ █▀
# █░█ ██▄ ░█░ █▄█ █ █░▀█ █▄▀ ▄█

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows

    # WINDOWS
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),

    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),

    Key(["control", "mod1"], "l", lazy.screen.next_group(), desc="Move to next group"),
    Key(["control", "mod1"], "h", lazy.screen.prev_group(), desc="Move to previous group"),

    Key(["control", "mod1"], "right", lazy.screen.next_group(), desc="Move to next group"),
    Key(["control", "mod1"], "left", lazy.screen.prev_group(), desc="Move to previous group"),

    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "Return", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod], "space", lazy.window.toggle_float(), desc="Toggle float"),
    Key([mod], "q", lazy.next_layout(), desc="Toggle between layouts"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),

    # QTILE

    Key([mod], "t", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle E tween different layouts as defined below
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key(["mod1", "control"], "Delete", lazy.shutdown(), desc="Shutdown Qtile"),


    # CUSTOM
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +5%"), desc='Volume Up'),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -5%"), desc='volume down'),
    Key([], "XF86AudioMute", lazy.spawn("pulsemixer --toggle-mute"), desc='Volume Mute'),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc='playerctl'),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc='playerctl'),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc='playerctl'),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s 10%+"), desc='brightness UP'),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 10%-"), desc='brightness Down'),


]


# █▀▀ █▀█ █▀█ █░█ █▀█ █▀
# █▄█ █▀▄ █▄█ █▄█ █▀▀ ▄█
@lazy.function
def window_to_prev_group(qtile):
    i = qtile.groups.index(qtile.current_group)
    if qtile.current_window is not None and i != 0:
        qtile.current_window.togroup(qtile.groups[i - 1].name)
        qtile.current_screen.toggle_group(qtile.groups[i - 1])


@lazy.function
def window_to_next_group(qtile):
    i = qtile.groups.index(qtile.current_group)
    if qtile.current_window is not None and i != 6:
        qtile.current_window.togroup(qtile.groups[i + 1].name)
        qtile.current_screen.toggle_group(qtile.groups[i + 1])


groups = [Group(f"{i + 1}", label="") for i in range(9)]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            Key(
                ["mod1", "shift"],
                "right",
                window_to_next_group,
                desc="Switch to & move focused window to group {}",
            ),
            Key(
                ["mod1", "shift"],
                "left",
                window_to_prev_group,
                desc="Switch to & move focused window to group {}",
            ),
        ]
    )

# ##𝙇𝙖𝙮𝙤𝙪𝙩###

layouts = [
    layout.Bsp(
        border_focus='#9EE9EA',
        border_normal='#343A40',
        margin=7,
        border_width=2,
        fair=True,
        ratio=1.6,
    ),

    layout.Floating(
        border_focus='#9EE9EA',
        border_normal='#343A40',
        margin=7,
        border_width=2,
    ),
    # Try more layouts by unleashing below layouts
    #  layout.Stack(num_stacks=2),

    #  layout.TreeTab(),
    #  layout.VerticalTile(),
    #  layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = [widget_defaults.copy()
                      ]


def open_launcher():
    qtile.cmd_spawn("rofi -show drun")


# █▄▄ ▄▀█ █▀█
# █▄█ █▀█ █▀▄

screens = [

    Screen(
        top=bar.Bar(
            [
                widget.Spacer(length=20,
                              background='#20262C',
                              ),

                widget.Image(
                    filename='~/.config/qtile/Assets/launch_Icon.png',
                    mouse_callbacks={'Button1': lazy.spawn("/home/juftuf/.config/rofi/launchers/misc/launcher.sh")},
                    margin=2,
                    background='#20262C',
                ),

                widget.Spacer(length=2,
                              background='#20262C',
                              ),

                widget.Image(
                    filename='~/.config/qtile/Assets/7.png',
                ),

                widget.TextBox(
                    fontsize=20,
                    foreground='#82DF94',
                    text='',
                    background='#343A40',
                ),

                widget.CPU(
                    background='#343A40',
                    fontsize=12,
                    font='JetBrains Mono Bold',
                    format=' {freq_current}GHz {load_percent}%',
                    update_interval=2,

                ),

                widget.ThermalSensor(
                    fontsize=12,
                    font='JetBrains Mono Bold',
                    tag_sensor='Tctl',
                    background='#343A40',
                    metric='True',
                    update_interval=5,
                    threshold=85,
                    foreground_alert='#f6ae4a',
                ),

                widget.TextBox(
                    fontsize=20,
                    foreground='#82DF94',
                    text='',
                    background='#343A40',
                ),

                widget.ThermalSensor(
                    fontsize=12,
                    font='JetBrains Mono Bold',
                    tag_sensor='junction',
                    background='#343A40',
                    metric='True',
                    update_interval=5,
                ),

                widget.TextBox(
                    fontsize=20,
                    foreground='#82DF94',
                    text='',
                    background='#343A40',
                ),

                widget.Memory(
                    format='{MemUsed:.0f}{mm}',
                    measure_mem='G',
                    font="JetBrains Mono Bold",
                    fontsize=12,
                    background='#343A40',
                    update_interval=5,
                ),

                widget.Spacer(length=2,
                              background='#343A40',
                              ),

                widget.Image(
                    filename='~/.config/qtile/Assets/8.png',
                ),
                widget.Image(
                    filename='~/.config/qtile/Assets/7.png',
                ),

                widget.GroupBox(
                    fontsize=16,
                    borderwidth=3,
                    highlight_method='block',
                    hide_unused=True,
                    active='#f1fcf9',
                    block_highlight_text_color="#9EE9EA",
                    highlight_color='#4B427E',
                    inactive='#858988',
                    foreground='#4B427E',
                    background='#343A40',
                    this_current_screen_border='#343A40',
                    this_screen_border='#343A40',
                    other_current_screen_border='#343A40',
                    other_screen_border='#343A40',
                    urgent_border='#343A40',
                    rounded=True,
                    disable_drag=True,
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/8.png',
                ),

                widget.CurrentLayoutIcon(
                    background='#20262C',
                    padding=0,
                    scale=0.5,
                ),

                widget.CurrentLayout(
                    background='#20262C',
                    padding=0,
                    max_chars=20,
                    font='JetBrains Mono Bold',
                ),

                widget.TextBox(
                    text=' ',
                    background='#20262C',
                ),

                widget.WindowName(
                    background='#20262C',
                    format="{name}",
                    font='JetBrains Mono Bold',
                    empty_group_string='Desktop',
                ),

                widget.Spacer(length=bar.STRETCH,
                              background='#20262C',
                              ),

                widget.TextBox(
                    fontsize=20,
                    foreground='#82DF94',
                    text='',
                    background='#20262C',
                ),

                widget.Clock(
                    format=' %H:%M',
                    mouse_callbacks={'Button1': lazy.spawn("coretime")},
                    background='#20262C',
                    font="JetBrains Mono Bold",
                ),

                widget.Spacer(length=bar.STRETCH,
                              background='#20262C',
                              ),

                widget.Image(
                    filename='~/.config/qtile/Assets/7.png',
                    background='#20262C',
                ),

                widget.TextBox(
                    fontsize=20,
                    mouse_callbacks={'Button1': lazy.spawn("pavucontrol")},
                    foreground='#82DF94',
                    text='',
                    background='#343A40',
                ),

                widget.PulseVolume(font='JetBrains Mono Bold',
                                   fontsize=12,
                                   padding=5,
                                   background='#343A40',
                                   ),

                widget.TextBox(
                    fontsize=20,
                    foreground='#82DF94',
                    text='',
                    background='#343A40',
                ),

                widget.Net(
                    fontsize=12,
                    font='JetBrains Mono Bold',
                    mouse_callbacks={'Button1': lazy.spawn("alacritty -e nmtui")},
                    format='{down} ↓↑ {up}',
                    padding=1,
                    use_bits=True,
                    background='#343A40',

                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/8.png',
                    background='#343A40',
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/7.png',
                ),

                widget.Systray(
                    background='#343A40',
                    iconsize=20,
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/8.png',
                    background='#343A40',
                ),

                widget.TextBox(
                    fontsize=26,
                    mouse_callbacks={'Button1': lazy.spawn("/home/juftuf/.config/rofi/applets/applets/powermenu.sh")},
                    foreground='#82DF94',
                    text='襤',
                    background='#20262C',
                ),
                widget.Spacer(
                    length=18,
                    background='#20262C',
                ),

            ],
            35,
            margin=[0, -10, 6, -10]
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    # Drag([mod], "Button1", lazy.window.set_position(), start=lazy.window.get_position()),
    # Drag([mod], "Button3", lazy.window.set_size(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus='#9EE9EA',
    border_normal='#343A40',
    border_width=2,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="zenmonitor"),
        Match(wm_class="qalculate-gtk"),
        Match(wm_class="file-roller"),
        Match(wm_class="gthumb"),
        Match(wm_class="obs"),
    ]
)


# Startup script
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('/home/juftuf/.config/qtile/autostart')  # path to my script, under my user directory
    subprocess.call([home])


auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
