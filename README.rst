stashy
======

Python API client for the Atlassian Stash REST API

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

-  Retrieve all groups

::

    stash.admin.groups.list()

-  Retrieve all users that match a given filter

::

    stash.admin.users.list(filter="admin")

-  Add a user to a group

::

    stash.admin.groups.add_user('stash-users', 'admin')

-  Iterate over all projects (that you have access to)

::

    stash.projects.list()

-  List all the repositories in a given project

::

    stash.projects[PROJECT].repos.list()

-  List all the commits in a pull request

::

    list(stash.projects[PROJECT].repos[REPO].pull_requests.commits())

Implemented
-----------

::

    /admin/groups [DELETE, GET, POST]
    /admin/groups/add-user [POST]
    /admin/groups/more-members [GET]
    /admin/groups/more-non-members [GET]
    /admin/groups/remove-user [POST]
    /admin/users [GET, POST, DELETE, PUT]
    /admin/users/add-group [POST]
    /admin/users/credentials [PUT]
    /admin/users/more-members [GET]
    /admin/users/more-non-members [GET]
    /admin/users/remove-group [POST]
    /admin/permissions/groups [GET, PUT, DELETE]
    /admin/permissions/groups/none [GET]
    /admin/permissions/users [GET, PUT, DELETE]
    /admin/permissions/users/none [GET]
    /groups [GET]
    /projects [POST, GET]
    /projects/{projectKey} [DELETE, PUT, GET]
    /projects/{projectKey}/permissions/groups [GET, PUT, DELETE]
    /projects/{projectKey}/permissions/groups/none [GET]
    /projects/{projectKey}/permissions/users [GET, PUT, DELETE]
    /projects/{projectKey}/permissions/users/none [GET]
    /projects/{projectKey}/permissions/{permission}/all [GET, POST]
    /projects/{projectKey}/repos [POST, GET]
    /projects/{projectKey}/repos/{repositorySlug} [DELETE, POST, PUT, GET]
    /projects/{projectKey}/repos/{repositorySlug}/branches [GET]
    /projects/{projectKey}/repos/{repositorySlug}/branches/default [GET, PUT]
    /projects/{projectKey}/repos/{repositorySlug}/changes [GET]
    /projects/{projectKey}/repos/{repositorySlug}/commits [GET]
    /projects/{projectKey}/repos/{repositorySlug}/pull-requests [GET, POST]
    /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId} [GET, PUT]
    /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/activities [GET]
    /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/decline [POST]
    /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/merge [GET, POST]
    /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/reopen [POST]
    /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/approve [POST, DELETE]
    /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/changes [GET]
    /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/commits [GET]
    /projects/{projectKey}/repos/{repositorySlug}/settings/hooks [GET]
    /projects/{projectKey}/repos/{repositorySlug}/settings/hooks/{hookKey} [GET]
    /projects/{projectKey}/repos/{repositorySlug}/settings/hooks/{hookKey}/enabled [PUT, DELETE]
    /projects/{projectKey}/repos/{repositorySlug}/settings/hooks/{hookKey}/settings [PUT, GET]
    /projects/{projectKey}/repos/{repositorySlug}/tags [GET]

Not yet implemented
-------------------

::

    /admin/mail-server [DELETE]
    /application-properties [GET]
    /hooks/{hookKey}/avatar [GET]
    /logs/logger/{loggerName} [GET]
    /logs/logger/{loggerName}/{levelName} [PUT]
    /logs/rootLogger [GET]
    /logs/rootLogger/{levelName} [PUT]
    /markup/preview [POST]
    /profile/recent/repos [GET]
    /projects/{projectKey}/avatar.png [GET, POST]
    /projects/{projectKey}/repos/{repositorySlug}/recreate [POST]
    /projects/{projectKey}/repos/{repositorySlug}/browse [GET]
    /projects/{projectKey}/repos/{repositorySlug}/browse/{path:.*} [GET]
    /projects/{projectKey}/repos/{repositorySlug}/commits/{changesetId:.*} [GET]
    /projects/{projectKey}/repos/{repositorySlug}/diff/{path:.*} [GET]
    /projects/{projectKey}/repos/{repositorySlug}/files [GET]
    /projects/{projectKey}/repos/{repositorySlug}/files/{path:.*} [GET]
    /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/comments [POST]
    /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/comments/{commentId} [DELETE, PUT, GET]
    /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/diff [GET]
    /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/diff/{path:.*} [GET]
    /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/participants [GET, DELETE, POST]
    /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/watch [POST, DELETE]
    /users [GET, PUT]
    /users/credentials [PUT]

