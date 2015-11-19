**提交门票申请:**

URL:

    api/ticket/insertApplication
    
参数:

    姓名:name(最大长度4)
    年级:grade(Int, 高一是10年级)
    班级:class(Int)
    学号:schoolID(最大长度6)
    身份证号:ID(需前端验证, 当然后端也会再次验证啦)
    申请的票的数量:requirement (默认值1)
    验证码:captcha
    
返回值:

    succes/failure(失败)/error(内部错误)/illegal(非法输入)

**提交店铺申请:**

URL:

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

**是否显示需要票的数量文本框:**

URL

    api/config/ifShowRequirementTextbox
    
返回值

    1 或 0

**首页显示按钮类型:**

URL

    api/config/getHomepageButtonType

返回值

    ticket 或 info

