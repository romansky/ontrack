from openid.consumer.consumer import Consumer, \
    SUCCESS, CANCEL, FAILURE, SETUP_NEEDED
from openid.consumer.discover import DiscoveryFailure
from django.utils.encoding import smart_unicode

from django.db import models
from django.conf import settings
from django.utils.hashcompat import md5_constructor

from openid.store.interface import OpenIDStore
import openid.store 
from openid.association import Association as OIDAssociation
import time, base64

from models import Association, Nonce
from django.db import transaction
from django.shortcuts import redirect



class DjangoOpenIDStore(OpenIDStore):
    """
The Python openid library needs an OpenIDStore subclass to persist data
related to OpenID authentications. This one uses our Django models.
"""

    def storeAssociation(self, server_url, association):
        assoc = Association(
            server_url = server_url,
            handle = association.handle,
            secret = base64.encodestring(association.secret),
            issued = association.issued,
            lifetime = association.issued,
            assoc_type = association.assoc_type
        )
        assoc.save()

    def getAssociation(self, server_url, handle=None):
        assocs = []
        if handle is not None:
            assocs = Association.objects.filter(
                server_url = server_url, handle = handle
            )
        else:
            assocs = Association.objects.filter(
                server_url = server_url
            )
        if not assocs:
            return None
        associations = []
        for assoc in assocs:
            association = OIDAssociation(
                assoc.handle, base64.decodestring(assoc.secret), assoc.issued,
                assoc.lifetime, assoc.assoc_type
            )
            if association.getExpiresIn() == 0:
                self.removeAssociation(server_url, assoc.handle)
            else:
                associations.append((association.issued, association))
        if not associations:
            return None
        return associations[-1][1]

    def removeAssociation(self, server_url, handle):
        assocs = list(Association.objects.filter(
            server_url = server_url, handle = handle
        ))
        assocs_exist = len(assocs) > 0
        for assoc in assocs:
            assoc.delete()
        return assocs_exist

    def useNonce(self, server_url, timestamp, salt):
        # Has nonce expired?
        if abs(timestamp - time.time()) > openid.store.nonce.SKEW:
            return False
        try:
            nonce = Nonce.objects.get(
                server_url__exact = server_url,
                timestamp__exact = timestamp,
                salt__exact = salt
            )
        except Nonce.DoesNotExist:
            nonce = Nonce.objects.create(
                server_url = server_url,
                timestamp = timestamp,
                salt = salt
            )
            return True
        nonce.delete()
        return False

    def cleanupNonce(self):
        Nonce.objects.filter(
            timestamp__lt = (int(time.time()) - nonce.SKEW)
        ).delete()

    def cleaupAssociations(self):
        Association.objects.extra(
            where=['issued + lifetimeint < (%s)' % time.time()]
        ).delete()

    def getAuthKey(self):
        # Use first AUTH_KEY_LEN characters of md5 hash of SECRET_KEY
        return md5_constructor.new(settings.SECRET_KEY).hexdigest()[:self.AUTH_KEY_LEN]

    def isDumb(self):
        return False




def google_signin(request):
    """ This is the view where the Google account login icon on your site points to, e.g. http://www.yourdomain.com/google-signin """
    consumer = Consumer(request.session, DjangoOpenIDStore())

    # catch Google Apps domain that is referring, if any 
    _domain = None
    if 'domain' in request.POST:
        _domain = request.POST['domain']
    elif 'domain' in request.GET:
        _domain = request.GET['domain']

    try:
        # two different endpoints depending on whether the using is using Google Account or Google Apps Account
        if _domain:
            auth_request = consumer.begin('https://www.google.com/accounts/o8/site-xrds?hd=%s' % _domain)
        else:
            auth_request = consumer.begin('https://www.google.com/accounts/o8/id')
    except DiscoveryFailure as e:
        return CustomError(request, "Google Accounts Error", "Google's OpenID endpoint is not available.")

    # add requests for additional account information required, in my case: email, first name & last name
    auth_request.addExtensionArg('http://openid.net/srv/ax/1.0', 'mode', 'fetch_request')
    auth_request.addExtensionArg('http://openid.net/srv/ax/1.0', 'required', 'email,firstname,lastname')
    auth_request.addExtensionArg('http://openid.net/srv/ax/1.0', 'type.email', 'http://schema.openid.net/contact/email')
    auth_request.addExtensionArg('http://openid.net/srv/ax/1.0', 'type.firstname', 'http://axschema.org/namePerson/first')
    auth_request.addExtensionArg('http://openid.net/srv/ax/1.0', 'type.lastname', 'http://axschema.org/namePerson/last')

    return redirect(auth_request.redirectURL('http://localhost', 'http://localhost/post_login'))


@transaction.commit_manually 
def google_signin_response(request):
    """ Callback from Google Account service with login the status. Your url could be http://www.yourdomain.com/google-signin-response """
    transaction.rollback() # required due to Django's transaction inconsistency between calls
    oidconsumer = Consumer(request.session, DjangoOpenIDStore())

    # parse GET parameters submit them with the full url to consumer.complete
    _params = dict((k,smart_unicode(v)) for k, v in request.GET.items())
    info = oidconsumer.complete(_params, request.build_absolute_uri().split('?')[0])
    display_identifier = info.getDisplayIdentifier()

    if info.status == FAILURE and display_identifier:
        return CustomError(request, _("Google Login Error"), _("Verification of %(user)s failed: %(error_message)s") % {'user' : display_identifier, 'error_message' : info.message})

    elif info.status == SUCCESS:
        try:
            _email = info.message.args[('http://openid.net/srv/ax/1.0', 'value.email')]
            _first_name = info.message.args[('http://openid.net/srv/ax/1.0', 'value.firstname')]
            _last_name = info.message.args[('http://openid.net/srv/ax/1.0', 'value.lastname')]
            try:
                _user = User.objects.get(email__iexact=_email)
            except ObjectDoesNotExist:
                # create a new account if one does not exist with the authorized email yet and log that user in
                _new_user = _new_account(_email, _first_name + ' ' + _last_name, _first_name, _last_name, p_account_status=1)
                _login(request, _new_user, info.message.args[('http://specs.openid.net/auth/2.0', 'response_nonce')])
                transaction.commit()
                return redirect('home')
            else:
                # login existing user
                _login(request, _user, info.message.args[('http://specs.openid.net/auth/2.0', 'response_nonce')])
                transaction.commit()
                return redirect('home')
        except Exception as e:
            transaction.rollback()
            system_log_entry(e, request=request)
            return CustomError(request, _("Login Unsuccessful"), "%s" % e)

    elif info.status == CANCEL:
        return CustomError(request, _("Google Login Error"), _('Google account verification cancelled.'))

    elif info.status == SETUP_NEEDED:
        if info.setup_url:
            return CustomError(request, _("Google Login Setup Needed"), _('<a href="%(url)s">Setup needed</a>') % { 'url' : info.setup_url })
        else:
            # This means auth didn't succeed, but you're welcome to try
            # non-immediate mode.
            return CustomError(request, _("Google Login Setup Needed"), _('Setup needed'))
    else:
        # Either we don't understand the code or there is no
        # openid_url included with the error. Give a generic
        # failure message. The library should supply debug
        # information in a log.
        return CustomError(request, _("Google Login Error"), _('Google account verification failed for an unknown reason. Please try to create a manual account on Acquee.'))


def get_url_host(request):
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    host = escape(get_host(request))
    return '%s://%s' % (protocol, host)