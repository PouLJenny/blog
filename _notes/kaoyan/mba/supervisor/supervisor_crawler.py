import os
import requests
import json
import time

session_id = '2a68f73f-3761-4b45-9633-ddb483ef06f2'

yixiang_tearchers = ['宋文燕']

def teacher_list_download():
    url = "https://dssx.buaa.edu.cn/api/pc/v1/selection/management/student/current-activity/teacher/list"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json; charset=UTF-8",
        "origin": "https://dssx.buaa.edu.cn",
        "priority": "u=1, i",
        "referer": "https://dssx.buaa.edu.cn/view/pc/v1/choice/student/online/index",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    cookies = {
        "_zte_cid_": "8cf72409-7dc7-9413-ebfd-1717647c47e6",
        "_zte_sid_": "006b82a2-6e9a-6229-f53b-1bdcc7beec56",
        "JSESSIONID": session_id
    }

    data = {
        "page": 1,
        "size": 500,
        "activityId": "ff80818195112aa3019902ad15d1085e",
        "batchId": "ff80818195112aa3019902b05b7c085f",
        "query": "",
        "title": "",
        "team": "",
        "researchDirection": ""
    }

    # 发起 POST 请求
    response = requests.post(url, headers=headers, cookies=cookies, json=data)

    # 保存到文件
    with open("/home/poul/workspace/src/blog/_notes/kaoyan/mba/supervisor/supervisor_list.json", "w", encoding="utf-8") as f:
        f.write(response.text)

    print("结果已保存到 supervisor_list.json")

def teacher_details_download():
    ## 老师详情 https://dssx.buaa.edu.cn/api/pc/v1/selection/management/student/current-activity/admission-summary/count?activityId=ff80818195112aa3019902ad15d1085e&batchId=ff80818195112aa3019902b05b7c085f&teacherId=ff80818181fa73ae0181fa85be16002d

    chuangxin_su_json = json.load(open('/home/poul/workspace/src/blog/_notes/kaoyan/mba/supervisor/supervisor_chuangxin.json'))
    chuangxin_su_json = chuangxin_su_json.get('body').get('data').get('content')

    # 目标URL
    for item in chuangxin_su_json:
        teacher_id = item.get('teacherId')
        teacher_detail_download(teacher_id)
        time.sleep(1)

def teacher_detail_download(teacher_id:str):
  url = "https://dssx.buaa.edu.cn/api/pc/v1/selection/management/student/current-activity/admission-summary/count"

  params = {
    "activityId": "ff80818195112aa3019902ad15d1085e",
    "batchId": "ff80818195112aa3019902b05b7c085f",
    "teacherId": teacher_id
  }

  headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9",
    "priority": "u=1, i",
    "referer": f"https://dssx.buaa.edu.cn/view/pc/v1/choice/student/online/teacher?activityId=ff80818195112aa3019902ad15d1085e&batchId=ff80818195112aa3019902b05b7c085f&id={teacher_id}",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
  }

  cookies = {
    "_zte_cid_": "8cf72409-7dc7-9413-ebfd-1717647c47e6",
    "_zte_sid_": "006b82a2-6e9a-6229-f53b-1bdcc7beec56",
    "JSESSIONID": session_id
  }

  # 发起请求
  response = requests.get(url, headers=headers, cookies=cookies, params=params)

  # 保存到文件
  with open(f"/home/poul/workspace/src/blog/_notes/kaoyan/mba/supervisor/teacher_details/{teacher_id}.json", "w",
            encoding="utf-8") as f:
    f.write(response.text)
  print(f"结果已保存到 {teacher_id}.json")


