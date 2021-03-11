import requests
import json


class Parser:

    def __init__(self, host):
        self.host = host

    def get(self, url):
        return requests.get(f'{self.host}{url}').json()

    def post(self, url, *args, **kwargs):
        return requests.post(f'{self.host}{url}')

    def get_posts(self):
        return self.get('api/article/posts/')

    def get_posts_top_by_like(self):
        return self.get('api/article/posts/top_by_likes/')

    def get_posts_top_by_comments(self):
        return self.get('api/article/posts/top_by_comments/')

    def get_one_post(self, post_id):
        return self.get(f'api/article/posts/{post_id}/')

    def do_like(self, post_id):
        return self.post((f'api/article/posts/{post_id}/do_like/'), data=json.dumps({"session_key": 1}),
                         headers={"Content-Type": "application/json"}).json()

    def post_comment(self, post_id):
        data = {
            'author': 'dsadasdasd',
            'body': 'fasafdasd'
        }
        # return requests.post((f'{self.host}api/article/posts/{post_id}/comments/'),
        #                          data=json.dumps(data), headers={"Content-Type": "application/json"}).text
        return self.post((f'api/article/posts/{post_id}/comments/'), data=json.dumps(data),
                         headers={"Content-Type": "application/json"}).text


local = Parser('http://127.0.0.1:8000/')
heroku = Parser('https://dw-project.herokuapp.com/')
#
# print('local')
# print(local.get_posts())
# print(local.get_posts_top_by_like())
# print(local.get_posts_top_by_comments())
# print(local.get_one_post(1202))
print(local.do_like(1202))
print(local.post_comment(1301))

# print('heroku')
# print(heroku.get_posts())


# while True:
#     text = (
#         "Posts \n"
#         "Posts_top_by_like \n"
#         "Posts_top_by_comments \n"
#         "Post \n"
#         "Like \n"
#         "Comment \n"
#         "End"
#     )
#     print(text)
#     user_input = input('Виберіть операцію яку хочете виконати: ').lower()
#
#     if user_input == "end":
#         break
#     elif user_input == 'posts':
#         print(heroku.get_posts())
#     elif user_input == 'posts_top_by_like':
#         print(heroku.get_posts_top_by_like())
#     elif user_input == 'posts_top_by_comments':
#         print(heroku.get_posts_top_by_comments())
#     elif user_input == 'post':
#         print(heroku.get_one_post(input('Введіть ID поста: ')))
#     elif user_input == 'like':
#         print(heroku.do_like('Введіть ID поста якому хочете поставити лайк: '))
#     elif user_input == 'comment':
#         post_id = input('Введіть ID поста якому хочете залишити коментар: ')
#         heroku.post_comment(post_id, {
#             'author': input("Введіть ім\'я автора "),
#             'body': input('Введіть текст поста: ')
#         })
#     else:
#         print('Невірна операція \n')
