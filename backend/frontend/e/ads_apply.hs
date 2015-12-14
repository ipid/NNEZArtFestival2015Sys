import Haste
import Haste.Prim
import Haste.Foreign
import Haste.DOM
import Haste.Events
import Haste.Ajax

import Control.Monad
import Control.Applicative

clearBox box val _ = do
    s <- getProp box "value"
    if s == val
    then setProp box "value" "" >> return ()
    else return ()

fillBox box val _ = do
    s <- getProp box "value"
    if null s
    then setProp box "value" val >> return ()
    else return ()

setClickToClear (id', val) = withElem id' $ \box -> do
    onEvent box Focus (clearBox box val)
    onEvent box Blur (fillBox box val)
    return ()

getDataURL = ffi $ toJSStr "(function(s,f){var reader=new FileReader();reader.readAsDataURL(document.getElementById(s).files[0]);reader.onload=function(){f(reader.result);};})" :: String -> (String -> IO ()) -> IO ()

onSubmitResultReturn :: Maybe String -> IO ()
onSubmitResultReturn (Just s) = alert s

buildPara [] = return []
buildPara (s:ss) = do
    val <- withElem s $ \e -> getProp e "value"
    (:) <$> return (s, val) <*> buildPara ss

submit = getDataURL "adPic" onDataURLReady

onDataURLReady dataURL = do
    paras <- (:) <$> return ("adPic", dataURL) <*> buildPara ["ownerName", "ownerContact", "ownerType", "isJoined", "captcha"]
    ajaxRequest POST "/api/advertisement/insertApplication" paras onSubmitResultReturn
    return ()

onCaptchaVerified :: Maybe String -> IO ()
onCaptchaVerified Nothing = alert "Internal Error!"
onCaptchaVerified (Just "1") = submit
onCaptchaVerified (Just "0") = alert "验证码错误"

onSubmit _ = do
    captcha <- withElem "captcha" $ \box -> getProp box "value"
    ajaxRequest GET ("/api/captcha/verify?code=" ++ captcha) noParams onCaptchaVerified
    return ()

main = do
    let textboxList = [("ownerName", "申请人姓名..."), ("ownerContact", "联系方式..."), ("captcha", "计算两数相乘结果...")]
    forM_ textboxList setClickToClear

    withElem "btn_submit" $ \btn -> onEvent btn Click onSubmit
    return ()

