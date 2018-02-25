"""API Helpers for Stream Tweeter."""

from model import StreamSession, SentTweet


def create_streams_payload(user, dt=None, limit=5):
    """Creates payload for returning stream session info."""

    payload = {}

    if dt:
        streams = [stream.serialize
                   for stream
                   in user.sessions.filter(
                       StreamSession.started_at < dt
                       )[:limit]]
    else:
        streams = [stream.serialize
                   for stream
                   in user.sessions[:limit]]

    # Get timestamp to be used as cursor
    next_ts = streams[-1]["startedAt"]

    # Add data to payload.
    payload["streams"] = streams
    payload["next"] = f"/api/streams?ts={next_ts}&limit={limit}"

    return(payload)


def create_senttweets_payload(user, started, ended):
    """Creates payload for returning tweets created between given times."""

    payload = {}

    tweets = [tweet.serialize
              for tweet
              in user.sent_tweets.filter(SentTweet.created_at.between(
                  started, ended
              ))]

    payload["tweets"] = tweets

    return(payload)
