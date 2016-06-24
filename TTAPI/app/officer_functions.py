from app.models import Brother, Excuse


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
    user.demographics.status='B'
    user.demographics.save()
    new_bro = Brother(user=user)
    new_bro.save()
    user.save()

"""
Checks a members password against a meeting password
@param:
    Attendance object
    meeting password
@return:
    boolean indicating match
"""
def check_password(attendance, password):
    if not attendance.password:
        return False
    return attendance.password == password

"""
Increments members gm count and adds the meeting to their meetings
@param:
    Userprofile object
    meeting object
"""
def add_to_meeting(member, meeting):
    if meeting in member.hours.meetings.all():
        return
    member.hours.meetings.add(meeting)
    member.hours.save()
    member.brother.gms += 1
    member.brother.save()

"""
Makes an excuse object and links it to the user and the meeting
@param
    excuse text
    member whos excuse it is
    meeting for which the excuse is
"""
def add_excuse(excuse, member, meeting):
    excuse_obj = Excuse.objects.create(user=member, meeting=meeting, excuse=excuse)
    excuse_obj.save()

#########################################################################################################
"""
Wrappers
"""
def initiate(pledges):
    for pledge in pledges:
        upgrade(pledge)


"""
Takes attendance for a gm
@param:
    meeting object to take attendance for
    members of the chapter that is taking attendance
@return:
    List object with the user email as the key, excuse as the value
"""
def attendance(members, meeting):
    password = meeting.password
    excuses = {}
    for member in members:
        match = check_password(member.attendance, password)
        if match:
            add_to_meeting(member, meeting)
        elif not not member.attendance.excuse: #lmao
            add_excuse(member.attendance.excuse, member, meeting)
            member.attendance.excuse = ""
            member.attendance.save()
        else:
            x = member.brother.u_absences
            member.brother.u_absences = x+1;
            member.brother.save()
    return excuses

