PLUGIN_DIR=$(dirname $0)

preexec() {
  alias | ${PLUGIN_DIR}/alias-tips $*
}
