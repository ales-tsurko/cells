# Cells

[![Cells — Live Coding Environment](https://img.youtube.com/vi/S0QfVc6bMhg/0.jpg)](https://www.youtube.com/watch?v=S0QfVc6bMhg)

Cells is a live and creative coding environment. It allows you to organize
code into runnable snippets and mix programming languages.

You can use it as a sequencer, effect processor, DAW, for
generative/interactive installations, prototyping, visuals, and more.

Cells supports:
- Clojure 
- Common Lisp (SBCL)
- Haskell
- Lua
- Node.js
- Overtone
- Python
- Ruby
- Scheme (Chez)
- SuperCollider
- Swift
- TidalCycles




## Build/Run

You need Python and [poetry](https://github.com/sdispater/poetry).

First, you need to install dependencies:
```
poetry install
```

Then:
```
poetry run cells -d
```




## Deploy

Update version in `settings.py` and `.github/main.yml` then run:

```
./packaging/macos/publish.sh <version>
```




## Status

### Version 1.0.0

~~It's about 90% ready for alpha.~~ v1.0.0-beta is ready. But there are some important points:

I chose Python to get the first version quickly and to look at the design
at a high level, without going deep into details. And without tests. And with
imperfect code quality... So the first version is going to be more like a prototype. But ready-to-use
working prototype though, developed with live performance stability in mind.


### Version 1.1.0

For the next version I'm going to rewrite it in Rust with all the good 
development practice applied (testing, code quality, low coupled design etc.)

I'm also thinking of the next features:

- more color themes, maybe user color themes support
- project templates
- backups
- cells browser (save/re-use cells between projects, maybe make a centralized place, where users could share them)
- support MIDI (to use Launchpad to run and select cells, for example, would be great)
- better mouse support
- one or even two more cool secret features
