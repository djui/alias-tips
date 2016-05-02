_alias_tips__PLUGIN_DIR=$(dirname $0)

#export ZSH_PLUGINS_ALIAS_TIPS_TEXT="💡 Alias tip: "
#export ZSH_PLUGINS_ALIAS_TIPS_EXCLUDES="_ c"
#export ZSH_PLUGINS_ALIAS_TIPS_EXPAND=1

_alias_tips__preexec () {
  if hash git 2> /dev/null; then
    git_aliases=$(\git alias | \
      sed 's/^/git /' | \
      sed 's/ = \([^!]\)/ = git \1/' | \
      sed 's/ = !/ = /')
  fi

  shell_aliases=$(alias)

  echo $git_aliases $shell_aliases | ${_alias_tips__PLUGIN_DIR}/alias-tips $*
}

autoload -Uz add-zsh-hook
add-zsh-hook preexec _alias_tips__preexec
