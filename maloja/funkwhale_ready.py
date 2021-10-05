# Copyright (c) 2021 Philipp Wolfer <ph.wolfer@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json

from config import plugins
from .funkwhale_startup import PLUGIN


class MalojaException(Exception):
    pass


@plugins.register_hook(plugins.LISTENING_CREATED, PLUGIN)
def submit_listen(listening, conf, **kwargs):
    server_url = conf["server_url"]
    api_key = conf["api_key"]
    if not server_url or not api_key:
        return

    logger = PLUGIN["logger"]
    logger.info("Submitting listening to Majola at %s", server_url)
    payload = get_payload(listening, api_key)
    logger.debug("Majola payload: %r", payload)
    url = server_url.rstrip("/") + "/apis/mlj_1/newscrobble"
    session = plugins.get_session()
    response = session.post(url, payload)
    response.raise_for_status()
    details = json.loads(response.text)
    if details["status"] == "success":
        logger.info("Majola listening submitted successfully")
    else:
        raise MalojaException(response.text)


def get_payload(listening, api_key):
    track = listening.track
    payload = {
        "key": api_key,
        "artists": track.artist.name,
        "title": track.title,
        "time": int(listening.creation_date.timestamp()),
    }

    if track.album:
        payload["album"] = track.album.title

    return payload
