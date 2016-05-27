_alias_tips__PLUGIN_DIR=${0:a:h}

#export ZSH_PLUGINS_ALIAS_TIPS_TEXT="💡 Alias tip: "
#export ZSH_PLUGINS_ALIAS_TIPS_EXCLUDES="_ c"
#export ZSH_PLUGINS_ALIAS_TIPS_EXPAND=1

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

  echo $git_aliases $shell_aliases | ${_alias_tips__PLUGIN_DIR}/alias-tips $*
}

autoload -Uz add-zsh-hook
add-zsh-hook preexec _alias_tips__preexec
