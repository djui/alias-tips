_alias_tips__PLUGIN_DIR=$(dirname $0)

#export ZSH_PLUGINS_ALIAS_TIPS_TEXT="💡 Alias tip: "
#export ZSH_PLUGINS_ALIAS_TIPS_EXCLUDES="_ c"
#export ZSH_PLUGINS_ALIAS_TIPS_EXPAND=1

_alias_tips__preexec () {
  alias | ${_alias_tips__PLUGIN_DIR}/alias-tips $*
}

autoload -Uz add-zsh-hook
add-zsh-hook preexec _alias_tips__preexec
