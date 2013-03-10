.. stashy documentation master file, created by
   sphinx-quickstart on Sun Mar 10 17:38:40 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================
Documentation for stashy
========================

.. rubric:: Python API client for the Atlassian Stash REST API

Installation
------------

::

    pip install stashy

Usage
-----

::

    import stashy
    stash = stashy.connect("http://localhost:7990/stash", "admin", "admin")

Examples
--------

Retrieve all groups::

    stash.admin.groups.list()

Retrieve all users that match a given filter::

    stash.admin.users.list(filter="admin")

Add a user to a group::

    stash.admin.groups.add_user('stash-users', 'admin')

Iterate over all projects (that you have access to)::

    stash.projects.list()

List all the repositories in a given project::

    stash.projects[PROJECT].repos.list()

List all the commits in a pull request::

    list(stash.projects[PROJECT].repos[REPO].pull_requests.commits())

Contents:
---------

.. toctree::
   :maxdepth: 2

   api

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
