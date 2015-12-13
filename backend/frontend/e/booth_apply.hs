import Haste
import Haste.Events
import Haste.DOM

import Control.Monad

clearBox box _ = setProp box "value" ""
fillBox box val _ = do
    s <- getProp box "value"
    if null s
    then setProp box "value" val >> return ()
    else return ()

setClickToClear (id', val) = withElem id' $ \box -> do
    onEvent box Focus (clearBox box)
    onEvent box Blur (fillBox box val)
    return ()

main = do
    let textboxList = [("ownerName", "申请人姓名..."), ("ownerContact", "联系方式..."), ("shopName", "摊位名..."), ("privilegeKey", "申请密钥...(没有请填00000000)"), ("captcha", "计算两数相乘结果...")]
    forM_ textboxList setClickToClear
    return ()
