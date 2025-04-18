Changelog
=========

v1.6
^^^^

v1.6 - v1.6.1
---------------

**Changed**

- Import cycle changed in core. No adjustments are necessary here.

**Fixes**

- Important Bug Fix in ``Core.Instantiate()``. Engine was not returned

v1.5.4 - v1.6
---------------

**New**

- ``@scene``-decorator and ``scene_manager`` added.

**Changed**

- ``core`` structure

- ``core`` must now have at least one scene to run

- removed simple ``start``-func and ``update``-func runtime

- ``Prefab`` base class removed -> engines without ``@scene``-decorator are now prefabs 

**Fixes**

- ``docs``-coroutine code fixed

v1.5
^^^^

v1.5.3 - v1.5.4
---------------

**New**

* Added new example ``grid_navigation.py``

**Documentation and structure update**

* Added ``Navigation`` section -> ``GridNavigation`` and ``NavAgent``

**Bug fixes**

* Fixed ``a_star.py`` ``get_path()`` method. ``open_nodes`` and ``closed_nodes`` are now resetted after each call

v1.5.2 - v1.5.3
---------------

**Bug fixes**

* Structure changed for fixing pip installation
* Code-Reference sprite docu update
* Imports fixed

v1.5.1 - v1.5.2
---------------

**Documentation and structure update**

* Added missing documentation informations of core.py
* Added documentation code copy button
* Added screen_blink.py
* Changed Coroutine Docs, examples added
* Explanation of Surface and Sprites
* Changed SpriteAnimator documentation, SpriteAnimator and Simple sprites are now sections of ``Drawing System with Animations``
* Added new parameter ``surface`` to ``TileMapDrawer.on_enable``
* Added tutorial documentation for draw_system.py
* Changed animation.py -> sprite.py
* Docutils added to ``spaceship.py``
* Gfx/Image handler added:
    * Slicer
    * SizeSlicer
    * AmountSlicer
    * SimpleSprite
    * SimpleImageSprite
    * SimpleSpriteAnimator
    * SpriteDirectoryAnimation
* Example code added:
    * DrawSystem
    * DrawSystemImage
    * DrawSystemAnimationImage
    * DrawSystemAnimationImageSliced
    * DrawSystemAnimationImageSlicedWithPaddings
    * DrawSystemDirectoryAnimationImageSliced
* Example sprites added in ``examples/assets/pixel-adventure/``. Creator: https://pixelfrog-assets.itch.io/pixel-adventure-1

v1.5 - v1.5.1
-------------

**Documentation update**

* Added ``Basic``  doc page
* Bug Fix google meta tag