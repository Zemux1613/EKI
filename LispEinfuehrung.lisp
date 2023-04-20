(setq x 3)                                   ; x = 3
(setq y (+ x (* x x)))                       ; y = x + (x*x)
(print (+ y x))                              ; print x + y

(defun quad (z) (* z z))                     ; define a function named quad with the argument "z" and the return value "z*z".
(print (quad 2))                             ; call function quad with 2 as argument
(print (quad x))                             ; call function quad with variable as argument
(print (quad y))                             ; call function quad with variable as argument
(print (quad (* x x)))                       ; call function quad with x*x as argument
(print (quad (+ y y)))                       ; call function quad with y+y as argument
(print (quad (+ (* x x) y x x x x)))         ; call function quad with (x*x)+y+x+x+x+x as argument
