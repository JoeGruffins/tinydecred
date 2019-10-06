"""
Copyright (c) 2019, Brian Stafford
See LICENSE for details

DcrdataClient.endpointList() for available enpoints.
"""
import urllib.request as urlrequest
from urllib.parse import urlencode
from tinydecred.util import tinyjson
from tinydecred.util.helpers import formatTraceback, getLogger

log = getLogger("HTTP")

def get(uri, **kwargs):
    return request(uri, **kwargs)

def post(uri, data, **kwargs):
    return request(uri, data, **kwargs)

def request(uri, postData=None, headers=None, urlEncode=False):
    try:
        headers = headers if headers else {}
        if postData:
            if urlEncode:
                # encode the data in url query string form, without ?. 
                encoded = urlencode(postData).encode("utf-8")
            else:
                # encode the data as json.
                encoded = tinyjson.dump(postData).encode("utf-8")
            req = urlrequest.Request(uri, headers=headers, data=encoded)
        else:
            req = urlrequest.Request(uri, headers=headers, method="GET")
        raw = urlrequest.urlopen(req).read().decode()
        try:
            # try to decode the response as json, but fall back to just
            # returning the string.
            return tinyjson.load(raw)
        except tinyjson.JSONDecodeError:
            return raw
        except Exception as e:
            raise Exception("JSONError", "Failed to decode server response from path %s: %s : %s" % (uri, raw, formatTraceback(e)))
    except Exception as e:
        log.error("error retrieving %s request for %s" % ("POST" if postData else "GET", uri, e))
        raise Exception("RequestError", "Error encountered in requesting path %s: %s" % (uri, formatTraceback(e)))