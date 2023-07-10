import codecs
import bs4
import cssutils
from bs4 import BeautifulSoup

with open("../vk/Arina Snatkina.html",encoding="cp1251") as file:
    src = file.read()
soup = BeautifulSoup(src, "html.parser")

posts = soup.find_all("div",class_ = "_post_content") # array of posts of the page
for post in posts:
    if len(post['class'])>1: #if the class name includes other blocks reply_wrap _reply_content etc.
        continue

    post_author = post.find("a",class_ = "author").text if post.find("a",class_ = "author")!=None else ""

    content_type = True if (post.find("div",class_="copy_quote"))==None else False #true - post; fasle - repost
    content_type = "post" if content_type==True else "repost"

    post_text = post.find("div",class_="wall_post_text") if post.find("div",class_="wall_post_text")!=None else ""
    
    if post_text!="":
        emoji = post_text.select('img.emoji')
        if emoji:
            for em in emoji:
                if em in post_text:
                    index = post_text.contents.index(em)
                    post_text.contents[index].replace_with(em['alt'])
        post_text = post_text.text

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
        post_source_text = post_source_text.find("div",class_="wall_post_text") if post_source_text!=None and post_source_text.find("div",class_="wall_post_text")!=None else ""
        if post_source_text!="":
            emoji = post_source_text.select('img.emoji')
            if emoji:
                for em in emoji:
                    if em in post_source_text: 
                        index = post_source_text.contents.index(em)
                        post_source_text.contents[index].replace_with(em['alt'])
            post_source_text = post_source_text.text


    post_group_author = post.find("a",class_ = "wall_signed_by").text if post.find("a",class_ = "wall_signed_by")!=None else ""

    post_likes = post.find("div",class_="PostButtonReactions__title _counter_anim_container").text if post.find("div",class_="PostButtonReactions__title _counter_anim_container")!=None and post.find("div",class_="PostButtonReactions__title _counter_anim_container").text!="" else 0
    post_reposts = post.find("div",class_="PostBottomAction PostBottomAction--withBg share _share")['data-count'] if post.find("div",class_="PostBottomAction PostBottomAction--withBg share _share")!=None else 0
    post_comments = post.find("div",class_="PostBottomAction PostBottomAction--withBg comment _comment _reply_wrap")['data-count'] if post.find("div",class_="PostBottomAction PostBottomAction--withBg comment _comment _reply_wrap")!=None else 0
    post_date = post.find("span",class_="rel_date").text if post.find("span",class_="rel_date")!=None else ""
    post_views = post.find("span",class_="_views").text if post.find("span",class_="_views")!=None else 0

    print(post_author)
    print(content_type)
    print(post_source)
    print(post_group_author)
    print(post_source_text)
    print(post_text)
    print(post_likes)
    print(post_reposts)
    print(post_comments)
    print(post_views)
    print(post_date)

    #GETTING CONTENT#
    content_resource = post.find("div",class_="page_post_sized_thumbs")
    if content_resource:
        contents = content_resource.findChildren("a" , recursive=False)

    for content in contents:
        video_url = content.get("href") if content.get("href")!=None else ""
        if content['aria-label'].count('Видео')>0 and video_url!="":
            print("URL FOR VIDEO:"+str(video_url))
        elif content['aria-label'].find('фотография') and video_url!="":
            print("URL FOR PHOTO:"+str(video_url))
        style = cssutils.parseStyle(content['style'])
        url = style['background-image']
        url = url.split("(")
        url = url[1].replace(")", "")
        print("URL FOR PHOTO:"+str(url))
    
    print("POST COMMENTS:")
    comments = post.find_all("div",class_ = "reply_content")
    for comment in comments:
        comment_author = comment.find("a",class_ = "author").text if comment.find("a",class_ = "author")!=None else ""
        comment_text = comment.find("div",class_ = "wall_reply_text").text if comment.find("div",class_ = "wall_reply_text")!=None else ""
        comment_likes = comment.find("a",class_ = "like_btn")['data-count'] if comment.find("a",class_ = "like_btn")!=None else 0
        print(comment_author)
        print(comment_text)
        print(comment_likes)
