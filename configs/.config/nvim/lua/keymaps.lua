-- Space bar leader key
vim.g.mapleader = " "

-- Yank to clipboard
vim.keymap.set({"n", "v"}, "<leader>y", [["+y]])
-- Yank line to clipboard
vim.keymap.set("n", "<leader>Y", [["+Y]])

-- Gitsign stuff
vim.keymap.set("n", "<leader>gp", ":Gitsign preview_hunk", {})
vim.keymap.set("n", "<leader>gd", ":Gitsign toggle_current_line_blame", {})

-- Neotree stuff
vim.keymap.set("n", "<C-s>", ":Neotree filesystem reveal left<CR>", {})
vim.keymap.set("n", "<leader>bf", ":Neotree buffers reveal float<CR>", {})

-- Autoformat the buffer
vim.keymap.set("n", "<leader>gf", vim.lsp.buf.format, {})

-- Telescope stuff
local builtin = require("telescope.builtin")
vim.keymap.set("n", "<C-p>", builtin.find_files, {})
vim.keymap.set("n", "<leader>fg", builtin.live_grep, {})
vim.keymap.set("n", "<leader><leader>", builtin.oldfiles, {})
