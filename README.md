# alias-tips

[![Build Status](https://travis-ci.org/djui/alias-tips.svg)](https://travis-ci.org/djui/alias-tips)

A Zsh plugin to help remembering those shell aliases and Git aliases you once
defined.

Works with [Oh My Zsh](#oh-my-zsh), [Fig](#fig), [zplug](#zplug), [antigen](#antigen), [zgen](#zgen), [Arch Linux](#arch-linux), or [pure Zsh](#zsh).

It works by trying to find an shell or Git alias for the command you are
currently executing and printing a help line reminding you about that alias.

The idea is that you might be too afraid to execute aliases defined because you
can't remember them correctly, or just have forgotten about some aliases, or
that aliases for your daily commands even exist.


# Example

```sh
$ ls -lh
Alias tip: ll
:

$ git gui
Alias tip: gg
:

$ git rebase --interactive master
Alias tip: grbi master
:

$ git status
Alias tip: g st
:
```


# Installation

## [Oh My Zsh](https://github.com/robbyrussell/oh-my-zsh)

1. Get it

    Go to your custom plugins folder:

    ```sh
    $ cd ${ZSH_CUSTOM1:-$ZSH/custom}/plugins
    ```

    Then either clone:

    ```sh
    $ git clone https://github.com/djui/alias-tips.git
    ```

    Or download:

    ```sh
    $ wget https://github.com/djui/alias-tips/archive/master.zip
    $ unzip master.zip && mv alias-tips-master alias-tips && rm master.zip
    ```

    Or add it as submodule:

    ```sh
    $ git submodule add https://github.com/djui/alias-tips
    $ git submodule update --init
    ```

2. Include it

    Then add the plugin to your plugin list in oh-my-zsh configuration:

    ```sh
    $ $EDITOR ~/.zshrc

    # -plugins=(...)
    # +plugins=(... alias-tips)
    ```


## Fig

[Fig](https://fig.io) adds apps, shortcuts, and autocomplete to your existing terminal.

Install `alias-tips` in just one click.

<a href="https://fig.io/plugins/other/alias-tips_djui" target="_blank"><img src="https://fig.io/badges/install-with-fig.svg" /></a>


## [zplug](https://github.com/zplug/zplug)

1. Add `zplug "djui/alias-tips"` to your `.zshrc`
2. Install it with `zplug install`


## [Antigen](https://github.com/zsh-users/antigen)

1. Add `antigen bundle djui/alias-tips` to your `.zshrc` with your other antigen
   bundle commands.


## [zgen](https://github.com/tarjoilija/zgen)

1. Add `zgen load djui/alias-tips` to your `.zshrc`
2. Regenerate your `init.zsh` with `zgen save`


## Arch Linux

1. Install [`alias-tips-git`](https://aur.archlinux.org/packages/alias-tips-git/) from the [AUR](https://wiki.archlinux.org/index.php/Arch_User_Repository).

2. Add the following to your `.zshrc`:

    ```sh
    source /usr/share/zsh/plugins/alias-tips/alias-tips.plugin.zsh
    ```

3. Start a new terminal session.


## Zsh

1. Get it `git clone https://github.com/djui/alias-tips.git`
2. Add `source alias-tips/alias-tips.plugin.zsh` to your `.zshrc`.


# Usage

After installation re-source your `.zshrc`.


## Customizations

### Customize the Output

The help string can be configured exporting an environment variable, e.g. in
your `.zshrc`:

```sh
:
export ZSH_PLUGINS_ALIAS_TIPS_TEXT="Alias tip: "
:
```


### Exclude some Aliases

A list of aliases to be excluded from being reminded of can be configured
exporting an environment variable of space separated aliases, e.g. in your
`.zshrc`:

```sh
:
export ZSH_PLUGINS_ALIAS_TIPS_EXCLUDES="_ ll vi"
:
```


### Disable Command Expansion

If you have several alias, e.g. for different git commands the command get
expanded before looking for an alias.

Example:

```sh
alias gRv='git remote -v'
alias gR='git remote'
```

Without the expand option `gR -v` will execute without a tip, with expand, it
will suggest `gRv`.

If this may not be desired, the behaviour can be disabled by setting the
environment variable, e.g. in your .zshrc:

```sh
:
export ZSH_PLUGINS_ALIAS_TIPS_EXPAND=0
:
```


### Force Alias Use

If you want to force yourself to use the aliases you set you can enable this
option through this environmental variable:

```sh
:
export ZSH_PLUGINS_ALIAS_TIPS_FORCE=1
:
```

This will cause alias-tips to abort the command you have entered if there exists
an alias for it.


### Reveal Command

If you want to reveal aliased command, e.g. to demonstrate your shell to someone else
you can enable this option through this environmental variable:

```sh
:
export ZSH_PLUGINS_ALIAS_TIPS_REVEAL=1
:
```

Use this environmental variable to customize text:

``````sh
:
export ZSH_PLUGINS_ALIAS_TIPS_REVEAL_TEXT="Alias tip: "
:
``````

And this to exclude some obvious expansions:

``````sh
:
export ZSH_PLUGINS_ALIAS_TIPS_REVEAL_EXCLUDES=(_ ll vi)
:
``````



# Limitations

- *Suffix* and *Global* aliases are currently not supported. Only *Prefix*
  aliases ("command position") are supported. Check the
  [Zsh manual](http://zsh.sourceforge.net/Doc/Release/Shell-Builtin-Commands.html#Shell-Builtin-Commands)
  on `alias` for their definition.
- Multiline aliases (aliases which definition span multiple lines) are not
  supported. Currently their first line only will be used (likely incorrectly)


# FAQ

**Q:** *Why only Zsh?*

**A:** This works because of feature in Zsh called
[preexec](http://zsh.sourceforge.net/Doc/Release/Functions.html). Other shells,
e.g. Bash, do not have this feature. There are
workarounds[[1](https://github.com/rcaloras/bash-preexec),[2](http://www.twistedmatrix.com/users/glyph/preexec.bash.txt)]
but integrating these is a task left for the reader.


# Testing

    $ python  -m unittest test_alias-tips
    $ python3 -m unittest test_alias-tips


# Contributing

See: [CONTRIBUTIONS.md](CONTRIBUTIONS.md).
