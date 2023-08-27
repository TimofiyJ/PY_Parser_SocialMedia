import codecs
import bs4
import cssutils
import os
from bs4 import BeautifulSoup, Tag
import json
import sys

def calculate_content(source):
    content_resource = source.find("div",class_="page_post_sized_thumbs")
    contents=[]
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
    return content_result

def calculate_comments(comment_rule, author_rule, text_rule, likes_rule, source):
    comment_section= {}
    for i in range(len(comment_rule["class"])):
        comments = source.find_all(f"{comment_rule['tag'][i]}",class_=f"{comment_rule['class'][i]}",id=f"{comment_rule['id'][i]}")
        for comment in comments:
            comment_author = comment.find(f"{author_rule['tag'][i]}",class_=f"{author_rule['class'][i]}",id=f"{author_rule['id'][i]}") if comment.find(f"{author_rule['tag'][i]}",class_=f"{author_rule['class'][i]}",id=f"{author_rule['id'][i]}")!=None else f"{i}-step-not-found"
            if author_rule["variable"][i]!="" and comment_author!= f"{i}-step-not-found" and f"{author_rule['variable'][i]}" in comment_author.attrs:
                comment_author = comment_author[f"{author_rule['variable'][i]}"]
            else:
                if comment_author.text!=None:
                    comment_author = comment_author.text
            comment_text = comment.find(f"{text_rule['tag'][i]}",class_=f"{text_rule['class'][i]}",id=f"{text_rule['id'][i]}") if comment.find(f"{text_rule['tag'][i]}",class_=f"{text_rule['class'][i]}",id=f"{text_rule['id'][i]}")!=None else f"{i}-step-not-found"
            if text_rule["variable"][i]!="" and comment_text!= f"{i}-step-not-found" and f"{text_rule['variable'][i]}" in comment_text.attrs:
                comment_text = comment_text[f"{text_rule['variable'][i]}"]
            else:
                if comment_text.text!=None:
                    comment_text = comment_text.text
            comment_likes = comment.find(f"{likes_rule['tag'][i]}",class_=f"{likes_rule['class'][i]}",id=f"{likes_rule['id'][i]}") if comment.find(f"{likes_rule['tag'][i]}",class_=f"{likes_rule['class'][i]}",id=f"{likes_rule['id'][i]}")!=None else f"{i}-step-not-found"
            if likes_rule["variable"][i]!="" and comment_likes!= f"{i}-step-not-found" and f"{likes_rule['variable'][i]}" in comment_likes.attrs:
                comment_likes = comment_likes[f"{likes_rule['variable'][i]}"]
            else:
                if comment_likes.text!=None:
                    comment_likes = comment_likes.text
            if comment_author!="":
                comment_container = {}
                comment_container[comment_text] = comment_likes
                comment_section[comment_author] = comment_container
    return comment_section

def get_info(name,parameters,source):

    original_name = name

    if name=="post_comments_info":
        return calculate_comments(parameters,parameters["comment_author"],parameters["comment_text"],parameters["comment_likes"],source)
    if name=="post_content_result":
        return calculate_content(source)
    
    for i in range(len(parameters["class"])): #class is just for example, every parameter should contain equal elements
        name = source.find(f"{parameters['tag'][i]}",class_=f"{parameters['class'][i]}",id=f"{parameters['id'][i]}") if source.find(f"{parameters['tag'][i]}",class_=f"{parameters['class'][i]}",id=f"{parameters['id'][i]}")!=None else f"{i}-step-not-found"
        if parameters["variable"][i]!="" and name!= f"{i}-step-not-found" and f"{parameters['variable'][i]}" in name.attrs and parameters["recursive"][i]=="False":
            name = name[f"{parameters['variable'][i]}"]
            return name
            #can add ere if name=="" -> name=0

        elif parameters["variable"][i]!="" and (name== f"{i}-step-not-found" or f"{parameters['variable'][i]}" not in name.attrs):
            name = f"{i}-step-not-found"
        
        if name!=f"{i}-step-not-found" and parameters["recursive"][i]=="False":
            if type(name) == Tag:
                if original_name=="post_text":
                    #Adding emojis to the text
                    if name.text!="":
                        emoji = name.select('img.emoji')
                        if emoji:
                            for em in emoji:
                                if em in name: 
                                    index = name.contents.index(em)
                                    name.contents[index].replace_with(em['alt'])
                    #Adding emojis to the text
                name=name.text
            return name
        
        if name!=f"{i}-step-not-found" and parameters["recursive"][i]=="False":
            return name
        
        if parameters["recursive"][i]=="True":
            if(name!=f"{i}-step-not-found"):
                source=name
            else:
                return ""
                break
    if name==original_name:
        return ""
    return name

