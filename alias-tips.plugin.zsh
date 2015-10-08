PLUGIN_DIR=$(dirname $0)

#export ZSH_PLUGINS_ALIAS_TIPS_TEXT="💡 Alias tip: "
#export ZSH_PLUGINS_ALIAS_TIPS_EXCLUDES="_ c"
#export ZSH_PLUGINS_ALIAS_TIPS_EXPAND=1

preexec() {
  alias | ${PLUGIN_DIR}/alias-tips $*
}
