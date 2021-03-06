import os
import re
from datetime import datetime, timezone, timedelta

path = os.path.dirname(os.path.abspath(__file__))
# old_html_file = path + "\\original_memories_history.html"
# new_html_file = path + "\\memories_history.html"
# os.rename(new_html_file, new_html_file)
old_html_file = path + "\\memories_history.html"
new_html_file = path + "\\new_memories_history.html"

# first row of memories is after 10231 characters
#   (file.read(10231) is probably the command you want)

with open(file=old_html_file, encoding="utf_8") as old_html_file:
    old_html = old_html_file.read()

with open(file=new_html_file, mode="w", encoding="utf_8") as new_html_file:
    new_html_file.write(r"""<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title> </title>
        <style>
            body {
                font-size: 14px;
                font-family: 'Avenir Next','Helvetica Neue', Arial, Helvetica, sans-serif;
                margin: 20px auto;
                width: 1200px;
            }

            b {
                font-weight: 600;
            }

            table {
                width: 100%;
                table-layout: fixed;
            }

            .ghost {
                padding: 10px;
                height: 150px;
                width: 150px;
                background-color: #FFFE00;
                display: block;
                margin: auto;
                border-radius: 10px;
            }

            .leftpanel {
                float: left;
                width: 300px;
                color: #6c6c6c;
            }

            .leftpanel a {
                text-decoration: none;
                color: #6c6c6c;
            }

            .leftpanel ul {
                margin-left: 20px;
                padding: 0;
            }

            .leftpanel li {
                display: block;
                padding: 11px 16px;
            }

            .leftpanel li:hover {
                background-color: #f3f3f3;
            }

            .rightpanel th {
                text-align : left
            }

            .rightpanel {
                padding-left: 310px;
                padding-top: 5px;
            }

            .rightpanel th, td {
                padding: 15px;
                font-weight: normal;
            }

            .bold-headers th {
                font-weight: 600;
            }
            
            .options-dropdown {
                position: relative;
                display: inline-block;
            }
            
            .options-dropdown ul {
                display: none;
                position: absolute;
                min-width: 100%;
                z-index: 1;
                left: 0;
            }
            
            .options-dropdown:hover ul {
                display: block;
            }
            
            .options-dropdown ul li {
                display: block;
            }

        </style>
    </head>
    <body>
        <div class="leftpanel">
            <img class="ghost" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA1MDAgNTAwIj48ZGVmcz48c3R5bGU+LmNscy0xe2ZpbGw6I2ZmZjt9PC9zdHlsZT48L2RlZnM+PHRpdGxlPjFBcnRib2FyZCAxIGNvcHkgMjwvdGl0bGU+PGcgaWQ9IlBSSU1BUllfLV9HSE9TVCIgZGF0YS1uYW1lPSJQUklNQVJZIC0gR0hPU1QiPjxwYXRoIGNsYXNzPSJjbHMtMSIgZD0iTTQxNy45MywzNDAuNzFjLTYwLjYxLTI5LjM0LTcwLjI3LTc0LjY0LTcwLjctNzgtLjUyLTQuMDctMS4xMS03LjI3LDMuMzgtMTEuNDEsNC4zMy00LDIzLjU0LTE1Ljg5LDI4Ljg3LTE5LjYxLDguODEtNi4xNiwxMi42OS0xMi4zMSw5LjgzLTE5Ljg3LTItNS4yMy02Ljg3LTcuMi0xMi03LjJhMjIuMywyMi4zLDAsMCwwLTQuODEuNTRjLTkuNjgsMi4xLTE5LjA4LDYuOTUtMjQuNTIsOC4yNmE4LjU2LDguNTYsMCwwLDEtMiwuMjdjLTIuOSwwLTQtMS4yOS0zLjcyLTQuNzguNjgtMTAuNTgsMi4xMi0zMS4yMy40NS01MC41Mi0yLjI5LTI2LjU0LTEwLjg1LTM5LjY5LTIxLTUxLjMyQzMxNi44LDEwMS40MywyOTQsNzcuMiwyNTAsNzcuMlMxODMuMjMsMTAxLjQzLDE3OC4zNSwxMDdjLTEwLjE4LDExLjYzLTE4LjczLDI0Ljc4LTIxLDUxLjMyLTEuNjcsMTkuMjktLjE3LDM5LjkzLjQ1LDUwLjUyLjIsMy4zMi0uODIsNC43OC0zLjcyLDQuNzhhOC42NCw4LjY0LDAsMCwxLTItLjI3Yy01LjQzLTEuMzEtMTQuODMtNi4xNi0yNC41MS04LjI2YTIyLjMsMjIuMywwLDAsMC00LjgxLS41NGMtNS4xNSwwLTEwLDItMTIsNy4yLTIuODYsNy41NiwxLDEzLjcxLDkuODQsMTkuODcsNS4zMywzLjcyLDI0LjU0LDE1LjYsMjguODcsMTkuNjEsNC40OCw0LjE0LDMuOSw3LjM0LDMuMzgsMTEuNDEtLjQzLDMuNDEtMTAuMSw0OC43MS03MC43LDc4LTMuNTUsMS43Mi05LjU5LDUuMzYsMS4wNiwxMS4yNCwxNi43Miw5LjI0LDI3Ljg1LDguMjUsMzYuNSwxMy44Miw3LjM0LDQuNzMsMywxNC45Myw4LjM0LDE4LjYxLDYuNTYsNC41MywyNS45NS0uMzIsNTEsNy45NSwyMSw2LjkyLDMzLjc2LDI2LjQ3LDcxLDI2LjQ3czUwLjM3LTE5LjY0LDcxLTI2LjQ3YzI1LTguMjcsNDQuNDMtMy40Miw1MS03Ljk1LDUuMzMtMy42OCwxLTEzLjg4LDguMzQtMTguNjEsOC42NS01LjU3LDE5Ljc3LTQuNTgsMzYuNS0xMy44MkM0MjcuNTIsMzQ2LjA3LDQyMS40OCwzNDIuNDMsNDE3LjkzLDM0MC43MVoiLz48cGF0aCBkPSJNNDQ0LjMsMzM3LjI2Yy0yLjcyLTcuNC03LjktMTEuMzYtMTMuOC0xNC42NC0xLjExLS42NS0yLjEzLTEuMTctMy0xLjU3LTEuNzYtLjkxLTMuNTYtMS43OS01LjM1LTIuNzItMTguMzktOS43NS0zMi43NS0yMi4wNS00Mi43MS0zNi42M2E4My4wNiw4My4wNiwwLDAsMS03LjMzLTEzYy0uODUtMi40My0uODEtMy44MS0uMi01LjA3YTguMjUsOC4yNSwwLDAsMSwyLjM1LTIuNDVjMy4xNi0yLjA5LDYuNDItNC4yMSw4LjYzLTUuNjQsMy45NC0yLjU1LDcuMDYtNC41Nyw5LjA3LTYsNy41NS01LjI4LDEyLjgzLTEwLjg5LDE2LjEzLTE3LjE2QTM0LjE3LDM0LjE3LDAsMCwwLDQwOS43OCwyMDRjLTUtMTMuMTYtMTcuNDMtMjEuMzMtMzIuNDktMjEuMzNhNDQuNzUsNDQuNzUsMCwwLDAtOS40NSwxYy0uODMuMTgtMS42Ni4zNy0yLjQ3LjU4LjE0LTktLjA2LTE4LjUtLjg2LTI3Ljg1LTIuODQtMzIuODctMTQuMzUtNTAuMS0yNi4zNS02My44NEExMDUsMTA1LDAsMCwwLDMxMS4zNyw3MUMyOTMuMTYsNjAuNiwyNzIuNTEsNTUuMzIsMjUwLDU1LjMyUzIwNi45NCw2MC42LDE4OC43MSw3MWExMDQuNjIsMTA0LjYyLDAsMCwwLTI2Ljg0LDIxLjZjLTEyLDEzLjc0LTIzLjUxLDMxLTI2LjM1LDYzLjg0LS44LDkuMzUtMSwxOC45LS44NywyNy44NS0uODEtLjIxLTEuNjMtLjQtMi40Ni0uNThhNDQuNzUsNDQuNzUsMCwwLDAtOS40NS0xYy0xNS4wNywwLTI3LjUyLDguMTctMzIuNSwyMS4zM2EzNC4yMSwzNC4yMSwwLDAsMCwxLjY1LDI4LjQxYzMuMzEsNi4yNyw4LjU5LDExLjg4LDE2LjE0LDE3LjE2LDIsMS40LDUuMTMsMy40Miw5LjA3LDYsMi4xMywxLjM4LDUuMjQsMy40LDguMjksNS40MmE4LjksOC45LDAsMCwxLDIuNjYsMi42N2MuNjQsMS4zMS42NiwyLjcyLS4yOSw1LjMyYTgyLjI5LDgyLjI5LDAsMCwxLTcuMjEsMTIuNzNjLTkuNzQsMTQuMjUtMjMuNjgsMjYuMzMtNDEuNDgsMzYtOS40Myw1LTE5LjIzLDguMzQtMjMuMzcsMTkuNTktMy4xMiw4LjQ5LTEuMDgsMTguMTUsNi44NSwyNi4yOWgwYTM5LjYzLDM5LjYzLDAsMCwwLDEwLDcuNTcsMTA4LjM1LDEwOC4zNSwwLDAsMCwyNC40Nyw5Ljc5LDE2LjE2LDE2LjE2LDAsMCwxLDQuOTQsMi4yMWMyLjg5LDIuNTMsMi40OCw2LjM0LDYuMzMsMTEuOTJhMjcuOCwyNy44LDAsMCwwLDcuMjQsNy4zNmM4LjA4LDUuNTgsMTcuMTYsNS45MywyNi43OCw2LjMsOC42OS4zMywxOC41NC43MSwyOS43OSw0LjQyLDQuNjYsMS41NCw5LjUsNC41MiwxNS4xMSw4LDEzLjQ3LDguMjgsMzEuOTEsMTkuNjEsNjIuNzcsMTkuNjFzNDkuNDMtMTEuMzksNjMtMTkuN2M1LjU3LTMuNDIsMTAuMzgtNi4zNywxNC45MS03Ljg3LDExLjI1LTMuNzIsMjEuMS00LjA5LDI5Ljc5LTQuNDIsOS42Mi0uMzcsMTguNy0uNzIsMjYuNzgtNi4zYTI3Ljg5LDI3Ljg5LDAsMCwwLDguMjQtOWMyLjc3LTQuNzEsMi43LTgsNS4zLTEwLjNhMTUuMzIsMTUuMzIsMCwwLDEsNC42NC0yLjEyLDEwOC43NiwxMDguNzYsMCwwLDAsMjQuOC05Ljg4QTM5LDM5LDAsMCwwLDQzNy45NCwzNjNsLjEtLjEyQzQ0NS40OCwzNTQuOTIsNDQ3LjM1LDM0NS41NCw0NDQuMywzMzcuMjZaTTQxNi44NywzNTJjLTE2LjczLDkuMjQtMjcuODUsOC4yNS0zNi41LDEzLjgyLTcuMzUsNC43My0zLDE0LjkzLTguMzQsMTguNjEtNi41Niw0LjUzLTI1Ljk1LS4zMi01MSw3Ljk1LTIwLjY2LDYuODMtMzMuODQsMjYuNDctNzEsMjYuNDdTMjAwLDM5OS4yNSwxNzksMzkyLjMzYy0yNS04LjI3LTQ0LjQzLTMuNDItNTEtNy45NS01LjMzLTMuNjgtMS0xMy44OC04LjM0LTE4LjYxQzExMSwzNjAuMiw5OS44OCwzNjEuMTksODMuMTYsMzUyYy0xMC42NS01Ljg4LTQuNjEtOS41Mi0xLjA2LTExLjI0LDYwLjYtMjkuMzQsNzAuMjctNzQuNjQsNzAuNy03OCwuNTItNC4wNywxLjEtNy4yNy0zLjM4LTExLjQxLTQuMzMtNC0yMy41NC0xNS44OS0yOC44Ny0xOS42MS04LjgyLTYuMTYtMTIuNy0xMi4zMS05Ljg0LTE5Ljg3LDItNS4yMyw2Ljg4LTcuMiwxMi03LjJhMjIuMywyMi4zLDAsMCwxLDQuODEuNTRjOS42OCwyLjEsMTkuMDgsNi45NSwyNC41MSw4LjI2YTguNjQsOC42NCwwLDAsMCwyLC4yN2MyLjksMCwzLjkyLTEuNDYsMy43Mi00Ljc4LS42Mi0xMC41OS0yLjEyLTMxLjIzLS40NS01MC41MiwyLjI5LTI2LjU0LDEwLjg0LTM5LjY5LDIxLTUxLjMyLDQuODgtNS41OSwyNy44MS0yOS44Miw3MS42Ni0yOS44MlMzMTYuOCwxMDEuNDMsMzIxLjY4LDEwN2MxMC4xNywxMS42MywxOC43MywyNC43OCwyMSw1MS4zMiwxLjY3LDE5LjI5LjIzLDM5Ljk0LS40NSw1MC41Mi0uMjMsMy40OS44Miw0Ljc4LDMuNzIsNC43OGE4LjU2LDguNTYsMCwwLDAsMi0uMjdjNS40NC0xLjMxLDE0Ljg0LTYuMTYsMjQuNTItOC4yNmEyMi4zLDIyLjMsMCwwLDEsNC44MS0uNTRjNS4xNSwwLDEwLDIsMTIsNy4yLDIuODYsNy41Ni0xLDEzLjcxLTkuODMsMTkuODctNS4zMywzLjcyLTI0LjU0LDE1LjYtMjguODcsMTkuNjEtNC40OSw0LjE0LTMuOSw3LjM0LTMuMzgsMTEuNDEuNDMsMy40MSwxMC4wOSw0OC43MSw3MC43LDc4QzQyMS40OCwzNDIuNDMsNDI3LjUyLDM0Ni4wNyw0MTYuODcsMzUyWiIvPjwvZz48L3N2Zz4=">
            <ul>
                <li><a href="account.html">Login History and Account Information</a></li>
                <li><a href="snap_history.html">Snap History Metadata</a></li>
                <li><a href="chat_history.html">Chat History Metadata</a></li>
                <li><a href="shared_story.html">Our Story & Spotlight Content</a></li>
                <li><a href="purchase_history.html">Purchase History</a></li>
                <li><a href="shop_history.html">Shop History</a></li>
                <li><a href="support_note.html">Snapchat Support History</a></li>
                <li><a href="user_profile.html">User Profile</a></li>
                <li><a href="snap_pro.html">Public Profiles</a></li>
                <li><a href="friends.html">Friends</a></li>
                <li><a href="ranking.html">Ranking</a></li>
                <li><a href="story_history.html">Story History</a></li>
                <li><a href="account_history.html">Account History</a></li>
                <li><a href="location_history.html">Location</a></li>
                <li><a href="search_history.html">Search History</a></li>
                <li><a href="terms_history.html">Terms History</a></li>
                <li><a href="subscriptions.html">Subscriptions</a></li>
                <li><a href="bitmoji.html">Bitmoji</a></li>
                <li><a href="in_app_surveys.html">In-app Surveys</a></li>
                <li><a href="in_app_reports.html">Reported Content</a></li>
                <li><a href="bitmoji_kit_user.html">Bitmoji Kit</a></li>
                <li><a href="connected_apps.html">Connected Apps</a></li>
                <li><a href="talk_history.html">Talk History</a></li>
                <li><a href="snap_ads.html">Ads Manager</a></li>
                <li><a href="snap_games_and_minis.html">Snap Games and Minis</a></li>
                <li><a href="community_lenses.html">My Lenses</a></li>
                <li><a href="memories_history.html">Memories</a></li>
                <li><a href="cameos_metadata.html">Cameos</a></li>
                <li><a href="email_campaign_history.html">Email Campaign History</a></li>
                <li><a href="snap_tokens_order_history.html">Snap Tokens</a></li>
                <li><a href="payouts.html">Payouts</a></li>
                <li><a href="scans.html">Scans</a></li>
                <li><a href="netsuite_orders.html">Orders</a></li>
                <li><a href="snap_map_places_history.html">Snap Map Places</a></li>
                <li><a href="snapcode_scan_history.html">Snapcode Scan History</a></li>
                <li><a href="item_favorites.html">Shopping Favorites</a></li>
                <li><a href="payments.html">Payments</a></li>
                <li><a href="faq.html">Frequently Asked Questions</a></li>
                <li><a href="custom_sounds.html">My Sounds</a></li>
            </ul>
        </div>
        <div class="rightpanel">
            <h1>Memories</h1>
            <p>This section includes information about Memories you've saved in Snapchat. Download links below will expire 7 days from when your data file was made available to you.</p>
            <p class="important"></p>
            <script>
                const htmlPath = decodeURI(location.pathname);
                const regex = /(?<=\/).*(?=\/)/;
                const path = regex.exec(htmlPath)[0];
                function getPath() {return path;}
                function copyFilePath(fileLocalPath) 
                {
                    navigator.clipboard.writeText(path + fileLocalPath);
                }
            </script>
            <script type="module">
                let images = document.getElementsByTagName("img");
                for (let i = 1; i < images.length; i++) {
                    images[i].setAttribute("src", "file:///" + getPath() + images[i].getAttribute("src").slice(0,-4) + ".jpg");
                }
            </script>
            <div id='mem-info-bar' style='color:red'></div>
            <table id="table">
                <tbody>
                    <tr>
                        <th style="white-space: nowrap; overflow: hidden;">
                            <strong>
                                Date <a id="sort" href="javascript:reverseTable();" style="text-decoration:inherit;color:inherit;">???</a>
                            </strong>
                        </th>
                        <th style="white-space: nowrap;" class="options-dropdown">
                            <strong>Media Type</strong>
                            <ul class="options-list">
                                <li><a href="javascript:toggleImages();">Show Images</a></li>
                                <li><a href="javascript:toggleVideos();">Show Videos</a></li>
                            </ul>
                        </th>
                        <th style="white-space: nowrap; overflow: hidden;">
                            <strong> </strong>
                        </th>
                    </tr>
                    <script>
                        const table = document.getElementById("table");
                        const rows = table.rows;
                        const sort = document.getElementById("sort");
                        function reverseTable() {
                            let newTBody = table.createTBody();
                            newTBody.appendChild(rows[0]);
                            for (let i = rows.length - 1; i >= 0; i--)
                            {
                                newTBody.appendChild(rows[i]);
                            }
                            table.removeChild(table.getElementsByTagName("tbody")[0]);
                            if (sort.innerHTML == "???") {sort.innerHTML = "???";}
                            else {sort.innerHTML = "???";}
                        }
                    </script>""")

    regex = re.compile(r"(?<=<td>).*?(?=</td>)", flags=re.S)
    rows = re.findall(r"(?<=<tr>).*?(?=</tr>)", string=old_html, flags=re.S)
    duplicate_count = 0

    # for x in range(1, len(rows)):
    for x in range(1, 11):
        date, media_type = tuple(regex.findall(rows[x])[:2])
        dt = [int(group) for group in re.split("[- :]", date[:-4])]
        dt = datetime(dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], 0, timezone.utc)
        dt_text = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        dt = dt.astimezone()
        if x != 1 and date == regex.search(rows[x - 1]).group(0):
            duplicate_count += 1
            dt = dt - timedelta(seconds=duplicate_count)
        file_name = dt.strftime("%Y%m%d%H%M%S")

        if media_type == "Image":
            file_name = file_name + ".jpg"
        else:
            file_name = file_name + ".mp4"
        new_html_file.write(f"""
                    <tr>
                        <td>{dt_text}</td>
                        <td class="{media_type.lower()}">{media_type}</td>
                        <td>
                            <a href=\"javascript:copyFilePath('/Memories/{file_name}');\">
                                <img src='/Thumbnails/{file_name}'>
                            </a>
                        </td>
                    </tr>""")
    new_html_file.write("""
                </tbody>
            </table>
            <script>
                const images = document.getElementsByClassName("image");
                const videos = document.getElementsByClassName("video");
                const imageCheckmark = document.getElementById("image-checkmark");
                const videoCheckmark = document.getElementById("video-checkmark");
                let hideImages = false;
                let hideVideos = false;
                function toggleImages() {
                    hideImages = !hideImages;
                    Array.from(images).forEach((element) => {element.parentNode.hidden = hideImages});
                }
                function toggleVideos() {
                    hideVideos = !hideVideos;
                    Array.from(videos).forEach((element) => {element.parentNode.hidden = hideVideos});
                }
            </script>
        </div>
    </body>
</html>""")
