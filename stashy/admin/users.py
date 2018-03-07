from ..helpers import ResourceBase, FilteredIterableResource
from ..errors import ok_or_error, response_or_error
from ..compat import update_doc

class Users(ResourceBase, FilteredIterableResource):
    @response_or_error
    def add(self, name, password, displayName, emailAddress, addToDefaultGroup=True):
        """
        Add a user, returns a dictionary containing information about the newly created user
        """
        params = dict(name=name,
                    password=password,
                    displayName=displayName,
                    emailAddress=emailAddress,
                    addToDefaultGroup=addToDefaultGroup)

        return self._client.post(self.url(), params=params)

    @ok_or_error
    def delete(self, user):
        """
        Delete a user.
        """
        return self._client.delete(self.url(), params=dict(name=user))

    @response_or_error
    def update(self, name, displayName=None, emailAddress=None):
        """
        Update the user information, and return the updated user info.

        None is used as a sentinel value, use empty string if you mean to clear.
        """

        data = dict(name=name)
        if displayName is not None:
            data['displayName'] = displayName
        if data is not None:
            data['emailAddress'] = emailAddress

        return self._client.put(self.url(), data)

    @ok_or_error
    def credentials(self, name, new_password):
        """
        Update a user's password.
        """

        data = dict(name=name, password=new_password, passwordConfirm=new_password)
        return self._client.put(self.url(), data)

    @ok_or_error
    def add_group(self, user, group):
        """
        Add the given group to the given user.
        """
        return self._client.post(self.url("/add-group"), dict(context=user, itemName=group))

    @ok_or_error
    def remove_group(self, user, group):
        """
        Remove the given group from the given user.
        """
        return self._client.post(self.url("/remove-group"), dict(context=user, itemName=group))

    def more_members(self, user, filter=None):
        """
        Retrieves a list of groups the specified user is a member of.

        filter: if specified only groups with names containing the supplied string will be returned
        """
        params = dict(context=user)
        if filter:
            params['filter'] = filter
        return self.paginate("/more-members", params)

    def more_non_members(self, user, filter=None):
        """
        Retrieves a list of groups that the specified user is not a member of

        filter: if specified only groups with names containing the supplied string will be returned
        """
        params = dict(context=user)
        if filter:
            params['filter'] = filter
        return self.paginate("/more-non-members", params)


update_doc(Users.all, """
Returns an iterator that will walk all the users, paginating as necessary.

filter: return only users with usernames, display name or email addresses containing the supplied string
""")
