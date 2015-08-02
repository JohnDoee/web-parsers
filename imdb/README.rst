IMDB Parser
===========

Library to parse `IMDB <hhttp://www.imdb.com/>`_ pages.

Help and stuff
--------------
https://github.com/JohnDoee (there is an email here)

Example
-------

.. code-block:: python

    >>> from imdbparser import IMDB
    >>> imdb = IMDB()
    >>> movie = imdb.get_movie(1954470)
    >>> movie.fetched
    False
    >>> movie.fetch()
    >>> movie.fetched
    >>> movie.__dict__
    ...

License
-------
See LICENSE
