**提交门票申请:**

    api/ticket/insertApplication

参数:

    姓名:name(最大长度4)
    年级:grade(最大长度1)
    班级:classNo(最大长度2)
    学号:schoolID(最大长度6)
    身份证号:societyID(需前端验证, 当然后端也会再次验证啦)
    申请的票的数量:requirement (默认值1)
    验证码:captcha
    
**获得门票申请数量:**

    api/ticket/queryApplicationNumber
    
返回值:
    
    数量
    
**检索门票申请:**

    api/ticket/indexApplication
    
参数:

    起始:from
    长度:len
    
返回:
    同下, ID从from开始,长度为len的所有申请

**精确查询门票申请:**

    api/ticket/queryApplication

返回值:

    {
        "state":"[success/failure/error/illegal]",
        "result":[
            {
                "applicationID":
                "name":
                "grade":
                "classNo":
                "schoolID":
                "societyID":
                "requirement":
            }
        ]
    }

参数:

    申请ID:applicationID
    姓名:name
    年级:grade
    班级:classNo
    学号:schoolID
    身份证号:societyID
    申请的票的数量:requirement
    若不需要则[置空], 缺少字段则返回错误

**删除门票申请:**

    api/ticket/deleteApplication

返回值:

    success/failure/error/illegal

参数:

    申请id:applicationID

**更改门票申请:**

    api/ticket/modifyApplication

返回值:

    success/failure/error/illegal

参数:

    和提交一样, 少一个验证码, 多一个applicationID

**提交店铺申请:**

    api/shop/insertApplication

参数:

    申请人姓名:owner(最大长度4)
    申请人联系方式:ownerContact(最大长度64)
    商铺名:shopName(最大长度32)
    申请人类型:ownerType
      0 == 凤岭高中部班级/国际班 (默认值)
      1 == 教师
      2 == 凤岭高中部社团/国际班社团
      3 == 凤岭高中部个人/国际班个人
      4 == 非学生个人
      5 == 东盟中学
      6 == 二中初中部/新民中学
    申请人年级:ownerGrade(同上)
    申请人班级:ownerClass(同上)
    是否需要电力:electricity(1或0)
    是否贩卖食物:food(1或0)
    是否贩卖非食物:nonFood(1或0)
    密钥:privilegeKey(8位, 默认00000000)
    验证码:captcha

返回值:

    success/failure(失败)/error(内部错误)/illegal(非法输入)
    
**获得店铺申请数量:**

    api/shop/queryApplicationNumber
    
返回值:
    
    数量
    
**检索店铺申请:**

    api/shop/indexApplication
    
参数:

    起始:from
    长度:len
    
返回:
    同下, ID从from开始,长度为len的所有申请

**精确查询店铺申请:**

    api/shop/queryApplication

返回值:

    {
        "state":"[success/failure/error/illegal]",
        "result":[
            {
                "applicationID":
                "owner":
                "ownerContact":
                "shopName":
                "ownerType":
                "ownerGrade":
                "ownerClass":
                "electrcity":
                "food":
                "nonFood":
                "privilegeKey":
            }
        ]
    }

参数:

    申请ID:applicationID
    姓名:owner
    年级:grade
    班级:ownerContact
    店名:shopName
    类型:ownerType
    年级:ownerGrade
    班级:ownerClass
    用电:electricity
    食物:food
    非食物:nonFood
    密钥:privilegeKey
    若不需要则[置空], 缺少字段则返回错误

**删除店铺申请:**

    api/shop/deleteApplication

返回值:

    success/failure/error/illegal

参数:

    申请id:applicationID

**更改店铺申请:**

    api/shop/modifyApplication

返回值:

    success/failure/error/illegal

参数:

    和提交一样, 少一个验证码, 多一个applicationID

**是否显示需要票的数量文本框:**

    api/config/ifShowRequirementTextbox

返回值

    1 或 0

**首页显示按钮类型:**

    api/config/getHomepageButtonType

返回值

    ticket 或 info

**获取验证码:**

    api/captcha/get

    返回验证码图片
    验证码存储在session的code中

**验证验证码:**

    api/captcha/verify?code=[code]

返回值

    1(正确) 或 0(错误)


**管理界面登陆**

    api/admin/login

参数:

    密码:password
    验证码:captcha

返回值:

    success(登陆成功)/illegal(验证码错误)/failure(登陆失败)/error(内部错误)

**管理界面登出**

    api/admin/logout

返回值:

    success/failure/error

**验证是否登录**

    api/admin/isAdmin

参数:

    无

返回值:

    1(已经登录)/0(没有登录)
