import cssutils
from bs4 import BeautifulSoup, Tag, Comment
import json
import sys


def calculate_content(source):
    content_resource = source.find("div", class_="page_post_sized_thumbs")
    contents = []
    if content_resource:
        contents = content_resource.findChildren("a", recursive=False)
    content_result = {}
    content_number = 0
    for content in contents:
        content_number = +1
        content_type = "undefined"
        content_url = ""
        video_url = content.get("href") if content.get("href") is not None else ""
        if content["aria-label"].count("Видео") > 0 and video_url != "":
            content_type = "video"
            content_url = str(video_url)
            content_info = {content_type: content_url}
            content_result[content_number] = content_info
        elif content["aria-label"].find("фотография") and video_url != "":
            content_type = "photo"
            content_url = str(video_url)
            content_info = {content_type: content_url}
            content_result[content_number] = content_info

        style = cssutils.parseStyle(content["style"])
        url = style["background-image"]
        url = url.split("(")
        if len(url) > 1 and url[1] is not None:
            url = url[1].replace(")", "")
        else:
            url = ""
        if url != "":
            content_number = +1
            content_type = "photo"
            content_url = str(url)
            content_info = {content_type: content_url}
            content_result[content_number] = content_info
    return content_result


def calculate_comments(comment_rule, author_rule, text_rule, likes_rule, source):
    comment_section = {}
    for i in range(len(comment_rule["class"])):
        comments = source.find_all(
            f"{comment_rule['tag'][i]}",
            class_=f"{comment_rule['class'][i]}",
            id=f"{comment_rule['id'][i]}",
        )
        for comment in comments:
            comment_author = (
                comment.find(
                    f"{author_rule['tag'][i]}",
                    class_=f"{author_rule['class'][i]}",
                    id=f"{author_rule['id'][i]}",
                )
                if comment.find(
                    f"{author_rule['tag'][i]}",
                    class_=f"{author_rule['class'][i]}",
                    id=f"{author_rule['id'][i]}",
                )
                is not None
                else ""
            )
            if (
                author_rule["variable"][i] != ""
                and comment_author != ""
                and f"{author_rule['variable'][i]}" in comment_author.attrs
            ):
                comment_author = comment_author[f"{author_rule['variable'][i]}"]
            else:
                if (
                    type(comment_author) not in [str]
                    and comment_author.text is not None
                ):
                    comment_author = comment_author.text
            comment_text = (
                comment.find(
                    f"{text_rule['tag'][i]}",
                    class_=f"{text_rule['class'][i]}",
                    id=f"{text_rule['id'][i]}",
                )
                if comment.find(
                    f"{text_rule['tag'][i]}",
                    class_=f"{text_rule['class'][i]}",
                    id=f"{text_rule['id'][i]}",
                )
                is not None
                else ""
            )
            if (
                text_rule["variable"][i] != ""
                and comment_text != ""
                and f"{text_rule['variable'][i]}" in comment_text.attrs
            ):
                comment_text = comment_text[f"{text_rule['variable'][i]}"]
            else:
                if type(comment_author) not in [str] and comment_text.text is not None:
                    comment_text = comment_text.text
            comment_likes = (
                comment.find(
                    f"{likes_rule['tag'][i]}",
                    class_=f"{likes_rule['class'][i]}",
                    id=f"{likes_rule['id'][i]}",
                )
                if comment.find(
                    f"{likes_rule['tag'][i]}",
                    class_=f"{likes_rule['class'][i]}",
                    id=f"{likes_rule['id'][i]}",
                )
                is not None
                else ""
            )
            if (
                likes_rule["variable"][i] != ""
                and comment_likes != ""
                and f"{likes_rule['variable'][i]}" in comment_likes.attrs
            ):
                comment_likes = comment_likes[f"{likes_rule['variable'][i]}"]
            else:
                if type(comment_author) not in [str] and comment_likes.text is not None:
                    comment_likes = comment_likes.text
            if comment_author != "":
                if type(comment_author) not in [str]:
                    comment_author = comment_author.text
                if type(comment_text) not in [str]:
                    comment_text = comment_text.text

                comment_container = {}
                comment_container[comment_text] = comment_likes
                comment_section[comment_author] = comment_container
    return comment_section


