import pwd
import socket
import subprocess
import sys

from action_meta import action

class list (action):
    help = 'list accounts and their status'

    @staticmethod
    def add_arguments (p):
        p.add_argument ('-a', '--all', dest='all', action='store_true', help='Include disabled/ok accounts in output')

    def disabled (self, spwd):
        if self.args.all:
            print spwd.sp_nam, 'disabled'

    def force_expired (self, spwd):
        print spwd.sp_nam, 'force_expired'

    def inactive (self, spwd):
        print spwd.sp_nam, 'inactive'

    def expired (self, spwd, until_inactive):
        print spwd.sp_nam, 'expired'

    def warn (self, spwd, until_expire):
        print spwd.sp_nam, 'warn'

    def ok (self, spwd):
        if self.args.all:
            print spwd.sp_nam, 'ok'

class warnmail (action):
    help = 'send mail to expired and expiring accounts'

    def mail (self, user, subject, body):
        try:
            p = subprocess.Popen (['sendmail', '-ti'], stdin=subprocess.PIPE)
        except Exception, e:
            print >> sys.stderr, e
            return

        o, e = p.communicate (
'''To: %s
Subject: %s

%s
-- 
account aging report''' % (user, subject, body)
        )
        if p.returncode != 0:
            print >> sys.stderr, '%s: %s' % (p, e.strip ())

    def realname (self, user):
        try:
            return pwd.getpwnam (user).pw_gecos.split (',')[0]
        except KeyError:
            return user

    def expired (self, spwd, until_inactive):
        self.mail (spwd.sp_nam, 'Password expired',
'''Dear %(user)s,

Your password on %(host)s has expired.

Please log in to %(host)s, where you will be prompted to change your
password.

If you do not do so within %(until)i days, your account
will be locked due to inactivity.
''' % {'user': self.realname (spwd.sp_nam),
       'host': socket.gethostname (),
       'until': until_inactive})

    def warn (self, spwd, until_expire):
        self.mail (spwd.sp_nam, 'Password expiry warning',
'''Dear %(user)s,

Your password on %(host)s will expire in %(until)s days.

Please log in to %(host)s and change your password by running the
'passwd' command.
''' % {'user': self.realname (spwd.sp_nam),
       'host': socket.gethostname (),
       'until': until_expire})


