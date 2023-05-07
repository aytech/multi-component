app_routes: dict = {
    'DELETE_USER': '/api/users/<int:user_id>',
    'GET_ARCHIVE_LOGS': '/api/logs/archive',
    'GET_LOGS': '/api/logs',
    'GET_TAIL_LOGS': '/api/logs/tail',
    'GET_SETTINGS': '/api/settings',
    'GET_SETTINGS_LIKES': '/api/settings/likes',
    'HIDE_USER': '/api/users/<int:user_id>/hide',
    'LIKE_USER': '/api/users/<int:user_id>/like',
    'LIST_USERS': '/api/users',
    'SAVE_API_TOKEN': '/api/settings/token/<string:token>',
    'SAVE_BASE_URL': '/api/settings/url/<string:url>',
    'SCHEDULE_LIKE': '/api/users/schedule/<int:user_id>',
    'SEARCH_LOGS': '/api/logs/search',
    'SEARCH_USERS': '/api/users/search/<string:name>'
}