def get_info(name, parameters, source):
    original_name = name
    original_source = source
    if name == "post_comments_info":
        return calculate_comments(
            parameters,
            parameters["comment_author"],
            parameters["comment_text"],
            parameters["comment_likes"],
            source,
        )
    if name == "post_content_result":
        return calculate_content(source)
    # if name == "post_date":
    #     # print(source)
    #     name = (
    #         source.find(
    #             f"{parameters['tag'][0]}",
    #             class_=f"{parameters['class'][0]}",
    #             id=f"{parameters['id'][0]}",
    #         )
    #         if source.find(
    #             f"{parameters['tag'][0]}",
    #             class_=f"{parameters['class'][0]}",
    #             id=f"{parameters['id'][0]}",
    #         )
    #         is not None
    #         else ""
    #     )
    #     print(name)
    #     return name

    for i in range(
        len(parameters["class"])
    ):  # class is just for example, every parameter should contain equal elements
        # special condition for post reactions in TG
        if original_name == "post_reactions":
            reaction_amount = (
                source.find_all(
                    f"{parameters['tag'][i]}",
                    class_=f"{parameters['class'][i]}",
                    id=f"{parameters['id'][i]}",
                )
                if source.find(
                    f"{parameters['tag'][i]}",
                    class_=f"{parameters['class'][i]}",
                    id=f"{parameters['id'][i]}",
                )
                is not None
                else 0
            )
            if reaction_amount == 0:
                return 0

            reaction_amount = [int(reaction.text) for reaction in reaction_amount]
            return sum(reaction_amount)

        name = (
            source.find(
                f"{parameters['tag'][i]}",
                class_=f"{parameters['class'][i]}",
                id=f"{parameters['id'][i]}",
            )
            if source.find(
                f"{parameters['tag'][i]}",
                class_=f"{parameters['class'][i]}",
                id=f"{parameters['id'][i]}",
            )
            is not None
            else ""
        )

        if (
            parameters["variable"][i] != ""
            and name != ""
            and f"{parameters['variable'][i]}" in name.attrs
            and parameters["recursive"][i] == "False"
        ):
            name = name[f"{parameters['variable'][i]}"]
            return name
            # can add ere if name=="" -> name=0

        elif parameters["variable"][i] != "" and (
            name == "" or f"{parameters['variable'][i]}" not in name.attrs
        ):
            name = ""

        if name != "" and parameters["recursive"][i] == "False":
            if type(name) is Tag:
                if original_name == "post_text":
                    # Adding emojis to the text
                    if name.text is not None or name.text != "":
                        emoji = name.select("img.emoji")
                        if emoji:
                            for em in emoji:
                                if em in name:
                                    index = name.contents.index(em)
                                    name.contents[index].replace_with(em["alt"])
                    # Adding emojis to the text
                name = name.text
            return name

        if name != "" and parameters["recursive"][i] == "False":

            return name

        if parameters["recursive"][i] == "True":
            if name != "":
                source = name
            else:
                name = ""

        if i == len(parameters["class"]) - 1:
            return name
        else:  # was Recursive but didn't find anything inside
            source = original_source

    return name


file_rules = open(f"{sys.argv[2]}")
file_read = open(
    f"{sys.argv[3]}", encoding="utf-8", errors="ignore"
)  # encoding="cp1251" for vk
file_write = None

result = []
data = {}

data = json.load(file_rules)

if sys.argv[1] == "0":
    # Writing to sample.json
    file_write = open(f"{sys.argv[4]}", "a", encoding="utf-8", errors="ignore")


src = file_read.read()
soup = BeautifulSoup(src, "html.parser")
source_type = "VK" if soup.find("title").text != "Telegram Web" else "TG"

if source_type == "VK":
    file_read = open(f"{sys.argv[3]}", encoding="cp1251", errors="ignore")
    src = file_read.read()
    soup = BeautifulSoup(src, "html.parser")


posts = soup.find_all(
    data["post_array"]["tag"][0], class_=data["post_array"]["class"][0]
)  # array of posts of the page

group_link = ""

if source_type == "TG":
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for c in comments:
        if c.find("saved from"):
            group_link = "https" + c.split("https")[1]
            break

for post in posts:
    if (
        source_type == "VK" and post["class"].count("post") == 0
    ):  # if the class name includes other blocks reply_wrap _reply_content etc.
        continue
    info = {}
    for key in data:
        if key.find("post") == -1:
            info[key] = get_info(key, data[key], soup)
        else:
            info[key] = get_info(key, data[key], post)

    # ADDITIONAL CONFIGURATIONS
    if source_type == "TG":
        info["group_link"] = group_link
        info["node_type_name"] = "TelegramGroup"
        if info["post_date"] == "":
            info["post_date"] = post.find("div")["data-timestamp"]
    if info["post_link"] is not None and source_type == "VK":
        info["post_link"] = "vk.com" + info["post_link"]

    if (
        info["post_author_id"] is not None
        and info["post_author_id"] != ""
        and source_type == "VK"
    ):
        if info["post_author_id"][0] == "-":
            info["node_type_name"] = "VkGroup"
        else:
            info["node_type_name"] = "VkAccount"
    if info["post_views"] is not None:
        if info["post_views"].count(".") >= 1:
            info["post_views"] = info["post_views"].replace("K", "00")
            info["post_views"] = info["post_views"].replace(".", "")
        else:
            info["post_views"] = info["post_views"].replace("K", "000")
    if info["owner_followers_group"] is not None:
        if info["owner_followers_group"].count(".") >= 1:
            info["owner_followers_group"] = info["owner_followers_group"].replace(
                "K", "00"
            )
            info["owner_followers_group"] = info["owner_followers_group"].replace(
                ".", ""
            )
        else:
            info["owner_followers_group"] = info["owner_followers_group"].replace(
                "K", "000"
            )
    result.append(info)
if file_write is not None:
    json.dump(result, file_write, ensure_ascii=False)
else:
    print(result)
# file_write.write(json_object)
# 1697022880
