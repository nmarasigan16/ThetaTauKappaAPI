
"""
Helper functions
"""

"""
Checks if a person is a certain status
@param
    User to check
    status to check for
@return
    Boolean value of check.
    True if brother is status, false if not
"""
def status_check(user, status):
    if(user.demographics.status == status):
        return True
    return False

"""
Initiate function.  Deletes a users pledge instance and
initializes a brother instance linked to the user
@param
    User to initiate
"""
def upgrade(user):
    user.pledge.delete()
    new_bro = Brother(user=user)
    new_bro.save()




"""
Wrappers
"""
def initiate(members):
    for member in members:
        if(status_check(member, 'P') == True):
            upgrade(member)



