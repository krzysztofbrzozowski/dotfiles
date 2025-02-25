return {
    "goolord/alpha-nvim",
    dependencies = {
        "nvim-tree/nvim-web-devicons",
    },

    config = function()
        local alpha = require("alpha")
        local dashboard = require("alpha.themes.dashboard")

        dashboard.section.header.val = {
            [["Elo"]],
        }

        dashboard.section.buttons.val = {
            dashboard.button("p", "  Find project", ":Telescope projects <CR>"),
            dashboard.button("n", "  New file", ":ene <BAR> startinsert <CR>"),
            dashboard.button("k", "Keybindings", ":e ~/.config/nvim/lua/keymaps.lua<CR>"),
            dashboard.button("q", "Quit Neovim", ":qa<CR>"),
        }

        alpha.setup(dashboard.opts)
    end,
}
