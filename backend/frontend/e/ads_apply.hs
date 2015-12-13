import Haste
import Haste.Prim
import Haste.Foreign
import Haste.DOM
import Haste.Events
import Haste.Ajax

import Control.Monad
import Control.Applicative

getDataURL = ffi $ toJSStr "(function(s){var reader=new FileReader();reader.readAsDataURL(document.getElementById(s).files[0]);return reader.result;})" :: String -> IO String

onSubmitResultReturn :: Maybe String -> IO ()
onSubmitResultReturn (Just s) = return ()

buildPara [] = return []
buildPara (s:ss) = do
    val <- withElem s $ \e -> getProp e "value"
    (:) <$> return (s, val) <*> buildPara ss

submit = do
    dataURL <- getDataURL "addPic"
    paras <- (:) <$> return ("adPic", dataURL) <*> buildPara ["owner", "ownerContact", "ownerType", "isJoined", "captcha"]
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
    withElem "btn_submit" $ \btn -> onEvent btn Click onSubmit
    return ()

