from db.dao import UserDao, PhotoDao


class Results:
    users: list[UserDao] = []

    def __init__(self, raw_data=None):
        if raw_data is None or 'data' not in raw_data:
            return
        if 'results' not in raw_data['data']:
            return
        for user in raw_data['data']['results']:
            if 'type' not in user:
                return
            if user['type'] != 'user':
                return
            if 'user' not in user:
                return
            new_user = UserDao(
                name=user['user']['name'],
                s_number=user['s_number'],
                user_id=user['user']['_id'])
            if 'city' in user['user']:
                new_user.city = user['user']['city']['name']
            if 'photos' in user['user']:
                photos = []
                for photo in user['user']['photos']:
                    photos.append(PhotoDao(
                        photo_id=photo['id'],
                        url=photo['url']
                    ))
                new_user.photos = photos
            self.users.append(new_user)


'''
Raw data example:
{
  "results": [
    {
      "type": "user",
      "user": {
        "_id": "54735a13599e187310e31bdf",
        "badges": [],
        "bio": "Hudba, příroda, šachy - nemusíš být šachista, stačí, když ...to tam bude 🙂\n",
        "birth_date": "1979-03-20T08:24:54.675Z",
        "city": {
            "name": "Pardubice"
        },
        "name": "Monika",
        "photos": [
          {
            "id": "7cce90b0-b039-43a2-9209-c5687dc13978",
            "url": "...",
            "fileName": "7cce90b0-b039-43a2-9209-c5687dc13978.jpg",
            "extension": "jpg",
            "assets": [],
            "media_type": "image"
          },
          ...
        ],
        ...
      },
      "distance_mi": 4,
      "content_hash": "R1LfemsnECrwF3rcxRIZjcL6UEAt3UR0txViZjUdZuAxIpD",
      "s_number": 7851887500488879,
      ...
    },
  ]
}
'''
