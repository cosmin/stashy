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

    list(stash.admin.groups.all())

-  Retrieve all users that match a given filter

::

    list(stash.admin.users.all(filter="admin"))

-  Add a user to a group

::

    stash.admin.groups.add_user('stash-users', 'admin')

-  Iterate over all projects (that you have access to)

::

    list(stash.projects)

-  List all the repositories in a given project

::

    list(stash.projects[PROJECT].repos.all())

-  List all the commits in a pull request

::

    list(stash.projects[PROJECT].repos[REPO].pull_requests.commits())

Status
------

The following are all the API 1.0 REST endpoints in Stash that have been
implement, with the remainder included using [STRIKEOUT:striketrough]
for completeness.

-  /admin/groups [DELETE, GET, POST]
-  /admin/groups/add-user [POST]
-  /admin/groups/more-members [GET]
-  /admin/groups/more-non-members [GET]
-  /admin/groups/remove-user [POST]
-  /admin/users [GET, POST, DELETE, PUT]
-  /admin/users/add-group [POST]
-  /admin/users/credentials [PUT]
-  /admin/users/more-members [GET]
-  /admin/users/more-non-members [GET]
-  /admin/users/remove-group [POST]
-  [STRIKEOUT:/admin/mail-server [DELETE]]
-  /admin/permissions/groups [GET, PUT, DELETE]
-  /admin/permissions/groups/none [GET]
-  /admin/permissions/users [GET, PUT, DELETE]
-  /admin/permissions/users/none [GET]
-  [STRIKEOUT:/application-properties [GET]]
-  /groups [GET]
-  [STRIKEOUT:/hooks/{hookKey}/avatar [GET]]
-  [STRIKEOUT:/logs/logger/{loggerName} [GET]]
-  [STRIKEOUT:/logs/logger/{loggerName}/{levelName} [PUT]]
-  [STRIKEOUT:/logs/rootLogger [GET]]
-  [STRIKEOUT:/logs/rootLogger/{levelName} [PUT]]
-  [STRIKEOUT:/markup/preview [POST]]
-  [STRIKEOUT:/profile/recent/repos [GET]]
-  /projects [POST, GET]
-  /projects/{projectKey} [DELETE, PUT, GET]
-  [STRIKEOUT:/projects/{projectKey}/avatar.png [GET, POST]]
-  /projects/{projectKey}/permissions/groups [GET, PUT, DELETE]
-  /projects/{projectKey}/permissions/groups/none [GET]
-  /projects/{projectKey}/permissions/users [GET, PUT, DELETE]
-  /projects/{projectKey}/permissions/users/none [GET]
-  /projects/{projectKey}/permissions/{permission}/all [GET, POST]
-  /projects/{projectKey}/repos [POST, GET]
-  /projects/{projectKey}/repos/{repositorySlug} [DELETE, POST, PUT,
   GET]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/recreate
   [POST]]
-  /projects/{projectKey}/repos/{repositorySlug}/branches [GET]
-  /projects/{projectKey}/repos/{repositorySlug}/branches/default [GET,
   PUT]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/browse
   [GET]]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/browse/{path:.\*}
   [GET]]
-  /projects/{projectKey}/repos/{repositorySlug}/changes [GET]
-  /projects/{projectKey}/repos/{repositorySlug}/commits [GET]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/commits/{changesetId:.\*}
   [GET]]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/diff/{path:.\*}
   [GET]]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/files [GET]]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/files/{path:.\*}
   [GET]]
-  /projects/{projectKey}/repos/{repositorySlug}/pull-requests [GET,
   POST]
-  /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}
   [GET, PUT]
-  /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/activities
   [GET]
-  /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/decline
   [POST]
-  /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/merge
   [GET, POST]
-  /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/reopen
   [POST]
-  /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/approve
   [POST, DELETE]
-  /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/changes
   [GET]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/comments
   [POST]]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/comments/{commentId}
   [DELETE, PUT, GET]]
-  /projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/commits
   [GET]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/diff
   [GET]]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/diff/{path:.\*}
   [GET]]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/participants
   [GET, DELETE, POST]]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}/watch
   [POST, DELETE]]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/settings/hooks
   [GET]]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/settings/hooks/{hookKey}
   [GET]]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/settings/hooks/{hookKey}/enabled
   [PUT, DELETE]]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/settings/hooks/{hookKey}/settings
   [PUT, GET]]
-  [STRIKEOUT:/projects/{projectKey}/repos/{repositorySlug}/tags [GET]]
-  [STRIKEOUT:/users [GET, PUT]]
-  [STRIKEOUT:/users/credentials [PUT]]

