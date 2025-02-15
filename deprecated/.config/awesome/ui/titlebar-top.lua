-- ## Titlebars ##
-- ~~~~~~~~~~~~~~~

-- requirements
-- ~~~~~~~~~~~~
local gears = require("gears")
local awful = require("awful")
local wibox = require("wibox")
local beautiful = require("beautiful")
local gears = require("gears")
local dpi = beautiful.xresources.apply_dpi


----- Titlebar/s -----
client.connect_signal("request::titlebars", function(c)
    -- buttons for the titlebar
    local buttons = {
        awful.button({ }, 1, function()
            c:activate { context = "titlebar", action = "mouse_move"  }
        end),
        awful.button({ }, 3, function()
            c:activate { context = "titlebar", action = "mouse_resize"}
        end),
    }

    -- Set the titlebar :
    local titlebar = awful.titlebar(c, {
	size = dpi(30),
	position = 'top',
    })

    -- Titlebar :
    titlebar:setup {

	{
		{
			{ -- Left
				awful.titlebar.widget.iconwidget(c),
				buttons = buttons,
				layout  = wibox.layout.fixed.horizontal
			},
			
			{ -- Middle
				{ -- Title
					align  = 'center',
					widget = awful.titlebar.widget.titlewidget(c)
				},
				buttons = buttons,
				layout  = wibox.layout.flex.horizontal
			},
			
			{-- Right
				--awful.titlebar.widget.floatingbutton (c),
				awful.titlebar.widget.minimizebutton (c),
				awful.titlebar.widget.maximizedbutton(c),
				awful.titlebar.widget.closebutton    (c),
				--awful.titlebar.widget.stickybutton   (c),
				--awful.titlebar.widget.ontopbutton    (c),
				spacing = dpi(6),
				layout = wibox.layout.fixed.horizontal,
			},
			layout = wibox.layout.align.horizontal,
		},
		margins = { top = dpi(6), bottom = dpi(6), left = dpi(6), right = dpi(6)},
		widget = wibox.container.margin,
	},
	id = 'background_role',
	widget = wibox.container.background,
    }
end)
