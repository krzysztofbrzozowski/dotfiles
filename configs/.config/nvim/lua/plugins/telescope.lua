return {
  {
    "nvim-telescope/telescope-ui-select.nvim",
  },
  {
    "nvim-telescope/telescope.nvim",
    tag = "0.1.8",
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function()
      require("telescope").setup({
        defaults = {
	  file_ignore_patterns = { "%.git/" },  -- Optional: Ignore .git folder
    	  hidden = true,  -- Show hidden files
	  vimgrep_arguments = {
	    'rg',
	    '--color=never',
		'--no-heading',
      		'--with-filename',
      		'--line-number',
      		'--column',
      		'--smart-case',
      	        '--ignore',
      		'--files',
      		'--hidden',
    		},
	},
	pickers = {
    	  find_files = {
	  hidden = true  -- Ensure `find_files` shows hidden files
    	  }
  	},
	extensions = {
          ["ui-select"] = {
            require("telescope.themes").get_dropdown({}),
          },
        },
      })
      local builtin = require("telescope.builtin")
      vim.keymap.set("n", "<C-p>", builtin.find_files, {})
      vim.keymap.set("n", "<leader>fg", builtin.live_grep, {})
      vim.keymap.set("n", "<leader><leader>", builtin.oldfiles, {})

      require("telescope").load_extension("ui-select")
    end,
  },
}