def generate_html():
    chuangxin_su_json = json.load(open('/home/poul/workspace/src/blog/_notes/kaoyan/mba/supervisor/supervisor_list.json'))
    chuangxin_su_json = chuangxin_su_json.get('body').get('data').get('content')
    chuangxin_teachers = {}
    for item in chuangxin_su_json:
        chuangxin_teachers[item.get('employeeName')] = item

    # -*- coding: utf-8 -*-
    faculty_list = json.load(open('/home/poul/workspace/src/blog/_notes/kaoyan/mba/supervisor/supervisor_webinfo.json'))


    html_head = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>北京航空航天大学经济管理学院教师信息</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 0; }
            h1 { text-align: center; padding: 20px; }
            .search-box { text-align: center; margin-bottom: 20px; }
            .search-box input { width: 300px; padding: 8px; font-size: 16px; }
            .faculty-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; padding: 20px; }
            .faculty-card { background-color: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); width: 250px; padding: 15px; text-align: center; transition: transform 0.2s; }
            .faculty-card:hover { transform: scale(1.05); }
            .faculty-card img { width: 120px; height: 120px; border-radius: 50%; object-fit: cover; margin-bottom: 10px; }
            .faculty-card h3 { margin: 10px 0 5px; font-size: 18px; }
            .faculty-card p { font-size: 14px; margin: 5px 0; }
            .faculty-card a { color: #1a73e8; text-decoration: none; }
            .faculty-card a:hover { text-decoration: underline; }
            .department { font-weight: bold; color: #333; }
        </style>
        <script>
            // 页面加载时恢复输入框内容
            window.onload = function() {
                var savedValue = localStorage.getItem("searchInputValue");
                if (savedValue) {
                    document.getElementById("searchInput").value = savedValue;
                    filterFaculty(); // 恢复时自动过滤
                }
            }

            function filterFaculty() {
                var input = document.getElementById("searchInput");
                var filter = input.value.toLowerCase();

                // 保存当前输入到 localStorage
                localStorage.setItem("searchInputValue", input.value);

                var cards = document.getElementsByClassName("faculty-card");
                for (var i = 0; i < cards.length; i++) {
                    var text = cards[i].innerText.toLowerCase();
                    if (text.indexOf(filter) > -1) {
                        cards[i].style.display = "";
                    } else {
                        cards[i].style.display = "none";
                    }
                }
            }
        </script>
    </head>
    <body>
        <h1>北京航空航天大学经济管理学院教师信息</h1>
        <div class="search-box">
            <input type="text" id="searchInput" onkeyup="filterFaculty()" placeholder="输入关键词搜索教师...">
        </div>
        <div class="faculty-container">
    """

    html_footer = """
        </div>
    </body>
    </html>
    """

    def generate_faculty_card(faculty):
        chuangxin_p = "<p>非指导老师</p>"
        minge = ""
        yaoqiu = ""
        if faculty['name'] in chuangxin_teachers:
            tinfo = chuangxin_teachers.get(faculty['name'])
            research_d = tinfo.get('researchDirection')
            teacher_id = tinfo.get('teacherId')
            file_path = f'/home/poul/workspace/src/blog/_notes/kaoyan/mba/supervisor/teacher_details/{teacher_id}.json'
            if not os.path.exists(file_path):
              teacher_detail_download(teacher_id)
            teacher_detail = json.load(open(file_path))
            teacher_detail = teacher_detail.get('body').get('data').get('mjwiseTeacherInfo')
            teacher_yq = ''
            if 'otherInfo' in teacher_detail and teacher_detail['otherInfo'] is not None:
                teacher_other_info = teacher_detail.get('otherInfo')
                teacher_other_info = json.loads(teacher_other_info)
                teacher_yq = [info for info in teacher_other_info if info.get("name") == "对学生的要求"]
            if len(teacher_yq) > 0:
                teacher_yq = teacher_yq[0]
                teacher_yq = teacher_yq.get('value')
            if research_d is None:
                research_d = ''
            chuangxin_p = f"<p>指导方向： {research_d.replace('$$',',')}</p>"

            remain = tinfo.get('surplusStudentNumber')
            expect = tinfo.get('enterStudentNumber')
            minge = f"<p>剩余名额：{remain} 报名学生：{expect}</p>"
            yaoqiu = f"<p>对学生要求：{teacher_yq}</p>"
        return f"""
        <div class="faculty-card">
            <img src="{faculty['img']}" alt="{faculty['name']}">
            <h3>{faculty['name']}</h3>
            <p class="department">{faculty['deptName']}</p>
            <p>职位：{faculty['job']}</p>
            <p>研究方向：{faculty['mainTarget']}</p>
            <p>Email: <a href="mailto:{faculty['email']}">{faculty['email']}</a></p>
            <p><a href="{faculty['homePage']}" target="_blank">个人主页</a></p>
            <p><a href="{faculty['deptPage']}" target="_blank">院系主页</a></p>
            {chuangxin_p}
            {minge}
            {yaoqiu}
        </div>
        """

    # 生成 HTML
    faculty_html = "".join([generate_faculty_card(f) for f in faculty_list])
    full_html = html_head + faculty_html + html_footer

    # 保存到文件
    with open("/home/poul/workspace/src/blog/_notes/kaoyan/mba/supervisor/supervisor.html", "w", encoding="utf-8") as f:
        f.write(full_html)

    print("HTML 页面已生成：buaa_sem_faculty.html")

def teacher_list_web_download():
  json_array = json.load(open('/home/poul/workspace/src/blog/_notes/kaoyan/mba/supervisor/supervisor.json'))
  all_teachers = []
  for dep in json_array:
    dep_name = dep.get('name')
    dep_page = dep.get('page')
    dep_info = {'deptName': dep_name, 'deptPage': dep_page}
    dep_teachers = dep.get('teachers')
    for dt in dep_teachers:
      dt['deptName'] = dep_name
      dt['deptPage'] = dep_page
      all_teachers.append(dt)

  print(json.dumps(all_teachers, ensure_ascii=False))



teacher_list_download()
generate_html()
