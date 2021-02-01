_alias_tips__PLUGIN_DIR=${0:a:h}

# If alias-tips is loaded from a symlink, then work out
# where the actual file is located
if [[ -L ${0:a} ]]; then
  _alias_tips__PLUGIN_DIR=$(readlink ${0:a})
  _alias_tips__PLUGIN_DIR=${_alias_tips__PLUGIN_DIR:h}
fi

#export ZSH_PLUGINS_ALIAS_TIPS_TEXT="💡 Alias tip: "
#export ZSH_PLUGINS_ALIAS_TIPS_EXCLUDES="_ c"
#export ZSH_PLUGINS_ALIAS_TIPS_EXPAND=0

_alias_tips__preexec () {
  local CMD=$1
  local CMD_EXPANDED=$2
  if [[ $CMD != $CMD_EXPANDED ]] then # Alias is used
    if [[ ${ZSH_PLUGINS_ALIAS_TIPS_REVEAL-0} == 1 ]] \
    && [[ ${${ZSH_PLUGINS_ALIAS_TIPS_REVEAL_EXCLUDES-()}[(I)$1]} == 0 ]] then # Reveal cmd
        local reveal_text=${ZSH_PLUGINS_ALIAS_TIPS_REVEAL_TEXT-Alias for: }
        local color_dark_gray='\e[1;30m'
        local color_reset='\e[0m'
        echo -e "$color_dark_gray$reveal_text$CMD_EXPANDED $color_reset"
    fi
    if [[ ${ZSH_PLUGINS_ALIAS_TIPS_EXPAND-1} == 0 ]] then
      return 0
    fi
  fi

  if hash git 2> /dev/null; then

    # alias.foo bar      => git foo = git bar
    # alias.foo !git bar => git foo = git bar
    local git_aliases
    git_aliases=$(git config --get-regexp "^alias\." | \
      \sed 's/[ ]/ = /' | \
      \sed 's/^alias\./git /' | \
      \sed 's/ = \([^!]\)/ = git \1/' | \
      \sed 's/ = !/ = /')
  fi

  local shell_aliases
  shell_aliases=$(\alias)

  local shell_functions
  shell_functions=$(\functions | \egrep '^[a-zA-Z].+ \(\) \{$')

  # Exit code returned from python script when we want to force use of aliases.
  local force_exit_code=10
  echo $shell_functions "\n" $git_aliases "\n" $shell_aliases | \
    python3 ${_alias_tips__PLUGIN_DIR}/alias-tips.py $*
  local ret=$?
  if [[ $ret = $force_exit_code ]]; then kill -s INT $$ ; fi
}

autoload -Uz add-zsh-hook
add-zsh-hook preexec _alias_tips__preexec
