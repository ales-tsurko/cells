# Cells

Live coder's editor/IDE. Use SuperCollider, Python, Tidal Cycles etc. in
 the same project.




## Build

You need Python and [poetry](https://github.com/sdispater/poetry).

First, you need to install the dependencies:
```
poetry install
```

Then you can run project:
```
poetry run cells
```




## Status

### Version 1.0

It's ~90% ready for alpha. But there are some important points:

I chose Python to get the first version quick and to look at the design
at a high level, without going deep into details. And without tests. And with
imperfect code quality... So the first version is going to be more like a prototype. But ready-to-use
working prototype though, developed with live performance stability in mind.

After I'll finish the programm, these things still have to be done for the v1.0:

* [ ] website
* [ ] documentation
* [ ] theming
* [ ] packaging/deployment configuration

I'm going to finish the v1.0-beta until November, 19.




### Version 1.1.0

For the next version I'm going to rewrite it in Rust with all the good 
development practice applied (testing, code quality, low coupled design etc.)

I'm also thinking of next features:

- more color themes, maybe user color themes support
- project templates
- backups
- cells browser (save/re-use cells between projects, maybe make a centralized place, where users could share them)
- support MIDI (to use Launchpad to run and select cells, for example, would be great)
- better mouse support
- one or even two more cool secret features