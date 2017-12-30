class Element(object):
    # (id, kind, user_id, title, url, username, password, form_data, comment, status)

    def __init__(self, title, kind='website', url='', username='', password='', form_data='', comment='', status=1):
        self.title = title
        self.kind = kind
        self.url = url
        self.username = username
        self.password = password
        self.form_data = form_data
        self.comment = comment
        self.status = status

    def print(self):
        print('Title:', self.title)
        print('Kind:', self.kind)
        print('URL:', self.url and self.url or 'None')
        print('Username:', self.username and self.username or 'None')

        if self.comment:
            print('Comment:', self.comment)

