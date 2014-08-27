# -*- coding:utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.plugins.facebook.utils import facebook_language
from sc.social.like.utils import get_content_image
from sc.social.like.utils import get_language
from zope.component import getMultiAdapter

BASE_URL = 'https://www.facebook.com/plugins/like.php?'
PARAMS = 'locale=%s&href=%s&send=false&layout=%s&show_faces=true&action=%s'


class PluginView(BrowserView):

    enabled_portal_types = []
    typebutton = ''
    fb_enabled = False
    fbaction = ''
    fbadmins = ''
    language = 'en_US'

    metadata = ViewPageTemplateFile("templates/metadata.pt")
    plugin = ViewPageTemplateFile("templates/plugin.pt")

    def __init__(self, context, request):
        super(PluginView, self).__init__(context, request)
        pp = getToolByName(context, 'portal_properties')

        self.context = context
        self.title = context.title
        self.description = context.Description()
        self.request = request
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.portal = self.portal_state.portal()
        self.site_url = self.portal_state.portal_url()
        self.portal_title = self.portal_state.portal_title()
        self.url = context.absolute_url()
        self.language = facebook_language(get_language(context), self.language)
        self.sheet = getattr(pp, 'sc_social_likes_properties', None)
        self.image = get_content_image(context, width=1200, height=630)
        if self.sheet:
            self.fbaction = self.sheet.getProperty("fbaction", "")
            self.fbapp_id = self.sheet.getProperty("fbapp_id", "")
            self.fbadmins = self.sheet.getProperty("fbadmins", "")
            self.button = self.typebutton
            if self.fbaction == 'share':
                self.fbclass = 'fb-share-button'
            else:
                self.fbclass = 'fb-like'

    def image_height(self):
        """ Return height to image
        """
        img = self.image
        if img:
            return img.height

    def image_type(self):
        """ Return content type to image
        """
        img = self.image
        if img:
            return getattr(img, 'content_type',
                           getattr(img, 'mimetype', 'image/jpeg'))

    def image_width(self):
        """ Return width to image
        """
        img = self.image
        if img:
            return img.width

    def image_url(self):
        """ Return url to image
        """
        img = self.image
        if img:
            return img.url
        else:
            return '%s/logo.png' % self.site_url

    @property
    def typebutton(self):
        typebutton = self.sheet.getProperty("typebutton", "")
        show_my_counts = self.sheet.getProperty("show_my_counts", 0)
        if typebutton == 'horizontal':
            if show_my_counts:
                typebutton = 'button_count'
            else:
                typebutton = 'button'
            self.width = '90px'
        else:
            typebutton = 'box_count'
            self.width = '55px'
        return typebutton
