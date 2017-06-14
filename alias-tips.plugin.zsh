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
  if hash git 2> /dev/null; then

    # alias.foo bar      => git foo = git bar
    # alias.foo !git bar => git foo = git bar
    git_aliases=$(git config --get-regexp "^alias\." | \
      sed 's/[ ]/ = /' | \
      sed 's/^alias\./git /' | \
      sed 's/ = \([^!]\)/ = git \1/' | \
      sed 's/ = !/ = /')
  fi

  shell_aliases=$(alias)

  shell_functions=$(functions | grep '^[a-zA-Z].\+ () {$')

  echo $shell_functions "\n" $git_aliases "\n" $shell_aliases | \
    python ${_alias_tips__PLUGIN_DIR}/alias-tips.py $*
  ret=$?
  if [[ $ret = 10 ]]; then exit 10; fi
}

autoload -Uz add-zsh-hook
add-zsh-hook preexec _alias_tips__preexec
