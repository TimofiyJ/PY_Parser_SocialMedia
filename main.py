import codecs
import bs4
import cssutils
import os
from bs4 import BeautifulSoup
import json
import sys
result = []
# Writing to sample.json 
with open(f'{sys.argv[2]}', 'a',encoding="utf-8", errors='ignore') as file_write:

    with open(f"{sys.argv[1]}",encoding="cp1251") as file:
        src = file.read()
    soup = BeautifulSoup(src, "html.parser")
    owner_followers = 0
    owner_friends = 0
    owner_photo = 0
    owner_video = 0
    owner_audio = 0
    page_description=""
    node_type_name = "" if soup.find("div",id = "page_wall_posts")==None else True
    if node_type_name==True:
        node_type_name = "VkAccount" if soup.find("div",id = "page_wall_posts")["data-stat-container"]=="user_wall" else "VkGroup"
        if node_type_name=="VkGroup":
            page_description = soup.find("div",class_ = "page_description").text
            owner_followers=soup.find("div",class_ = "header_top clear_fix").find("span",class_="header_count fl_l").text if soup.find("div",class_ = "header_top clear_fix")!=None else 0 
            owner_followers = owner_followers.replace(" ","")
        else:
            #find_all("span",class_="header_count fl_l")
            owner_list_info = soup.find_all("div",class_ = "header_top clear_fix") if soup.find("div",class_ = "header_top clear_fix") else 0
            owner_friends=owner_list_info[0].find("span",class_="header_count fl_l").text if owner_list_info[0]!=None else 0
            owner_friends=owner_friends.replace(" ","")
            owner_followers = owner_list_info[1].find("span",class_="header_count fl_l").text if owner_list_info[1]!=None else 0
            owner_followers=owner_followers.replace(" ","")
            owner_photo =owner_list_info[2].find("span",class_="header_count fl_l").text if owner_list_info[2]!=None else 0
            owner_photo=owner_photo.replace(" ","")
            owner_video = owner_list_info[3].find("span",class_="header_count fl_l").text if owner_list_info[3]!=None else 0
            owner_video=owner_video.replace(" ","")
            owner_audio =owner_list_info[4].find("span",class_="header_count fl_l").text if owner_list_info[4]!=None else 0
            owner_audio=owner_audio.replace(" ","")
    posts = soup.find_all("div",class_ = "_post") # array of posts of the page
    for post in posts:
        if post['class'].count("post")==0: #if the class name includes other blocks reply_wrap _reply_content etc.
            continue
        post_id = post["data-post-id"]
        post_author = post.find("a",class_ = "author").text if post.find("a",class_ = "author")!=None else "" # finding author of the post
        post_author_id=post.find("a",class_ = "author")["data-from-id"] if post.find("a",class_ = "author")!=None else ""
        post_link=post.find("a",class_ = "post_link")["href"] if post.find("a",class_ = "post_link")!=None else ""
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
                        post_text.contents[index].replace_with(em['alt'])
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
                            post_source_text.contents[index].replace_with(em['alt'])
                post_source_text = post_source_text.text
            #Adding emojis to the text

        post_group_author = post.find("a",class_ = "wall_signed_by").text if post.find("a",class_ = "wall_signed_by")!=None else ""

        post_likes = post.find("div",class_="PostButtonReactions__title _counter_anim_container").text if post.find("div",class_="PostButtonReactions__title _counter_anim_container")!=None and post.find("div",class_="PostButtonReactions__title _counter_anim_container").text!="" else 0
        post_reposts = post.find("div",class_="PostBottomAction PostBottomAction--withBg share _share")['data-count'] if post.find("div",class_="PostBottomAction PostBottomAction--withBg share _share")!=None else 0
        post_comments = post.find("div",class_="PostBottomAction PostBottomAction--withBg comment _comment _reply_wrap")['data-count'] if post.find("div",class_="PostBottomAction PostBottomAction--withBg comment _comment _reply_wrap")!=None else 0
        post_date = post.find("span",class_="rel_date") if post.find("span",class_="rel_date")!=None else ""
        post_views = post.find("div",class_="like_views like_views--inActionPanel")["title"] if post.find("div",class_="like_views like_views--inActionPanel")!=None else 0
        post_views = str(post_views).split(" ")[0]
        if 'time' in post_date.attrs:
            post_date=post_date['time']
        else:
            post_date = 0
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
        "post_author_id":post_author_id,
        "post_id": post_id,
        "post_link":post_link,
        "node_type_name":node_type_name,
        "content_type": content_type,
        "post_source": post_source,
        "post_group_author": post_group_author,
        "page_description":page_description,
        "owner_friends":owner_friends,
        "owner_followers":owner_followers,
        "owner_photo":owner_photo,
        "owner_video":owner_video,
        "owner_audio":owner_audio,
        "post_source_text":post_source_text,
        "post_text":post_text,
        "post_likes":post_likes,
        "post_reposts":post_reposts,
        "post_comments":post_comments,
        "post_views":post_views,
        "post_date":post_date,
        "comment_section":comment_section,
        "content_result":content_result
        }
        result.append(info)
    json.dump(result,file_write,ensure_ascii=False)
#file_write.write(json_object)
