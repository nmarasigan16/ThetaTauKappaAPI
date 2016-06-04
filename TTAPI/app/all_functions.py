#space for includes if necessary


"""
returns the amount of hours fulfilled by a person
@param:
    user to check
@return:
    dictionary with keys of type of hours, values of how many fulfilled
"""
def format_reqs(user):
    reqs = {}
    reqs['professional'] = user.hours.professional
    reqs['philanthropy'] = user.hours.philanthropy
    reqs['brotherhood'] = user.hours.brotherhood
    if user.status == 'P':
        #assemble requirements for pledges in dictionary
        pledge = user.pledge
        reqs['pledge family'] = pledge.family
        reqs['brother signatures'] = pledges.brother
        reqs['pledge signatures'] = pledges.pledge
    elif user.status == 'B':
        #assemble requirements for brother in dictionary
        brother = user.brother
        reqs['GMs'] = brother.gms
    else:
        return {"silly goose": "You have no requirements"}
    return reqs


"""
Adds hours to user and adds user to event
@param:
    user to add events to
    event to add
    number of hours to add, if -1 then duration of event
@return:
    boolean indicating success or failure in adding
"""
def adder(user, event, h):
    hours = float(h)
    if hours == 0.0:
        hours = event.duration

    if event.etype == 'PR':
        user.hours.professional += hours
    if event.etype == 'BR':
        user.hours.brotherhood += hours
    if event.etype == 'PH':
        user.hours.philanthropy += hours

    user.hours.events.add(event)
    user.hours.save()
    return True





