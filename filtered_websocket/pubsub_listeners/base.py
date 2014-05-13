class BasePubSubListener(object):

    def kill(self):
        """
        Any operations required to kill the thread in which listen runs.
        """
        raise NotImplementedError

    def listen(self, *args, **kwargs):
        """
        Any operations required to listen for pubsub events.
        Assumed to be a blocking loop, and, as such, is run in it's own thread.
        """
        raise NotImplementedError