file_rules = open(f'{sys.argv[2]}')
file_read = open(f"{sys.argv[3]}",encoding="cp1251")
file_write=None

result = []
data={}

data=json.load(file_rules)

if sys.argv[1]=="0":
    # Writing to sample.json 
    file_write= open(f'{sys.argv[4]}', 'a',encoding="utf-8", errors='ignore')


src = file_read.read()
soup = BeautifulSoup(src, "html.parser")

posts = soup.find_all("div",class_ = "_post") # array of posts of the page

for post in posts:
    if post['class'].count("post")==0: #if the class name includes other blocks reply_wrap _reply_content etc.
        continue

    info = {}

    for key in data:
        if key.find("post")==-1:
            info[key] = get_info(key,data[key],soup)
        else:
            info[key] = get_info(key,data[key],post)  

    # ADDITIONAL CONFIGURATIONS 
    if info["post_link"]!=None:
        info["post_link"] = "vk.com"+info["post_link"]
    
    if info["post_likes"]=="":
        info["post_likes"]=0

    if info["post_author_id"]!=None and info["post_author_id"]!="":
        if info["post_author_id"][0]=="-":
            info["node_type_name"] = "VkGroup"
        else:
            info["node_type_name"]="VkAccount"

    # #find_all("span",class_="header_count fl_l")
    # owner_list_info = soup.find_all("div",class_ = "header_top clear_fix") if soup.find("div",class_ = "header_top clear_fix") else ""
    # if owner_list_info!="":
    #     owner_friends=owner_list_info[0].find("span",class_="header_count fl_l").text if owner_list_info[0]!=None else 0
    #     owner_friends=owner_friends.replace(" ","")
    #     owner_followers = owner_list_info[1].find("span",class_="header_count fl_l").text if owner_list_info[1]!=None else 0
    #     owner_followers=owner_followers.replace(" ","")
    #     owner_photo =owner_list_info[2].find("span",class_="header_count fl_l").text if owner_list_info[2]!=None else 0
    #     owner_photo=owner_photo.replace(" ","")
    #     owner_video = owner_list_info[3].find("span",class_="header_count fl_l").text if owner_list_info[3]!=None else 0
    #     owner_video=owner_video.replace(" ","")
    #     owner_audio =owner_list_info[4].find("span",class_="header_count fl_l").text if owner_list_info[4]!=None else 0
    #     owner_audio=owner_audio.replace(" ","")


    # if content_type == "repost":
    #     post_text = "" #if repost -> text = post_repost_comment
    #     post_repost_comment = post.find("div",class_="published_comment")
    #     post_repost_comment = post_repost_comment.find("div",class_="wall_post_text").text if post_repost_comment!=None else ""
    #     post_text = post_repost_comment


    #     post_source = post.find("a",class_="copy_author").text if post.find("a",class_="copy_author")!=None else ""

    #     post_source_text = post.find("div",class_="copy_quote") #finding text of the post
    #     post_source_text = post_source_text.find("div",class_="wall_post_text") if post_source_text!=None and post_source_text.find("div",class_="wall_post_text")!=None else ""
        
    result.append(info)
if file_write!=None:
    json.dump(result,file_write,ensure_ascii=False)
else:
    print(result)
#file_write.write(json_object)
