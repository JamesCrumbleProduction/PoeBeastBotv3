^LButton::autoClicks(30, 40)
+LButton::autoClicks(80, 90)


autoClicks(min, max) {
  Send {blind}{Lbutton down}{Lbutton up} 
  sleep, 50
  while getkeystate("LButton", "p")
  {
    Send {blind}{Lbutton down}{Lbutton up} 
    sleep, rand(min, max)
  }
  
  return
}


rand(min, max) {
   random, ran, min, max
   return ran
}