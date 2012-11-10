import json
import traceback


from django.template import RequestContext, Context, loader
from django.http import HttpResponse, Http404, HttpResponseBadRequest

import models

def _log(msg, show_traceback=False):
    print msg
    
    if show_traceback:
        traceback.print_exc()
        
        
def _format_response(data):
    """
    Helper function to format a json response from the data given.
    """
    return HttpResponse(json.dumps(data), mimetype="application/json")


def home(request):
    t = loader.get_template("index.html")
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))


def post_login(request):
    return HttpResponse("Loginned!")


def create(request):
    """
    Create a new track page full of awesomeness.
    """
    _log("Creating awesomeness!")
    
    t = loader.get_template("create.html")
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))




##################
###### API
##################

def _get_track(track_id):
    try:
        track = models.Track.objects.get(id=track_id)
        return track
    except models.Track.DoesNotExist:
        error = {"error" : "Track does not exist."}
        raise Http404(json.dumps(error))

def track_details(request, track_id):
    track = _get_track(track_id)
    
    tags = [tag.name for tag in track.tags.all()]
    json_obj = { "id" : track.id,
                 "title" : track.title,
                 "desc" : track.description,
                 "tags" : tags,
                 "level" : track.level,
                 }
    

    return _format_response(json_obj)

def track_items(request, track_id):
    track = _get_track(track_id)
    
    links = []
    for link in track.links.all():
        link_dict = {  "url" : link.url,
                        "type" : link.link_type,
                        "notes" : link.notes,
                        "id" : link.id,
                        "track_id" : track.id,}
        if link.thumb:
            link_dict["thumb"] = link.thumb.url 
        
        links.append(link_dict)
        
    return _format_response(links)

