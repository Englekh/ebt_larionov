(define (problem test1-1)
(:domain test1)

(:objects 
o1 o2 - object
p0 p1 p2  - place
r - robot
)

(:init

(on o1 p2)
(on o2 p3)
(r_in r p1)

)

(:goal (get_two p2 p3 p1 o1 o2 r) )


)
