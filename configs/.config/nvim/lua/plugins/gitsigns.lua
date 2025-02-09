return {
	{
		"tpope/vim-fugitive",
	},
	{
		"lewis6991/gitsigns.nvim",
		config = function()
			require("gitsigns").setup()
		end,

		vim.keymap.set("n", "<leader>gp", ":Gitsign preview_hunk", {}),
		vim.keymap.set("n", "<leader>gp", ":Gitsign toggle_current_line_blame", {}),
	},
}
