// 找院系
let yxList = document.querySelectorAll('div.cont a.textUl')
let yxs = []
for (const yx of yxList) {
    let yxObj = {}
    yxObj.page = yx.href
    yxObj.name = yx.title
    yxs.push(yxObj)
}
console.log(JSON.stringify(yxs,null, 2))


// 找到老师的信息
let lis = document.querySelectorAll('ul.d-ldU3 li')
let teachers = []
for (const li of lis) {
  let teacher = {}
  teacher.homePage = li.querySelector('a').href
  teacher.name = li.querySelector('a').title
  teacher.img = li.querySelector('a div.pic img').src
  teacher.job = li.querySelector('a div.job').textContent
  teacher.mainTarget = li.querySelector('a div.desc p').textContent
  teacher.email = li.querySelector('a div.email span').textContent
  teachers.push(teacher)
}
console.log(JSON.stringify(teachers))