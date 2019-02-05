(define (problem test1-1)
(:domain test1)

(:objects 
o1 o2 o3 o4 o5  - object
p0 p1 p2  - place
)

(:init

(on o1 o2) (on o2 o3) (on o2 o4) (on o1 o5)

(in o1 p2)
(in o2 p2)
(in o3 p2)
(in o4 p2)
(in o5 p2)
 



)

(:goal (do-smth o2 o3) ) 


)
