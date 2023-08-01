import codecs
import bs4
import cssutils
import os
from bs4 import BeautifulSoup
import json
current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(current_file_path)
previous_directory = os.path.dirname(parent_directory)
previous_directory = os.path.dirname(parent_directory)
item_path = os.path.join(previous_directory, "vk")

# Writing to sample.json 
with open(f'{parent_directory}/result.json', 'a',encoding="cp1251", errors='ignore') as file_write:

    with open(f"{item_path}/No Ukraine!.html",encoding="cp1251") as file:
        src = file.read()
    soup = BeautifulSoup(src, "html.parser")

    posts = soup.find_all("div",class_ = "_post_content") # array of posts of the page
    for post in posts:
        if len(post['class'])>1: #if the class name includes other blocks reply_wrap _reply_content etc.
            continue

        post_author = post.find("a",class_ = "author").text if post.find("a",class_ = "author")!=None else "" # finding author of the post

        content_type = True if (post.find("div",class_="copy_quote"))==None else False #true - post; fasle - repost
        content_type = "post" if content_type==True else "repost"

        post_text = post.find("div",class_="wall_post_text") if post.find("div",class_="wall_post_text")!=None else "" #text of the post 
        
        #Adding emojis to the text
        if post_text!="":
            emoji = post_text.select('img.emoji')
            if emoji:
                for em in emoji:
                    if em in post_text:
                        index = post_text.contents.index(em)
                        #post_text.contents[index].replace_with(em['alt'])
            post_text = post_text.text
        #Adding emojis to the text

        post_source_text = ""
        post_repost_comment = ""
        post_source = ""

        if content_type == "repost":
            post_text = "" #if repost -> text = post_repost_comment
            post_repost_comment = post.find("div",class_="published_comment")
            post_repost_comment = post_repost_comment.find("div",class_="wall_post_text").text if post_repost_comment!=None else ""
            post_text = post_repost_comment


            post_source = post.find("a",class_="copy_author").text if post.find("a",class_="copy_author")!=None else ""

            post_source_text = post.find("div",class_="copy_quote") #finding text of the post
            post_source_text = post_source_text.find("div",class_="wall_post_text") if post_source_text!=None and post_source_text.find("div",class_="wall_post_text")!=None else ""
            
            #Adding emojis to the text
            if post_source_text!="":
                emoji = post_source_text.select('img.emoji')
                if emoji:
                    for em in emoji:
                        if em in post_source_text: 
                            index = post_source_text.contents.index(em)
                            #post_source_text.contents[index].replace_with(em['alt'])
                post_source_text = post_source_text.text
            #Adding emojis to the text

        post_group_author = post.find("a",class_ = "wall_signed_by").text if post.find("a",class_ = "wall_signed_by")!=None else ""

        post_likes = post.find("div",class_="PostButtonReactions__title _counter_anim_container").text if post.find("div",class_="PostButtonReactions__title _counter_anim_container")!=None and post.find("div",class_="PostButtonReactions__title _counter_anim_container").text!="" else 0
        post_reposts = post.find("div",class_="PostBottomAction PostBottomAction--withBg share _share")['data-count'] if post.find("div",class_="PostBottomAction PostBottomAction--withBg share _share")!=None else 0
        post_comments = post.find("div",class_="PostBottomAction PostBottomAction--withBg comment _comment _reply_wrap")['data-count'] if post.find("div",class_="PostBottomAction PostBottomAction--withBg comment _comment _reply_wrap")!=None else 0
        post_date = post.find("span",class_="rel_date").text if post.find("span",class_="rel_date")!=None else ""
        post_views = post.find("span",class_="_views").text if post.find("span",class_="_views")!=None else 0
        #print(post_text[2396:2397])
        #print(post_views)
        #print("\n\n\n\n\n")
        #GETTING CONTENT#
        content_resource = post.find("div",class_="page_post_sized_thumbs")
        if content_resource:
            contents = content_resource.findChildren("a" , recursive=False)
        content_result = {} 
        content_number=0
        for content in contents:
            content_number=+1
            content_type="undefined"
            content_url=""
            video_url = content.get("href") if content.get("href")!=None else ""
            if content['aria-label'].count('Видео')>0 and video_url!="":
                content_type = "video"
                content_url = str(video_url)
                content_info = {content_type:content_url}
                content_result[content_number]=content_info
            elif content['aria-label'].find('фотография') and video_url!="":
                content_type = "photo"
                content_url = str(video_url)
                content_info = {content_type:content_url}
                content_result[content_number]=content_info
            style = cssutils.parseStyle(content['style'])
            url = style['background-image']
            url = url.split("(")
            url = url[1].replace(")", "")
            if url!="":
                content_number=+1
                content_type = "photo"
                content_url = str(url)
                content_info = {content_type:content_url}
                content_result[content_number]=content_info
                #print("URL FOR PHOTO:"+str(url))
        
        #print("POST COMMENTS:")
        comments = post.find_all("div",class_ = "reply_content")
        comment_section= {}

        for comment in comments:
            comment_author = comment.find("a",class_ = "author").text if comment.find("a",class_ = "author")!=None else ""
            comment_text = comment.find("div",class_ = "wall_reply_text").text if comment.find("div",class_ = "wall_reply_text")!=None else ""
            comment_likes = comment.find("a",class_ = "like_btn")['data-count'] if comment.find("a",class_ = "like_btn")!=None else 0
            if comment_author!="":
                comment_container = {}
                comment_container[comment_text] = comment_likes
                comment_section[comment_author] = comment_container
            #print(comment_author)
            #print(comment_text)
            #print(comment_likes)
        
        # Data to be written
        info = {
        "post_author": post_author,
        "content_type": content_type,
        "post_source": post_source,
        "post_group_author": post_group_author,
        "post_source_text":post_source_text,
        "post_text":post_text[2395:2396],
        "post_likes":post_likes,
        "post_reposts":post_reposts,
        "post_comments":post_comments,
        "post_views":post_views,
        "post_date":post_date,
        "comment_section":comment_section,
        "content_result":content_result
        }
        json.dump(info,file_write,ensure_ascii=False)
        #file_write.write(json_object)
