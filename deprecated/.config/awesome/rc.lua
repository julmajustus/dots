pcall(require, "luarocks.loader")

-- Standard awesome library
require("awful.autofocus")

-- Theme handling library
local beautiful = require("beautiful")

-- Themes :

-- choose your theme here
local accents = {
    "otis-forest",			-- 1
    "kripton",				-- 2
    "hornet",				-- 3
	"cherry-blossom",		-- 4
	"matcha-sea",			-- 5
	"matcha",				-- 6
}
-- choose your theme here
local chosen_accents = accents[2]
local theme_path = string.format("%s/.config/awesome/themes/accents/%s.lua", os.getenv("HOME"), chosen_accents)
beautiful.init(theme_path)

-- Configs :

-- Notifications :
require("ui.notifications")

-- keybinds :
require("configuration.keys")

-- Layouts :
require("configuration.layouts")

-- Rules :
require("configuration.rules")

-- Titlebars :
-- require("ui.titlebar-top")


-- Menu :
require("ui.menu")

-- Bar :
require("ui.bar")


