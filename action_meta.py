registry = {}

class action (object):
    class __metaclass__ (type):
        def __init__ (klass, name, bases, attrs):
            registry[name] = klass
            type.__init__ (name, bases, attrs)

    @staticmethod
    def add_arguments (p):
        pass

    def __init__ (self, args):
        self.args = args

    def disabled (*args):
        pass

    def force_expired (*args):
        pass

    def inactive (*args):
        pass

    def expired (*args):
        pass

    def warn (*args):
        pass

    def ok (*args):
        pass
