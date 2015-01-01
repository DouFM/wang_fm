# coding:utf-8
from resource.files import FileResource
from resource.music import MusicQueryResource
from resource.channel import ChannelQueryResource
from resource.playlist import PlaylistListResource, PlaylistResource
from resource.user import UserProfileResource, UserHistoryResource, UserMusicResource, UserLogoutResource
from resource.oauth import OAuthRequest, OAuthAccess
from resource.app_auth import AppAuthRequest
url = {
    #####################user#####################
    '/api/user/logout/': UserLogoutResource,
    '/api/user/profile/': UserProfileResource,
    '/api/user/history/': UserHistoryResource,
    '/api/user/music/': UserMusicResource,

    ###################oauth######################
    '/api/oauth/request/': OAuthRequest,
    '/api/oauth/access/<string:request_token>/': OAuthAccess,
    '/api/app_auth/': AppAuthRequest,

    ###################fs#########################
    '/api/fs/<string:key>/': FileResource,

    ####################music######################
    '/api/music/': MusicQueryResource,
    #'/api/music/<string:key>': MusicResource,

    ###################channel####################
    '/api/channel/': ChannelQueryResource,
    #'/api/channel/<string:key>/': ChannelResource,

    ###################playlist####################
    '/api/playlist/': PlaylistListResource,
    '/api/playlist/<string:key>/': PlaylistResource
}


def set_url_map(api):
    global url
    for key in url:
        api.add_resource(url[key], key)
