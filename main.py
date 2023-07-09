import codecs
from bs4 import BeautifulSoup
with open("../vk/Arina Snatkina.html",encoding="cp1251") as file:
    src = file.read()
soup = BeautifulSoup(src, "html.parser")

posts = soup.find_all("div",class_ = "_post_content") # array of posts of the page
for post in posts:

    post_author = post.find("a",class_ = "author").text if post.find("a",class_ = "author")!=None else ""

    content_type = True if (post.find("div",class_="copy_quote"))==None else False #true - post; fasle - repost
    content_type = "post" if content_type==True else "repost"

    post_text = post.find("div",class_="wall_post_text").text if post.find("div",class_="wall_post_text")!=None else ""
    post_source_text = ""
    post_repost_comment = ""
    post_source = ""

    if content_type == "repost":
        post_text = ""
        post_repost_comment = post.find("div",class_="published_comment")
        post_repost_comment = post_repost_comment.find("div",class_="wall_post_text").text if post_repost_comment!=None else ""
        post_text = post_repost_comment

        post_source = post.find("a",class_="copy_author").text if post.find("a",class_="copy_author")!=None else ""

        post_source_text = post.find("div",class_="copy_quote")
        post_source_text = post_source_text.find("div",class_="wall_post_text").text if post_source_text!=None and post_source_text.find("div",class_="wall_post_text")!=None else ""

    post_likes = post.find("div",class_="PostButtonReactions__title _counter_anim_container").text if post.find("div",class_="PostButtonReactions__title _counter_anim_container")!=None and post.find("div",class_="PostButtonReactions__title _counter_anim_container").text!="" else 0
    post_reposts = post.find("div",class_="PostBottomAction PostBottomAction--withBg share _share").text if post.find("div",class_="PostBottomAction PostBottomAction--withBg share _share")!=None else 0
    post_comments = post.find("div",class_="PostBottomAction PostBottomAction--withBg comment _comment _reply_wrap").text if post.find("div",class_="PostBottomAction PostBottomAction--withBg comment _comment _reply_wrap")!=None else 0
    post_date = post.find("span",class_="rel_date").text if post.find("span",class_="rel_date")!=None else ""
    post_views = post.find("span",class_="_views").text if post.find("span",class_="_views")!=None else 0
 

    print(post_author)
    print(content_type)
    print(post_source)
    print(post_source_text)
    print(post_text)
    print(post_likes)
    print(post_reposts)
    print(post_comments)
    print(post_views)
    print(post_date)
    print("\n") 