# alias-tips

An oh-my-zsh plugin to help remembering thoses aliases you defined onces.

It works by trying to find an alias for the command you are currently trying to
execute and printing a help line reminding you about that alias.

The idea is that you mind be too afraid to execute aliases defined because you
can't remember them correctly, or just have forgotten about some aliases, or
that aliases for your daily commands actually exist.


# Example

```sh
$ ls -lh
You know you have an alias for that, right? ll
:

$ git gui
You know you have an alias for that, right? gg
:

$ git rebase --interactive master
You know you have an alias for that, right? gri master
:
```

# Installation

## antigen
1. Add `antigen bundle djui/alias-tips` to your `.zshrc` with your other antigen bundle commands.

## oh-my-zsh

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


# Usage

After installation re-source your `.zshrc`.

The help string can be configured exporting an environment variable, e.g. in
your `.zshrc`:

```sh
:
export ZSH_PLUGINS_ALIAS_TIPS_TEXT="Alias tip: "
:
```
